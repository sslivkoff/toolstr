"""functions related to python str templates"""
from __future__ import annotations

import typing


def get_template_keys(template: str) -> typing.Mapping[str, str | None]:
    keys = {}
    temp = template
    while '{' in temp:
        start_index = temp.index('{')
        end_index = temp.index('}')
        keypattern = temp[slice(start_index, end_index + 1)]
        if ':' in keypattern:
            name, pattern = keypattern[1:-1].split(':')
        else:
            name = keypattern[1:-1]
            pattern = None
        keys[name] = pattern
        temp = temp[end_index + 1 :]

    return keys


def template_to_regex(template: str) -> str:
    regex = template
    for key, pattern in get_template_keys(template).items():
        # reconstruct template key
        if pattern is None:
            replace = '{' + key + '}'
        else:
            replace = '{' + key + ':' + pattern + '}'

        # create regex group
        regex_pattern = '[a-zA-Z0-9_]+'
        group = '(?P<' + key + '>' + regex_pattern + ')'

        # replace template key with regex group
        regex = regex.replace(replace, group)

    return regex


#
# # template parsing
#


def parse_by_template(target: str, template: str) -> typing.Mapping[str, str]:
    """parse str according to template"""
    import re

    regex = template_to_regex(template)
    match = re.search(regex, target)
    if match is None:
        raise Exception('str does not fit template')
    else:
        return match.groupdict()


def parse_strs_by_template(
    strs: typing.Sequence[str],
    template: str,
    *,
    unique: bool = False,
) -> typing.Mapping[str, typing.Sequence[str]]:
    """parse strs according to template"""
    parsed: dict[str, list[str]] = {}
    for s in strs:
        for k, v in parse_by_template(s, template).items():
            if k not in parsed:
                parsed[k] = []
            if unique and v in parsed[k]:
                continue
            parsed[k].append(v)
    return parsed


def parse_aggregate_by_template(
    strs: typing.Sequence[str],
    template: str,
    aggregations: typing.Mapping[str, str],
) -> typing.Mapping[str, str]:
    """parse strs according to template, returning single value per key

    keys with multiple values should have aggregation specified
    """
    parse_values = parse_strs_by_template(
        strs=strs,
        template=template,
        unique=True,
    )
    output = {}
    for key, value in parse_values.items():
        if key in aggregations:
            output[key] = _get_str_aggregation(value, aggregations[key])
        elif len(value) == 1:
            output[key] = next(iter(value))
        else:
            raise Exception(
                'multiple values for key, need to aggregate: ' + str(key)
            )
    return output


def _get_str_aggregation(strs: typing.Sequence[str], aggregation: str) -> str:
    if aggregation == 'max':
        return max((float(value), value) for value in strs)[1]
    elif aggregation == 'min':
        return min((float(value), value) for value in strs)[1]
    else:
        raise Exception('invalid aggregation: ' + str(aggregation))

