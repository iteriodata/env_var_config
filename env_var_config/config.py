"""
Everything related to getting the application's configuration.
"""

import os
import typing
from typing import List


class MissingEnvironmentVariableError(Exception):
    """When an environment variable needed by the app's configuration is missing."""


NOT_SET = object()


def gather_config_for_class(
        class_: type,
        allow_empty: bool = False,
        env: dict = NOT_SET):
    """Gathers the configuration values from environment variables and returns them as an object
    of the passed class.

    Args:
        class_: Class inheriting from :class:`NamedTuple` that has type hint (only simple types)
            on every field.
        allow_empty: If True, then this won't crash when values for some config parameters
            are missing.
        env: Dict-like thing containing the environment variables we'll base the config on.
            Defaults to the variables from the real environment, but another set of variables
            can be passed.
    """
    if env is NOT_SET:
        env = os.environ

    tuple_fields = _get_tuple_fields(class_)
    fields_to_values = {}
    for config_field in tuple_fields:
        fields_to_values[config_field.name] = _get_value_from_env(
            config_field,
            allow_empty,
            env,
        )
    return class_(**fields_to_values)


class _Field(typing.NamedTuple):
    name: str
    type_: type
    default: object = NOT_SET


def _get_tuple_fields(tuple_class) -> List[_Field]:
    # The "protected access" warnings disabled for Pylint here, because it's not actually
    # protected, accessing protected fields. They are just special fields
    # on the typing.NamedTuple.
    tuple_fields = []
    for field_name, field_type in tuple_class._field_types.items(): # pylint: disable=protected-access
        tuple_fields.append(
            _Field(
                name=field_name,
                type_=field_type,
                default=tuple_class._field_defaults.get(field_name, NOT_SET), # pylint: disable=protected-access
            )
        )
    return tuple_fields


def _get_value_from_env(
        config_field: _Field,
        allow_empty: bool,
        env: dict):
    """Gets a typed value for the configuration field from the environment variables.
    """
    value_type = config_field.type_
    env_variable_name = config_field.name.upper()
    try:
        str_value = env[env_variable_name]
    except KeyError as ex:
        if config_field.default is not NOT_SET:
            return config_field.default
        elif allow_empty:
            return value_type()
        else:
            message = f'Missing environment variable: {env_variable_name}'
            raise MissingEnvironmentVariableError(message) from ex

    if value_type == bool:
        return _conf_string_to_bool(str_value)
    return value_type(str_value)


def _conf_string_to_bool(conf_string: str):
    """Normally in Python all non empty strings convert to True.
    We want it to not be as easy to accidentally turn on a configuration flag, so we only treat
    the explicit string "true" as True. Casing doesn't matter.
    """
    return conf_string.lower() == 'true'
