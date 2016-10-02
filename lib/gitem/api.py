#!/usr/bin/env python

import functools
import json

import requests


class AuthenticationRequiredException(BaseException):
    pass


class ApiCallException(BaseException):

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
    def conflict(self):
        return self.code == requests.codes.CONFLICT

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

        # https://developer.github.com/v3/media/#request-specific-version
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }

    def call(self, method, url, params=None):
        """
        Make a Github developer API call
        """
        if params is None:
            params = {}

        if self.oauth2_token:
            params["access_token"] = self.oauth2_token

        response = self.requester(method, url, params=params, headers=self.headers)

        if not response.ok:
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

    def get_user(self, username):
        """
        Return user information associated with a given username

        https://developer.github.com/v3/users/#get-a-single-user
        """
        method = "GET"
        endpoint = "/users/{}".format(username)
        params = {}

        result = self.json_call(method, endpoint, params)

        return result

    @oauth2_required
    def get_users_organizations(self):
        """
        Return organizations associated with an OAuth2 authenticated user

        https://developer.github.com/v3/orgs/#list-your-organizations
        """
        method = "GET"
        endpoint = "/user/orgs"
        params = {}

        result = self.json_call(method, endpoint, params)

        return result

    def get_users_public_organizations(self, username):
        """
        Return public organizations associated with a user

        https://developer.github.com/v3/orgs/#list-user-organizations
        """
        method = "GET"
        endpoint = "/users/{}/orgs".format(username)
        params = {}

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_users_public_repositories(self, username, type=None, sort=None, direction=None):
        """
        Return public repositories associated with a given user

        https://developer.github.com/v3/repos/#list-user-repositories
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

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_public_organization(self, organization):
        """
        Return public information associated with an organization

        https://developer.github.com/v3/orgs/#get-an-organization
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

        https://developer.github.com/v3/orgs/#get-an-organization
        """
        return self.get_public_organization(organization)

    def get_organizations_public_repositories(self, organization, type=None):
        """
        Return public repositories associated with a given organization

        https://developer.github.com/v3/repos/#list-organization-repositories
        """
        assert type in ["all", "public", "private", "forks", "sources", "member", None]

        method = "GET"
        endpoint = "/orgs/{}/repos".format(organization)
        params = {}

        if type:
            params["type"] = type

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_organizations_public_members(self, organization):
        """
        Return public members associated with a given organization

        https://developer.github.com/v3/orgs/members/
        """
        method = "GET"
        endpoint = "/orgs/{}/public_members".format(organization)
        params = {}

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_public_repository(self, owner, repository):
        """
        Return public information associated with a repository

        https://developer.github.com/v3/repos/#get
        """
        method = "GET"
        endpoint = "/repos/{}/{}".format(owner, repository)
        params = {}

        result = self.json_call(method, endpoint, params)

        return result

    def get_repository_contributors(self, owner, repository, anon=None):
        """
        Return contributor information associated with a given repository

        https://developer.github.com/v3/repos/#list-contributors
        """
        assert anon in [1, "true", None]

        method = "GET"
        endpoint = "/repos/{}/{}/contributors".format(owner, repository)
        params = {}

        if anon:
            params["anon"] = anon

        result = self.paginated_json_call(method, endpoint, params)

        return result

    def get_repository_commits(self, owner, repository, sha=None, path=None,
                               author=None, since=None, until=None):
        """
        Return commit information associated with a given repository
        """
        method = "GET"
        endpoint = "/repos/{}/{}/commits".format(owner, repository)
        params = {}

        if sha:
            params["sha"] = sha
        if path:
            params["path"] = path
        if author:
            params["author"] = author
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        result = self.paginated_json_call(method, endpoint, params)

        return result
