import shutil
import subprocess

from behave import given, then, when  # pylint: disable=no-name-in-module

# pylint: disable=function-redefined


@given("we have rpgt installed")
def step_impl(context):  # noqa: F811
    assert shutil.which("rpgt") is not None


@given('file "{file_name}" already exists')
def step_impl(context, file_name):  # noqa: F811
    context.scenario_test_dir.joinpath(file_name).touch()


@when("we run rpgt")
def step_impl(context):  # noqa: F811
    final_command = ["rpgt"]
    completed_process = subprocess.run(
        final_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    context.return_code = completed_process.returncode
    context.stdout = completed_process.stdout.decode("utf-8")
    context.stderr = completed_process.stderr.decode("utf-8")


@when('we run init command with parameter "{parameter}"')
def step_impl(context, parameter):  # noqa: F811
    final_command = ["rpgt", "init", f"{parameter}"]
    completed_process = subprocess.run(
        final_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    context.return_code = completed_process.returncode
    context.stdout = completed_process.stdout.decode("utf-8")
    context.stderr = completed_process.stderr.decode("utf-8")


@then('return code is "{return_code}"')
def step_impl(context, return_code):  # noqa: F811
    assert context.return_code == int(return_code)


@then('we see "{text}" on stdout')
def step_impl(context, text):  # noqa: F811
    if context.stdout:
        assert text in context.stdout, f"Expected text [{text}] not found in stdout"
    else:
        assert False, f"stdout is empty, expected text [{text}] not found in"


@then('we see "{text}" on stderr')
def step_impl(context, text):  # noqa: F811
    if context.stderr:
        assert text in context.stderr, f"Expected text [{text}] not found in stderr"
    else:
        assert False, f"stderr is empty, expected text [{text}] not found in"


@then('file "{file_name}" is created')
def step_impl(context, file_name):  # noqa: F811
    assert context.scenario_test_dir.joinpath(file_name).is_file()
