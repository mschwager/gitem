#!/usr/bin/env python

import functools
import json

import requests


class AuthenticationRequiredException(Exception):
    pass


class ApiCallException(Exception):

    rate_limiting_url = 'https://developer.github.com/v3/#rate-limiting'

    def __init__(self, code, message):
        self.code = code
        self.message = message

    @property
    def bad_request(self):
        return self.code == requests.codes.BAD_REQUEST

    @property
    def unprocessable_entity(self):
        return self.code == requests.codes.UNPROCESSABLE_ENTITY

    @property
    def forbidden(self):
        return self.code == requests.codes.FORBIDDEN

    @property
    def unauthorized(self):
        return self.code == requests.codes.UNAUTHORIZED

    @property
    def rate_limiting(self):
        return (
            self.forbidden and
            self.message.get('documentation_url') == self.rate_limiting_url
        )

    def __str__(self):
        return "{}: {}".format(self.code, json.dumps(self.message))


def oauth2_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args or getattr(args[0], "oauth2_token", None) is None:
            raise AuthenticationRequiredException("Please include an OAuth2 token.")
        return func(*args, **kwargs)
    return wrapper


class Api(object):

    BASE_URL = "https://api.github.com"

    def __init__(self, oauth2_token=None, requester=requests.request):
        self.oauth2_token = oauth2_token
        self.requester = requester

    def call(self, method, url, params=None):
        """
        Make a Github developer API call
        """
        if params is None:
            params = {}

        if self.oauth2_token:
            params["access_token"] = self.oauth2_token

        response = self.requester(method, url, params=params)

        if response.status_code != requests.codes.OK:
            raise ApiCallException(response.status_code, response.json())

        return response

    def json_call(self, method, endpoint, params=None):
        """
        Return JSON data from a Github developer API call
        """
        if params is None:
            params = {}

        url = self.BASE_URL + endpoint
        response = self.call(method, url, params)

        return (response.json(), response.status_code)

    def paginated_json_call(self, method, endpoint, params=None):
        """
        Return paginated JSON data from a Github developer API call
        """
        if params is None:
            params = {}

        url = self.BASE_URL + endpoint

        next_link = True
        while next_link:
            response = self.call(method, url, params)
            yield (response.json(), response.status_code)
            next_link = response.links.get("next", {})
            url = next_link.get("url")

    @oauth2_required
    def get_users_organizations(self):
        """
        Return organizations associated with an OAuth2 authenticated user
        """
        method = "GET"
        endpoint = "/user/orgs"
        params = {}

        result = self.json_call(method, endpoint, params)

        return result

    def get_users_public_organizations(self, username):
        """
        Return public organizations associated with a user
        """
        method = "GET"
        endpoint = "/users/{}/orgs".format(username)
        params = {}

        result = self.json_call(method, endpoint, params)

        return result

    def get_users_public_repositories(self, username, type=None, sort=None, direction=None):
        """
        Return public repositories associated with a given user
        """
        assert type in ["all", "owner", "member", None]
        assert sort in ["created", "updated", "pushed", "full_name", None]
        assert direction in ["asc", "desc", None]

        method = "GET"
        endpoint = "/users/{}/repos".format(username)
        params = {}

        if type:
            params["type"] = type
        if sort:
            params["sort"] = sort
        if direction:
            params["direction"] = direction

        result = self.json_call(method, endpoint, params)

        return result

    def get_public_organization(self, organization):
        """
        Return public information associated with an organization
        """
        method = "GET"
        endpoint = "/orgs/{}".format(organization)
        params = {}

        result = self.json_call(method, endpoint, params)

        return result

    @oauth2_required
    def get_organization(self, organization):
        """
        Return information associated with an organization, OAuth2
        authenticated user must be an owner
        """
        return self.get_public_organization(organization)

    def get_organizations_public_repositories(self, organization, type=None):
        """
        Return public repositories associated with a given organization
        """
        assert type in ["all", "owner", "member", None]

        method = "GET"
        endpoint = "/orgs/{}/repos".format(organization)
        params = {}

        if type:
            params["type"] = type

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_organizations_public_members(self, organization, filter=None, role=None):
        """
        Return public members associated with a given organization
        """
        assert filter in ["2fa_disabled", "all", None]
        assert role in ["all", "admin", "member", None]

        method = "GET"
        endpoint = "/orgs/{}/members".format(organization)
        params = {}

        if filter:
            params["filter"] = filter
        if role:
            params["role"] = role

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_repository_contributors(self, owner, repository, anon=None):
        """
        Return contributor information associated with a given repository
        """
        assert anon in [1, "true", None]

        method = "GET"
        endpoint = "/repos/{}/{}/contributors".format(owner, repository)
        params = {}

        if anon:
            params["anon"] = anon

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_repository_contributors_stats(self, owner, repository):
        """
        Return contributor stats information associated with a given repository
        """
        method = "GET"
        endpoint = "/repos/{}/{}/stats/contributors".format(owner, repository)
        params = {}

        result = self.json_call(method, endpoint, params)

        return result
