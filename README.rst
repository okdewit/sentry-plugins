sentry-plugins
==============

Extensions for Sentry.

Install the package via ``pip``::

    pip install --no-use-pep517 sentry-plugins

The :code:`--no-use-pep517` applies to pip >= 19, since pep517-compliant pip `doesn't work well with sentry's setup.py <https://github.com/getsentry/getsentry/pull/3074/>`_. This may be fixed in the future.

Run migrations after installation is complete::

    sentry upgrade

**Active Plugins**

* `Splunk <src/sentry_plugins/splunk/README.rst>`_
* `Asana <src/sentry_plugins/asana/README.rst>`_
* Amazon SQS
* Heroku
* Pagerduty
* Phabricator
* Pivotal
* Clubhouse
* Pushover
* Segment
* Sessionstack
* Victorops

**Deprecated Plugins**

These plugins have been replaced with Sentry's built in `Global Integrations <https://docs.sentry.io/workflow/integrations/global-integrations/>`_.

* `Slack <src/sentry_plugins/slack/README.rst>`_
* `GitHub <src/sentry_plugins/github/README.rst>`_
* `Gitlab <src/sentry_plugins/gitlab/README.rst>`_
* `Bitbucket <src/sentry_plugins/bitbucket/README.rst>`_
* `Visual Studio Team Services <src/sentry_plugins/vsts/README.rst>`_
* Jira
