import logging
import os
import sys

import invoke
from alembic.command import revision, upgrade
from alembic.config import Config

from src.settings.defaults import DB_URL, PROJECT_DIR

logging.getLogger("invoke").setLevel(logging.CRITICAL)


@invoke.task
def tests(ctx):
    cmd = f"PYTHONPATH=src/ {sys.executable} -m pytest"
    ctx.run(cmd, shell="/bin/sh", pty=True)


@invoke.task
def lint(ctx):
    cmd = (
        "black . --exclude env.py && "
        "isort -rc . --skip env.py && "
        "autoflake -r --in-place --remove-unused-variables . && "
        "flake8"
    )
    ctx.run(cmd, shell="/bin/sh", pty=True)


@invoke.task
def migratecreate(ctx):
    os.chdir("src")
    apps = [directory for directory in os.listdir(".") if os.path.isdir(directory)]
    for app in apps:
        if not os.path.isdir(f"{app}/migrations"):
            continue
        os.chdir(f"{app}")
        current_dir = os.getcwd()
        config = Config(file_=os.path.join(PROJECT_DIR, "alembic.ini"))
        config.set_main_option("script_location", f"{current_dir}/migrations")
        config.set_main_option("sqlalchemy.url", DB_URL)
        revision(config, autogenerate=True)


@invoke.task
def migraterun(ctx):
    os.chdir("src")
    apps = [directory for directory in os.listdir(".") if os.path.isdir(directory)]
    for app in apps:
        if not os.path.isdir(f"{app}/migrations"):
            continue
        os.chdir(f"{app}")
        current_dir = os.getcwd()
        config = Config(file_=os.path.join(PROJECT_DIR, "alembic.ini"))
        config.set_main_option("script_location", f"{current_dir}/migrations")
        config.set_main_option("sqlalchemy.url", DB_URL)
        upgrade(config, "head")
