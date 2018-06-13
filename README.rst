env_var_config
==============

This project allows you to describe the configuration of your application as a
``typing.NamedTuple``, like so:

.. code-block:: python

    import typing

    class MyAppConfig(typing.NamedTuple):
        some_string: str
        some_int: int
        some_float: float
        some_bool: bool = True

Then, gather the configuration from the environment variables:

.. code-block:: python

    import env_var_config

    config = env_var_config.gather_config_for_class(MyAppConfig)

The code will look for variables that are called like the fields of the tuple, but uppercase.

As you might have noticed, you can set default values on the fields.
If the fields with defaults are not found in the environment, they're set to their default value
(which is quite unsurprising).
If a value without a default is missing, though, an error will be raised.
That is, unless you set ``allow_empty`` option to ``True``
in the call to ``gather_config_for_class``.
Then all missing values will be initialized with the default value for their type,
such as an empty string for ``str``, 0 for ``int``, etc.

Installation
------------

.. code-block:: bash

    pip install env_var_config
