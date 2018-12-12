#!/usr/bin/env python

import unittest

try:
    # Python 3
    from unittest import mock
except ImportError:
    # Python 2 (third-party)
    import mock

import requests
import pytest

from gitem import api

import mocked_api_results


class TestApi(unittest.TestCase):

    def assertOk(self, status_code):
        assert status_code == requests.codes.OK

    def assertEmpty(self, iterable):
        assert len(iterable) == 0

    @staticmethod
    def api_will_return(json_return_value, status_code=requests.codes.OK, oauth2_token=None):
        assert isinstance(json_return_value, dict)

        return_value = mock.MagicMock()

        return_value.status_code = status_code
        return_value.json = mock.MagicMock(
            return_value=json_return_value
        )
        return_value.ok = status_code == requests.codes.OK

        return api.Api(oauth2_token, requester=mock.MagicMock(
            return_value=return_value
        ))

    @staticmethod
    def paged_api_will_return(json_return_values, status_codes=None, oauth2_token=None):
        assert isinstance(json_return_values, list)
        assert isinstance(status_codes, list) or status_codes is None

        if status_codes is None:
            status_codes = [requests.codes.OK] * len(json_return_values)

        return_value = mock.MagicMock()

        # This is some weird mock black magic...
        type(return_value).status_code = mock.PropertyMock(
            side_effect=status_codes
        )
        return_value.json = mock.Mock(
            side_effect=json_return_values
        )
        type(return_value).ok = mock.PropertyMock(
            side_effect=[
                status_code == requests.codes.OK
                for status_code in status_codes
            ]
        )

        return api.Api(oauth2_token, requester=mock.MagicMock(
            return_value=return_value
        ))

    def test_ok(self):
        will_return = mocked_api_results.STANDARD_API_RESULT

        mocked_api = self.api_will_return(*will_return)

        # The API call we make doesn't matter, it will return the same result
        # no matter what
        result, status_code = mocked_api.get_public_organization("unused")

        expected = mocked_api_results.get_result_value(
            mocked_api_results.STANDARD_API_RESULT
        )

        self.assertOk(status_code)
        assert result == expected

    def test_invalid_json(self):
        will_return = mocked_api_results.INVALID_JSON_RESULT

        mocked_api = self.api_will_return(*will_return)

        # The API call we make doesn't matter, it will return the same result
        # no matter what
        with pytest.raises(api.ApiCallException) as e:
            mocked_api.get_public_organization("unused")

        assert e.value.bad_request

    def test_invalid_json_argument_type(self):
        will_return = mocked_api_results.BAD_JSON_VALUES_RESULT

        mocked_api = self.api_will_return(*will_return)

        # The API call we make doesn't matter, it will return the same result
        # no matter what
        with pytest.raises(api.ApiCallException) as e:
            mocked_api.get_public_organization("unused")

        assert e.value.bad_request

    def test_invalid_json_field(self):
        will_return = mocked_api_results.INVALID_FIELDS_RESULT

        mocked_api = self.api_will_return(*will_return)

        # The API call we make doesn't matter, it will return the same result
        # no matter what
        with pytest.raises(api.ApiCallException) as e:
            mocked_api.get_public_organization("unused")

        assert e.value.unprocessable_entity

    def test_bad_credentials(self):
        will_return = mocked_api_results.BAD_CREDENTIALS_RESULT

        mocked_api = self.api_will_return(*will_return)

        # The API call we make doesn't matter, it will return the same result
        # no matter what
        with pytest.raises(api.ApiCallException) as e:
            mocked_api.get_public_organization("unused")

        assert e.value.unauthorized

    def test_maximum_bad_credentials(self):
        will_return = mocked_api_results.MAXIMUM_BAD_CREDENTIALS_RESULT

        mocked_api = self.api_will_return(*will_return)

        # The API call we make doesn't matter, it will return the same result
        # no matter what
        with pytest.raises(api.ApiCallException) as e:
            mocked_api.get_public_organization("unused")

        assert e.value.forbidden

    def test_not_found(self):
        will_return = mocked_api_results.NOT_FOUND_RESULT

        mocked_api = self.api_will_return(*will_return)

        # The API call we make doesn't matter, it will return the same result
        # no matter what
        with pytest.raises(api.ApiCallException) as e:
            mocked_api.get_public_organization("unused")

        assert e.value.not_found

    def test_authenticated_endpoint_ok(self):
        will_return = mocked_api_results.STANDARD_API_RESULT

        mocked_api = self.api_will_return(
            *will_return,
            oauth2_token="VALUE DOESN'T MATTER"
        )

        result, status_code = mocked_api.get_organization("unused")

        expected = mocked_api_results.get_result_value(
            mocked_api_results.STANDARD_API_RESULT
        )

        self.assertOk(status_code)
        assert result == expected

    def test_authenticated_endpoint_missing_token(self):
        will_return = mocked_api_results.STANDARD_API_RESULT

        mocked_api = self.api_will_return(
            *will_return,
            oauth2_token=None
        )

        with pytest.raises(api.AuthenticationRequiredException):
            mocked_api.get_organization("unused")

    def test_paged_ok(self):
        mocked_json_values = [
            mocked_api_results.get_result_value(result)
            for result in mocked_api_results.PAGED_API_RESULT
        ]

        mocked_status_codes = [
            mocked_api_results.get_result_status_code(result)
            for result in mocked_api_results.PAGED_API_RESULT
        ]

        mocked_api = self.paged_api_will_return(mocked_json_values, mocked_status_codes)

        for result, status_code in mocked_api.get_organizations_public_repositories("unused"):
            expected = mocked_api_results.get_result_value(
                mocked_api_results.STANDARD_API_RESULT
            )

            self.assertOk(status_code)
            assert result == expected

    def test_paged_pep_479(self):
        mocked_json_values = [
            mocked_api_results.get_result_value(result)
            for result in mocked_api_results.PAGED_API_RESULT
        ]
        mocked_json_values = [mocked_json_values[0]]

        mocked_api = self.paged_api_will_return(mocked_json_values)
        mocked_api.requester.return_value.ok = mock.PropertyMock(
            side_effect=StopIteration
        )

        result = list(mocked_api.get_organizations_public_repositories("unused"))

        self.assertEmpty(result)

    def test_get_users_public_repositories_bad_type(self):
        type_ = ""
        ghapi = api.Api()

        with pytest.raises(ValueError):
            ghapi.get_users_public_repositories("UNUSED", type_=type_)

    def test_get_users_public_repositories_bad_sort(self):
        sort = ""
        ghapi = api.Api()

        with pytest.raises(ValueError):
            ghapi.get_users_public_repositories("UNUSED", sort=sort)

    def test_get_users_public_repositories_bad_direction(self):
        direction = ""
        ghapi = api.Api()

        with pytest.raises(ValueError):
            ghapi.get_users_public_repositories("UNUSED", direction=direction)

    def test_get_organizations_public_repositories_bad_type(self):
        type_ = ""
        ghapi = api.Api()

        with pytest.raises(ValueError):
            ghapi.get_organizations_public_repositories("UNUSED", type_=type_)

    def test_get_repository_contributors_bad_anon(self):
        anon = ""
        ghapi = api.Api()

        with pytest.raises(ValueError):
            ghapi.get_repository_contributors("UNUSED", "UNUSED", anon=anon)

    def test_get_repository_contributors_ok(self):
        mocked_json_values = [
            mocked_api_results.get_result_value(result)
            for result in mocked_api_results.PAGED_API_RESULT
        ]

        mocked_status_codes = [
            mocked_api_results.get_result_status_code(result)
            for result in mocked_api_results.PAGED_API_RESULT
        ]

        mocked_api = self.paged_api_will_return(mocked_json_values, mocked_status_codes)

        for result, status_code in mocked_api.get_repository_contributors("unused", "unused"):
            expected = mocked_api_results.get_result_value(
                mocked_api_results.STANDARD_API_RESULT
            )

            self.assertOk(status_code)
            assert result == expected


if __name__ == "__main__":
    unittest.main()
