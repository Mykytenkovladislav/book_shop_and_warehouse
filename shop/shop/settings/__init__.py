"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
To change settings file:
`DJANGO_ENV=prod python manage.py runserver`
"""

from split_settings.tools import optional, include
from pathlib import PurePath
import environ

# https://github.com/joke2k/django-environ
env_file = PurePath(__file__).parent.parent.parent.parent.joinpath("config", ".env")
environ.Env.read_env(env_file=env_file.as_posix())
env = environ.Env(DJANGO_DEBUG=bool)

ENVIRONMENT = env("DJANGO_ENV")

base_settings = [
    "components/base.py",  # standard django settings
    "components/database.py",  # databases
    "components/static.py",
    "components/rest.py",
    "components/email.py",

    # Select the right env:
    "environments/%s.py" % ENVIRONMENT,

    # Optionally override some settings:
    optional("environments/local.py"),
]

# Include settings:
include(*base_settings)
