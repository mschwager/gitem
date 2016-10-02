#!/usr/bin/env python

import collections

from . import api


def get_organization_information(ghapi, organization):
    organization_info, _ = ghapi.get_public_organization(
        organization
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('name', 'Organization Name'),
        ('description', 'Description'),
        ('blog', 'Website'),
        ('html_url', 'Github URL'),
        ('created_at', 'Created'),
        ('updated_at', 'Last Updated'),
        ('email', 'Email Address'),
        ('location', 'Location'),
        ('login', 'Username'),
        ('public_repos', '# of Public Repositories'),
    ])

    human_readable_name_to_api_info = {
        human_readable_name: organization_info[api_name]
        for api_name, human_readable_name in api_name_to_human_readable_name.items()
    }

    return human_readable_name_to_api_info


def get_organization_repositories(ghapi, organization):
    paged_organization_repositories = ghapi.get_organizations_public_repositories(
        organization
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('name', 'Repository Name'),
        ('description', 'Description'),
        ('html_url', 'Github URL'),
        ('watchers_count', 'Watchers'),
        ('stargazers_count', 'Stars'),
        ('forks_count', 'Forks'),
        ('created_at', 'Created'),
        ('updated_at', 'Last Updated'),
        ('pushed_at', 'Last Pushed'),

    ])

    human_readable_name_to_api_info = [
        {
            human_readable_name: organization_repository[api_name]
            for api_name, human_readable_name in api_name_to_human_readable_name.items()
        }
        for organization_repositories, _ in paged_organization_repositories
        for organization_repository in organization_repositories
    ]

    return human_readable_name_to_api_info


def get_organization_members(ghapi, organization):
    paged_organization_members = ghapi.get_organizations_public_members(
        organization
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('login', 'Username'),
        ('site_admin', 'Site Administrator'),
        ('html_url', 'Github URL'),
    ])

    human_readable_name_to_api_info = [
        {
            human_readable_name: organization_member[api_name]
            for api_name, human_readable_name in api_name_to_human_readable_name.items()
        }
        for organization_members, _ in paged_organization_members
        for organization_member in organization_members
    ]

    return human_readable_name_to_api_info


def get_repository_information(ghapi, owner, repository):
    repository_info, _ = ghapi.get_public_repository(
        owner,
        repository
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('name', 'Repository Name'),
        ('description', 'Description'),
        ('homepage', 'Homepage'),
        ('html_url', 'Github URL'),
        ('created_at', 'Created'),
        ('updated_at', 'Last Updated'),
        ('pushed_at', 'Last Pushed'),
        ('language', 'Language'),
        ('forks_count', 'Forks'),
        ('stargazers_count', 'Stars'),
        ('watchers_count', 'Watchers'),
    ])

    human_readable_name_to_api_info = {
        human_readable_name: repository_info[api_name]
        for api_name, human_readable_name in api_name_to_human_readable_name.items()
    }

    return human_readable_name_to_api_info


def get_repository_contributors(ghapi, owner, repository):
    paged_repository_contributors = ghapi.get_repository_contributors(
        owner,
        repository
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('login', 'Username'),
        ('contributions', 'Contributions'),
    ])

    human_readable_name_to_api_info = [
        {
            human_readable_name: repository_contributor[api_name]
            for api_name, human_readable_name in api_name_to_human_readable_name.items()
        }
        for repository_contributors, _ in paged_repository_contributors
        for repository_contributor in repository_contributors
    ]

    return human_readable_name_to_api_info


def get_user_information(ghapi, username):
    user_info, _ = ghapi.get_user(
        username
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('login', 'Username'),
        ('html_url', 'Github URL'),
        ('name', 'Name'),
        ('company', 'Company'),
        ('blog', 'Blog'),
        ('location', 'Location'),
        ('email', 'Email Address'),
        ('created_at', 'Created'),
        ('updated_at', 'Updated'),
    ])

    human_readable_name_to_api_info = {
        human_readable_name: user_info[api_name]
        for api_name, human_readable_name in api_name_to_human_readable_name.items()
    }

    return human_readable_name_to_api_info


def get_user_organizations(ghapi, username):
    paged_user_organizations = ghapi.get_users_public_organizations(
        username
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('login', 'Organization'),
    ])

    human_readable_name_to_api_info = [
        {
            human_readable_name: user_organization[api_name]
            for api_name, human_readable_name in api_name_to_human_readable_name.items()
        }
        for user_organizations, _ in paged_user_organizations
        for user_organization in user_organizations
    ]

    return human_readable_name_to_api_info


def get_user_repositories(ghapi, username):
    # TODO: Change this back to type='all' and find a good way to grab
    # the correct repository owners
    paged_user_repositories = ghapi.get_users_public_repositories(
        username,
        type='owner',
        sort='pushed',
        direction='desc',
    )

    # Order it so we get the same keys first every time
    api_name_to_human_readable_name = collections.OrderedDict([
        ('name', 'Repository Name'),
        ('description', 'Description'),
        ('html_url', 'Github URL'),
    ])

    human_readable_name_to_api_info = [
        {
            human_readable_name: user_repository[api_name]
            for api_name, human_readable_name in api_name_to_human_readable_name.items()
        }
        for user_repositories, _ in paged_user_repositories
        for user_repository in user_repositories
    ]

    return human_readable_name_to_api_info


def get_repository_commit_emails(ghapi, owner, repository, author=None):
    paged_repository_commits = ghapi.get_repository_commits(
        owner,
        repository,
        author=author
    )

    # https://developer.github.com/v3/git/
    def get_commits_or_empty(repository_commits):
        try:
            for repository_commit in repository_commits:
                yield repository_commit
        except api.ApiCallException as e:
            if e.conflict:
                yield ([], None)
            else:
                # Re-raise original exception
                raise

    repository_commit_emails = {
        (
            repository_commit['commit']['author']['name'],
            repository_commit['commit']['author']['email'],
        )
        for repository_commits, _ in get_commits_or_empty(paged_repository_commits)
        for repository_commit in repository_commits
    }

    return repository_commit_emails
