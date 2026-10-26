from behave import when, then

from pages.browser_windows_page import BrowserWindowsPage


@when('clico no botão "New Window"')
def step_click_new_window(context):
    context.windows = BrowserWindowsPage(context.driver)
    context.windows.open_new_window()


@then('uma nova janela é aberta com a mensagem "{message}"')
def step_validate_message(context, message):
    assert context.windows.open_windows_count() == 2, "A nova janela não foi aberta"
    actual = context.windows.sample_message()
    assert actual == message, f"Esperado '{message}', veio '{actual}'"


@when("fecho a nova janela")
def step_close_new_window(context):
    context.windows.close_new_window()


@then("apenas a janela original permanece aberta")
def step_only_original(context):
    assert context.windows.open_windows_count() == 1
