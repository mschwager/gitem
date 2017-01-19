#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import functools
import multiprocessing
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gitem import api
from gitem import analytics

CONCISE_COUNT = 5


def leftpad_print(s, leftpad_length=0):
    print(" " * leftpad_length + s)


def organization(ghapi, *args, **kwargs):
    organization = kwargs['name']
    verbose = kwargs['verbose']

    organization_info = analytics.get_organization_information(
        ghapi,
        organization
    )
    organization_repositories = analytics.get_organization_repositories(
        ghapi,
        organization
    )
    organization_members = analytics.get_organization_members(
        ghapi,
        organization
    )

    for human_readable_name, api_info in organization_info.items():
        leftpad_print(
            "{}: {}".format(human_readable_name, api_info),
            leftpad_length=0
        )

    leftpad_print("Public Members:", leftpad_length=0)

    def member_administrator(member):
        return member['Site Administrator']

    members = sorted(
        organization_members,
        key=member_administrator,
        reverse=True
    )

    member_count = len(organization_members) if verbose else CONCISE_COUNT
    members = members[:member_count]

    for member in members:
        for human_readable_name, api_info in member.items():
            leftpad_print(
                "{}: {}".format(human_readable_name, api_info),
                leftpad_length=2
            )

        leftpad_print("", leftpad_length=0)

    leftpad_print("Public Repositories:", leftpad_length=0)

    def repository_popularity(repository):
        return (
            int(repository['Watchers']) +
            int(repository['Stars']) +
            int(repository['Forks'])
        )

    repositories = sorted(
        organization_repositories,
        key=repository_popularity,
        reverse=True
    )
    repository_count = len(organization_repositories) if verbose else CONCISE_COUNT
    repositories = repositories[:repository_count]

    for repository in repositories:
        for human_readable_name, api_info in repository.items():
            leftpad_print(
                "{}: {}".format(human_readable_name, api_info),
                leftpad_length=2
            )

        leftpad_print("", leftpad_length=0)


def repository(ghapi, *args, **kwargs):
    repository = kwargs['name']
    owner = kwargs['owner']
    verbose = kwargs['verbose']

    repository_info = analytics.get_repository_information(
        ghapi,
        owner,
        repository
    )
    repository_contributors = analytics.get_repository_contributors(
        ghapi,
        owner,
        repository
    )

    for human_readable_name, api_info in repository_info.items():
        leftpad_print(
            "{}: {}".format(human_readable_name, api_info),
            leftpad_length=0
        )

    leftpad_print("Contributors:", leftpad_length=0)

    contributor_count = len(repository_contributors) if verbose else CONCISE_COUNT

    for contributor in repository_contributors[:contributor_count]:
        for human_readable_name, api_info in contributor.items():
            leftpad_print(
                "{}: {}".format(human_readable_name, api_info),
                leftpad_length=2
            )


def user(ghapi, *args, **kwargs):
    username = kwargs['name']
    verbose = kwargs['verbose']
    processes = kwargs['processes']

    user_info = analytics.get_user_information(
        ghapi,
        username
    )
    user_organizations = analytics.get_user_organizations(
        ghapi,
        username
    )
    user_repositories = analytics.get_user_repositories(
        ghapi,
        username
    )

    for human_readable_name, api_info in user_info.items():
        leftpad_print(
            "{}: {}".format(human_readable_name, api_info),
            leftpad_length=0
        )

    leftpad_print("Organizations:", leftpad_length=0)

    organization_count = len(user_organizations) if verbose else CONCISE_COUNT

    for organization in user_organizations[:organization_count]:
        for human_readable_name, api_info in organization.items():
            leftpad_print(
                "{}: {}".format(human_readable_name, api_info),
                leftpad_length=2
            )

    leftpad_print("Repositories:", leftpad_length=0)

    repository_count = len(user_repositories) if verbose else CONCISE_COUNT

    for repository in user_repositories[:repository_count]:
        for human_readable_name, api_info in repository.items():
            leftpad_print(
                "{}: {}".format(human_readable_name, api_info),
                leftpad_length=2
            )

    user_repository_names = [
        repository['Repository Name']
        for repository in user_repositories
    ]

    if processes:
        pool = multiprocessing.Pool(processes=processes)
        partial_email_fn = functools.partial(
            analytics.get_repository_commit_emails,
            ghapi,
            username,
            author=username
        )
        user_repository_emails = pool.map(partial_email_fn, user_repository_names)
    else:
        user_repository_emails = [
            analytics.get_repository_commit_emails(
                ghapi,
                username,
                repository,
                author=username
            )
            for repository in user_repository_names
        ]

    user_emails = functools.reduce(set.union, user_repository_emails, set())

    leftpad_print("Emails:", leftpad_length=0)

    for name, email in user_emails:
        leftpad_print("{}: {}".format(name, email), leftpad_length=2)


def parse_args():
    p = argparse.ArgumentParser(description='''
        A Github organization reconnaissance tool.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument(
        '-o',
        '--oauth2-token',
        action='store',
        help='OAuth2 token for authentcation'
    )
    p.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='verbose output'
    )
    p.add_argument(
        '-p',
        '--processes',
        action='store',
        type=int,
        help='number of processes (for applicable commands)'
    )

    subparsers = p.add_subparsers(dest='command')

    organization = subparsers.add_parser('organization')
    organization.add_argument(
        'name',
        action='store',
        help='Github organization name'
    )

    repository = subparsers.add_parser('repository')
    repository.add_argument(
        'owner',
        action='store',
        help='Github repository owner'
    )
    repository.add_argument(
        'name',
        action='store',
        help='Github repository name'
    )

    user = subparsers.add_parser('user')
    user.add_argument(
        'name',
        action='store',
        help='Github user name'
    )

    args = p.parse_args()

    return args


def main():
    args = parse_args()

    dispatch = {
        "organization": organization,
        "repository": repository,
        "user": user,
    }

    ghapi = api.Api(args.oauth2_token)

    try:
        dispatch[args.command](ghapi, **vars(args))
    except api.ApiCallException as e:
        if e.rate_limiting:
            leftpad_print(
                "Your API requests are being rate-limited. " +
                "Please include an OAuth2 token and read the following:",
                leftpad_length=0
            )
            leftpad_print(e.rate_limiting_url, leftpad_length=0)
        elif e.not_found:
            leftpad_print(
                "The requested resource was not found or private. " +
                "Please confirm that it exists.",
                leftpad_length=0
            )
        else:
            # Re-raise original exception
            raise


if __name__ == "__main__":
    main()
