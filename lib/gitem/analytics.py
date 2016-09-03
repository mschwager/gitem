#!/usr/bin/env python

from gitem import api


def get_organization_information(organization):
    ghapi = api.Api()
    return ghapi.get_public_organization(organization)
