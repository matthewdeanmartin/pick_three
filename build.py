# coding=utf-8
"""
Just enough build script tech to make it work.
"""
from pyntcontrib import *

PROJECT_NAME = "pick_three"
SRC = ''
PYTHON = "python3.6"
IS_DJANGO = False
PIPENV = "pipenv run "

from semantic_version import Version

import os

from checksumdir import dirhash

CURRENT_HASH = None


# bash to find what has change recently
# find src/ -type f -print0 | xargs -0 stat -f "%m %N" | sort -rn | head -10 | cut -f2- -d" "
class BuildState(object):
    def __init__(self, what, where):
        self.what = what
        self.where = where
        if not os.path.exists(".build_state"):
            os.makedirs(".build_state")
        self.state_file_name = ".build_state/last_change_{0}.txt".format(what)

    def oh_never_mind(self):
        """
        If a task fails, we don't care if it didn't change since last, re-run,
        :return:
        """
        os.remove(self.state_file_name)

    def has_source_code_tree_changed(self):
        """
        If a task succeeds & is re-run and didn't change, we might not
        want to re-run it if it depends *only* on source code
        :return:
        """
        global CURRENT_HASH
        directory = self.where

        if CURRENT_HASH is None:
            CURRENT_HASH = dirhash(directory, 'md5', excluded_files="*.pyc")

        if os.path.isfile(self.state_file_name):
            with open(self.state_file_name, "r+") as file:
                last_hash = file.read()
                if last_hash != CURRENT_HASH:
                    file.seek(0)
                    file.write(CURRENT_HASH)
                    file.truncate()
                    return True
        else:
            with open(self.state_file_name, "w") as file:
                file.write(CURRENT_HASH)
                return True
        return False


def oh_never_mind(what):
    state = BuildState(what, PROJECT_NAME)
    state.oh_never_mind()


def has_source_code_tree_changed(what):
    state = BuildState(what, PROJECT_NAME)
    return state.has_source_code_tree_changed()


import functools


def skip_if_no_change(name):
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not has_source_code_tree_changed(name):
                print("Nothing changed, won't re-" + name)
                return
            try:
                return func(*args, **kwargs)
            except:
                oh_never_mind(name)
                raise

        return wrapper

    return real_decorator


def execute_with_environment(command, env):
    nose_process = os.subprocess.Popen(command.split(" "), env=env)
    nose_process.communicate()  # wait


import subprocess


def execute_get_text(command):
    try:
        completed = subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as err:
        raise
    else:
        return completed.stdout.decode('utf-8')


@task()
# @skip_if_no_change("bumpversion")
def bumpversion():
    """
    Fails if git isn't committed.
    :return:
    """
    # hide until fixed.
    return
    x = execute_get_text(" ".join(["python", "-c", '"import {0};print({0}.__version__)"'.format(PROJECT_NAME)]))
    print(x)
    current_version = Version(x)
    # new_version = Version("{0}{1}{2}".format(current_version.major, current_version.minor, current_version.build +1))
    # bumpversion --new-version 2.0.2 build --no-tag  --no-commit
    execute("bumpversion", "--current-version", str(current_version), "build", "--tag", "--no-commit")


@task()
@skip_if_no_change("clean")
def clean():
    for folder in ["build", "dist", PROJECT_NAME + ".egg-info"]:
        execute("rm", "-rf", folder)

    try:
        execute("rm", "lint.txt")
    except:
        pass


@task(clean)
@skip_if_no_change("compile")
def compile():
    execute(PYTHON, "-m", "compileall", PROJECT_NAME)


@task(compile)
@skip_if_no_change("lint")
def lint():
    # sort of redundant to above...
    #
    execute("prospector",
            *("{0} --profile {0}_style --pylint-config-file=pylintrc.ini --profile-path=.prospector"
              .format(PROJECT_NAME)
              .split(" ")))

    command = "{0}pylint --rcfile=pylintrc.ini {1}".format(PIPENV, PROJECT_NAME)

    lint_output_file_name = "lint.txt"
    with open(lint_output_file_name, "w") as outfile:
        subprocess.call(command.split(" "), stdout=outfile)

    num_lines = sum(1 for line in open('lint.txt')
                    if "*************" not in line
                    and "---------------------" not in line
                    and "Your code has been rated at" not in line)
    if num_lines > 100:
        raise TypeError("Too many lines of lint : {0}".format(num_lines))


@task(lint)
@skip_if_no_change("nose_tests")
def nose_tests():
    # if these were integration tests with say, API calls, we might not want to skip
    execute(PYTHON, "-m", "nose", PROJECT_NAME)


@task(nose_tests)
@skip_if_no_change("coverage")
def coverage():
    # if these were integration tests with say, API calls, we might not want to skip
    execute("py.test", *("{0} --cov={0} --cov-report html:coverage --verbose".format(PROJECT_NAME).split(" ")))


@task(nose_tests)
@skip_if_no_change("docs")
def docs():
    with safe_cd("docs"):
        execute("make", "html")


@task()
@skip_if_no_change("pip_check")
def pip_check():
    execute("pip", "check")
    execute("safety", "check")
    execute("safety", "check", "-r", "requirements_dev.txt")

@task()
def compile_md():
    execute("pandoc", *("--from=markdown --to=rst --output=README.rst README.md".split(" ")))

@task(nose_tests, pip_check, compile, lint) # docs pending init
@skip_if_no_change("package")
def package():
    execute("python", "setup.py", "sdist", "--formats=gztar,zip")


@task()
def echo(*args, **kwargs):
    print(args)
    print(kwargs)


# Default task (if specified) is run when no task is specified in the command line
# make sure you define the variable __DEFAULT__ after the task is defined
# A good convention is to define it at the end of the module
# __DEFAULT__ is an optional member

__DEFAULT__ = echo
