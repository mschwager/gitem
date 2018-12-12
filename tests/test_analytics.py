#!/usr/bin/env python

import collections
import unittest

try:
    # Python 3
    from unittest import mock
except ImportError:
    # Python 2 (third-party)
    import mock

import requests
import pytest

from gitem import analytics
from gitem import api


class TestAnalytics(unittest.TestCase):

    def test_get_organization_information(self):
        return_value = (
            {
                'name': 'name1',
                'description': 'desc1',
                'blog': 'blog1',
                'html_url': 'hu1',
                'created_at': 'ca1',
                'updated_at': 'ua1',
                'email': 'email1',
                'location': 'loc1',
                'login': 'test1',
                'public_repos': 'pr1',
            },
            requests.codes.OK,
        )

        ghapi = mock.MagicMock()
        ghapi.get_public_organization = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_organization_information(ghapi, "unused")

        expected = collections.OrderedDict([
            ('Organization Name', 'name1'),
            ('Description', 'desc1'),
            ('Website', 'blog1'),
            ('Github URL', 'hu1'),
            ('Created', 'ca1'),
            ('Last Updated', 'ua1'),
            ('Email Address', 'email1'),
            ('Location', 'loc1'),
            ('Username', 'test1'),
            ('# of Public Repositories', 'pr1'),
        ])

        assert result == expected

    def test_get_organization_repositories(self):
        return_value = [
            (
                [{
                    'name': 'name1',
                    'description': 'desc1',
                    'html_url': 'hu1',
                    'clone_url': 'cu1',
                    'watchers_count': 'wc1',
                    'stargazers_count': 'sc1',
                    'forks_count': 'fc1',
                    'created_at': 'ca1',
                    'updated_at': 'ua1',
                    'pushed_at': 'pa1',
                }],
                requests.codes.OK,
            ),
        ]

        ghapi = mock.MagicMock()
        ghapi.get_organizations_public_repositories = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_organization_repositories(ghapi, "unused")

        expected = [
            collections.OrderedDict([
                ('Repository Name', 'name1'),
                ('Description', 'desc1'),
                ('Github URL', 'hu1'),
                ('Clone URL', 'cu1'),
                ('Watchers', 'wc1'),
                ('Stars', 'sc1'),
                ('Forks', 'fc1'),
                ('Created', 'ca1'),
                ('Last Updated', 'ua1'),
                ('Last Pushed', 'pa1'),
            ]),
        ]

        assert result == expected

    def test_get_organization_members(self):
        return_value = [
            (
                [{
                    'login': 'test1',
                    'site_admin': 'sa1',
                    'html_url': 'hu1',
                }],
                requests.codes.OK,
            ),
            (
                [{
                    'login': 'test2',
                    'site_admin': 'sa2',
                    'html_url': 'hu2',
                }],
                requests.codes.OK,
            ),
        ]

        ghapi = mock.MagicMock()
        ghapi.get_organizations_public_members = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_organization_members(ghapi, "unused")

        expected = [
            collections.OrderedDict([
                ('Username', 'test1'),
                ('Site Administrator', 'sa1'),
                ('Github URL', 'hu1'),
            ]),
            collections.OrderedDict([
                ('Username', 'test2'),
                ('Site Administrator', 'sa2'),
                ('Github URL', 'hu2'),
            ]),
        ]

        assert result == expected

    def test_get_repository_information(self):
        return_value = (
            {
                'name': 'name1',
                'description': 'desc1',
                'homepage': 'home1',
                'html_url': 'hu1',
                'clone_url': 'cu1',
                'created_at': 'ca1',
                'updated_at': 'ua1',
                'pushed_at': 'pa1',
                'language': 'lang1',
                'forks_count': 'fc1',
                'stargazers_count': 'sc1',
                'watchers_count': 'wc1',
            },
            requests.codes.OK,
        )

        ghapi = mock.MagicMock()
        ghapi.get_public_repository = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_repository_information(ghapi, "unused", "unused")

        expected = collections.OrderedDict([
            ('Repository Name', 'name1'),
            ('Description', 'desc1'),
            ('Homepage', 'home1'),
            ('Github URL', 'hu1'),
            ('Clone URL', 'cu1'),
            ('Created', 'ca1'),
            ('Last Updated', 'ua1'),
            ('Last Pushed', 'pa1'),
            ('Language', 'lang1'),
            ('Forks', 'fc1'),
            ('Stars', 'sc1'),
            ('Watchers', 'wc1'),
        ])

        assert result == expected

    def test_get_repository_contributors(self):
        return_value = [
            (
                [{
                    'login': 'test1',
                    'contributions': 'cont1'
                }],
                requests.codes.OK
            ),
            (
                [{
                    'login': 'test2',
                    'contributions': 'cont2'
                }],
                requests.codes.OK
            ),
        ]

        ghapi = mock.MagicMock()
        ghapi.get_repository_contributors = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_repository_contributors(ghapi, "unused", "unused")

        expected = [
            collections.OrderedDict([
                ('Username', 'test1'),
                ('Contributions', 'cont1'),
            ]),
            collections.OrderedDict([
                ('Username', 'test2'),
                ('Contributions', 'cont2'),
            ]),
        ]

        assert result == expected

    def test_get_user_information(self):
        return_value = (
            {
                'login': 'username1',
                'html_url': 'hu1',
                'name': 'name1',
                'company': 'co1',
                'blog': 'blog1',
                'location': 'loc1',
                'email': 'email1',
                'created_at': 'ca1',
                'updated_at': 'ua1',
            },
            requests.codes.OK,
        )

        ghapi = mock.MagicMock()
        ghapi.get_user = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_user_information(ghapi, "unused")

        expected = collections.OrderedDict([
            ('Username', 'username1'),
            ('Github URL', 'hu1'),
            ('Name', 'name1'),
            ('Company', 'co1'),
            ('Blog', 'blog1'),
            ('Location', 'loc1'),
            ('Email Address', 'email1'),
            ('Created', 'ca1'),
            ('Updated', 'ua1'),
        ])

        assert result == expected

    def test_get_user_organization(self):
        return_value = [
            (
                [{
                    'login': 'test1'
                }],
                requests.codes.OK
            ),
            (
                [{
                    'login': 'test2'
                }],
                requests.codes.OK
            ),
        ]

        ghapi = mock.MagicMock()
        ghapi.get_users_public_organizations = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_user_organizations(ghapi, "unused")

        expected = [
            collections.OrderedDict([
                ('Organization', 'test1'),
            ]),
            collections.OrderedDict([
                ('Organization', 'test2'),
            ]),
        ]

        assert result == expected

    def test_get_user_repositories(self):
        return_value = [
            (
                [{
                    'name': 'name1',
                    'description': 'desc1',
                    'html_url': 'hu1',
                    'clone_url': 'cu1',
                }],
                requests.codes.OK,
            )
        ]

        ghapi = mock.MagicMock()
        ghapi.get_users_public_repositories = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_user_repositories(ghapi, "unused")

        expected = [
            collections.OrderedDict([
                ('Repository Name', 'name1'),
                ('Description', 'desc1'),
                ('Github URL', 'hu1'),
                ('Clone URL', 'cu1'),
            ])
        ]

        assert result == expected

    def test_get_repository_commit_emails_basic(self):
        return_value = [
            (
                [{
                    'commit': {
                        'author': {
                            'name': 'username1',
                            'email': 'email1',
                        },
                    },
                }],
                requests.codes.OK,
            )
        ]

        ghapi = mock.MagicMock()
        ghapi.get_repository_commits = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_repository_commit_emails(ghapi, "unused", "unused")

        expected = {('username1', 'email1')}

        assert result == expected

    def test_get_repository_commit_emails_conflict(self):
        def conflict_generator():
            raise api.ApiCallException(requests.codes.CONFLICT, "unused")
            yield  # Empty yield to make this a generator

        return_value = conflict_generator()

        ghapi = mock.MagicMock()
        ghapi.get_repository_commits = mock.MagicMock(
            return_value=return_value
        )

        result = analytics.get_repository_commit_emails(ghapi, "unused", "unused")

        expected = set()

        assert result == expected

    def test_get_repository_commit_emails_not_conflict(self):
        def not_conflict_generator():
            raise api.ApiCallException(requests.codes.BAD_REQUEST, "unused")
            yield  # Empty yield to make this a generator

        return_value = not_conflict_generator()

        ghapi = mock.MagicMock()
        ghapi.get_repository_commits = mock.MagicMock(
            return_value=return_value
        )

        with pytest.raises(api.ApiCallException):
            analytics.get_repository_commit_emails(ghapi, "unused", "unused")


if __name__ == "__main__":
    unittest.main()
