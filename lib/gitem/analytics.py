#!/usr/bin/env python

import collections


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
