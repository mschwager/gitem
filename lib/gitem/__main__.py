#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import argparse
import collections
import functools
import multiprocessing

from . import api
from . import analytics
from . import output

CONCISE_COUNT = 5


def organization(ghapi, outputter, *args, **kwargs):
    organization = kwargs['name']
    verbose = kwargs['verbose']

    organization_info = analytics.get_organization_information(
        ghapi,
        organization
    )

    outputter.output(organization_info)

    organization_members = analytics.get_organization_members(
        ghapi,
        organization
    )

    def member_administrator(member):
        return member['Site Administrator']

    members = sorted(
        organization_members,
        key=member_administrator,
        reverse=True
    )

    member_count = len(members) if verbose else CONCISE_COUNT
    outputter.output(collections.OrderedDict([
        ("Public Members", collections.OrderedDict([
            (member["Username"], collections.OrderedDict([
                (human_readable_name, api_info)
                for human_readable_name, api_info in member.items()
            ]))
            for member in members[:member_count]
        ]))
    ]))

    organization_repositories = analytics.get_organization_repositories(
        ghapi,
        organization
    )

    def repository_popularity(repository):
        return (
            int(repository['Watchers'])
            + int(repository['Stars'])
            + int(repository['Forks'])
        )

    repositories = sorted(
        organization_repositories,
        key=repository_popularity,
        reverse=True
    )

    repository_count = len(repositories) if verbose else CONCISE_COUNT
    outputter.output(collections.OrderedDict([
        ("Public Repositories", collections.OrderedDict([
            (repository["Repository Name"], collections.OrderedDict([
                (human_readable_name, api_info)
                for human_readable_name, api_info in repository.items()
            ]))
            for repository in repositories[:repository_count]
        ]))
    ]))


def repository(ghapi, outputter, *args, **kwargs):
    repository = kwargs['name']
    owner = kwargs['owner']
    verbose = kwargs['verbose']

    repository_info = analytics.get_repository_information(
        ghapi,
        owner,
        repository
    )

    outputter.output(repository_info)

    repository_contributors = analytics.get_repository_contributors(
        ghapi,
        owner,
        repository
    )

    contributor_count = len(repository_contributors) if verbose else CONCISE_COUNT
    outputter.output(collections.OrderedDict([
        ("Contributors", collections.OrderedDict([
            (contributor["Username"], collections.OrderedDict([
                (human_readable_name, api_info)
                for human_readable_name, api_info in contributor.items()
            ]))
            for contributor in repository_contributors[:contributor_count]
        ]))
    ]))


def user(ghapi, outputter, *args, **kwargs):
    username = kwargs['name']
    verbose = kwargs['verbose']
    processes = kwargs['processes']

    user_info = analytics.get_user_information(
        ghapi,
        username
    )

    outputter.output(user_info)

    user_organizations = analytics.get_user_organizations(
        ghapi,
        username
    )

    organization_count = len(user_organizations) if verbose else CONCISE_COUNT
    outputter.output(collections.OrderedDict([
        ("Organizations", collections.OrderedDict([
            (organization["Organization"], collections.OrderedDict([
                (human_readable_name, api_info)
                for human_readable_name, api_info in organization.items()
            ]))
            for organization in user_organizations[:organization_count]
        ]))
    ]))

    user_repositories = analytics.get_user_repositories(
        ghapi,
        username
    )

    repository_count = len(user_repositories) if verbose else CONCISE_COUNT
    outputter.output(collections.OrderedDict([
        ("Repositories", collections.OrderedDict([
            (repository["Repository Name"], collections.OrderedDict([
                (human_readable_name, api_info)
                for human_readable_name, api_info in repository.items()
            ]))
            for repository in user_repositories[:repository_count]
        ]))
    ]))

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

    outputter.output(collections.OrderedDict([
        ("Emails", [
            str((name, email))
            for name, email in user_emails
        ]),
    ]))


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
    p.add_argument(
        '-t',
        '--output',
        action='store',
        choices=[
            output.Stdout.name,
            output.Json.name,
        ],
        default=output.Stdout.name,
        help='show results in this format'
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

    outputters = {
        output.Stdout.name: output.Stdout,
        output.Json.name: output.Json,
    }
    outputter = outputters[args.output]()

    try:
        dispatch[args.command](ghapi, outputter, **vars(args))
    except api.ApiCallException as e:
        if e.rate_limiting:
            outputter.output({
                "Error": (
                    "Your API requests are being rate-limited. "
                    + "Please include an OAuth2 token and read the following:"
                )
            })
            outputter.output({
                "Rate Limiting": e.rate_limiting_url
            })
        elif e.not_found:
            outputter.output({
                "Error": (
                    "The requested resource was not found or private. "
                    + "Please confirm that it exists."
                )
            })
        else:
            # Re-raise original exception
            raise


if __name__ == "__main__":
    main()
