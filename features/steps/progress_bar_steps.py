from behave import when, then

from pages.progress_bar_page import ProgressBarPage


def _bar(context) -> ProgressBarPage:
    if not hasattr(context, "progress"):
        context.progress = ProgressBarPage(context.driver)
    return context.progress


@when("inicio a progress bar")
def step_start(context):
    _bar(context).start()


@when("paro a progress bar antes de atingir 25%")
def step_stop_before_25(context):
    _bar(context).stop_when_reaches(20)


@then("o valor da progress bar é menor ou igual a 25%")
def step_value_le_25(context):
    value = _bar(context).value()
    assert value <= 25, f"A barra passou de 25%: {value}%"


@when("inicio a progress bar novamente")
def step_start_again(context):
    _bar(context).start()


@when("aguardo a progress bar chegar a 100%")
def step_wait_100(context):
    _bar(context).wait_until_complete()


@when("reseto a progress bar")
def step_reset(context):
    _bar(context).reset()


@then("o valor da progress bar é 0%")
def step_value_zero(context):
    assert _bar(context).value() == 0
