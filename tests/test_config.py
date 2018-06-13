import os
from typing import NamedTuple
from unittest.mock import patch

import pytest

from env_var_config import gather_config_for_class, MissingEnvironmentVariableError


class SampleAppConfig(NamedTuple):
    some_string: str
    some_int: int
    some_float: float
    true_bool: bool
    false_bool: bool
    other_false_bool: bool
    field_with_a_default: int = 13


@pytest.fixture
def env_with_config():
    return {
        'SOME_STRING': "hey! I'm a string!",
        'SOME_INT': '666',
        'SOME_FLOAT': '2.25',
        'TRUE_BOOL': 'True',
        'FALSE_BOOL': 'False',
        'OTHER_FALSE_BOOL': 'xccjkhd',
        'FIELD_WITH_A_DEFAULT': '35',
    }


def test_get_config_from_environment_variables(env_with_config):
    with patch.dict(os.environ, env_with_config):
        app_config = gather_config_for_class(SampleAppConfig)

    assert app_config.some_string == env_with_config['SOME_STRING']
    assert app_config.some_int == 666
    assert app_config.some_float == 2.25
    assert app_config.true_bool
    assert not app_config.false_bool
    assert not app_config.other_false_bool


def test_get_config_from_a_dictionary(env_with_config):
    app_config = gather_config_for_class(SampleAppConfig, env=env_with_config)
    assert app_config.some_int == 666


def test_get_config_with_missing_environment_variables():
    with pytest.raises(MissingEnvironmentVariableError):
        gather_config_for_class(SampleAppConfig)


def test_get_config_with_missing_env_variables_allowing_empty():
    app_config = gather_config_for_class(SampleAppConfig, allow_empty=True)

    assert app_config.some_int == 0
    assert app_config.some_string == ''
    assert app_config.some_float == 0.0
    assert not app_config.true_bool
    assert not app_config.false_bool
    assert not app_config.other_false_bool
    assert app_config.field_with_a_default == 13


def test_get_config_with_non_set_value_with_a_default_and_not_allowing_empty():
    fake_env = {
        'SOME_STRING': "hey! I'm a string!",
        'SOME_INT': '666',
        'SOME_FLOAT': '2.25',
        'TRUE_BOOL': 'True',
        'FALSE_BOOL': 'False',
        'OTHER_FALSE_BOOL': 'xccjkhd',
    }
    with patch.dict(os.environ, fake_env):
        app_config = gather_config_for_class(SampleAppConfig, allow_empty=False)

    assert app_config.some_int == 666
    assert app_config.field_with_a_default == 13
