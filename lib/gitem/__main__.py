#!/usr/bin/env python

import argparse
import pprint

from gitem import analytics


def organization(*args, **kwargs):
    pprint.pprint(
        analytics.get_organization_information(kwargs['organization'])
    )


def repository(*args, **kwargs):
    pass


def user(*args, **kwargs):
    pass


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

    subparsers = p.add_subparsers(dest='command')

    organization = subparsers.add_parser('organization')
    organization.add_argument(
        'organization',
        action='store',
        help='Github organization name'
    )

    repository = subparsers.add_parser('repository')
    repository.add_argument(
        'repository',
        action='store',
        help='Github repository name'
    )

    user = subparsers.add_parser('user')
    user.add_argument(
        'user',
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

    dispatch[args.command](**vars(args))

if __name__ == "__main__":
    main()
