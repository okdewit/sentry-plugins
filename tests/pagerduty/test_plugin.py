from __future__ import absolute_import

import responses

from exam import fixture
from sentry.models import Rule
from sentry.plugins import Notification
from sentry.testutils import TestCase
from sentry.utils import json

from sentry_plugins.pagerduty.plugin import PagerDutyPlugin

INVALID_METHOD = '{"status":"invalid method","message":"You must use HTTP POST to submit your event"}'

SUCCESS = """{
  "status": "success",
  "message": "Event processed",
  "incident_key": "73af7a305bd7012d7c06002500d5d1a6"
}"""


class PagerDutyPluginTest(TestCase):
    @fixture
    def plugin(self):
        return PagerDutyPlugin()

    def test_conf_key(self):
        assert self.plugin.conf_key == 'pagerduty'

    def test_is_configured(self):
        assert self.plugin.is_configured(self.project) is False
        self.plugin.set_option('service_key', 'abcdef', self.project)
        assert self.plugin.is_configured(self.project) is True

    @responses.activate
    def test_simple_notification(self):
        responses.add('GET', 'https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                      body=INVALID_METHOD)
        responses.add('POST', 'https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                      body=SUCCESS)
        self.plugin.set_option('service_key', 'abcdef', self.project)

        group = self.create_group(message='Hello world', culprit='foo.bar')
        event = self.create_event(group=group, message='Hello world', tags={'level': 'warning'})

        rule = Rule.objects.create(project=self.project, label='my rule')

        notification = Notification(event=event, rule=rule)

        with self.options({'system.url-prefix': 'http://example.com'}):
            self.plugin.notify(notification)

        request = responses.calls[0].request
        payload = json.loads(request.body)
        assert payload == {
            'client_url': 'http://example.com',
            'event_type': 'trigger',
            'contexts': [{
                'text': 'Issue Details',
                'href': 'http://example.com/baz/bar/issues/{}/'.format(group.id),
                'type': 'link',
            }],
            'incident_key': group.id,
            'client': 'sentry',
            'details': {
                'project': self.project.name,
                'release': None,
                'url': 'http://example.com/baz/bar/issues/1/',
                'culprit': group.culprit,
                'platform': None,
                'event_id': event.event_id,
                'tags': {
                    'level': 'warning',
                },
                'datetime': event.datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
            'service_key': 'abcdef',
            'description': event.get_legacy_message(),
        }
