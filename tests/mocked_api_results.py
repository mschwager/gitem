#!/usr/bin/env python

import requests

STANDARD_API_RESULT = [
    {
        "api results": "go here",
    },
    requests.codes.OK,
]

PAGED_API_RESULT = [
    STANDARD_API_RESULT,
    STANDARD_API_RESULT,
    STANDARD_API_RESULT,
]

INVALID_JSON_RESULT = [
    {
        "message": "Problems parsing JSON",
    },
    requests.codes.BAD_REQUEST,
]

BAD_JSON_VALUES_RESULT = [
    {
        "message": "Body should be a JSON object",
    },
    requests.codes.BAD_REQUEST,
]

INVALID_FIELDS_RESULT = [
    {
        "message": "Validation Failed",
        "errors": [
            {
                "resource": "Issue",
                "field": "title",
                "code": "missing_field",
            }
        ],
    },
    requests.codes.UNPROCESSABLE_ENTITY,
]

BAD_CREDENTIALS_RESULT = [
    {
        "message": "Bad credentials",
        "documentation_url": "https://developer.github.com/v3",
    },
    requests.codes.UNAUTHORIZED,
]

MAXIMUM_BAD_CREDENTIALS_RESULT = [
    {
        "message": "Maximum number of login attempts exceeded. Please try again later.",
        "documentation_url": "https://developer.github.com/v3",
    },
    requests.codes.FORBIDDEN,
]

NOT_FOUND_RESULT = [
    {
        "message": "Not Found",
        "documentation_url": "https://developer.github.com/v3",
    },
    requests.codes.NOT_FOUND,
]


def get_result_value(result):
    return result[0]


def get_result_status_code(result):
    return result[1]
