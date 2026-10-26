from behave import when, then

from pages.sortable_page import SortablePage, ASCENDING


@when("ordeno os elementos em ordem crescente usando drag and drop")
def step_sort(context):
    context.sortable = SortablePage(context.driver)
    context.sortable.sort_ascending()


@then("a lista exibe os elementos em ordem crescente")
def step_validate_sorted(context):
    actual = context.sortable.items_text()
    assert actual == ASCENDING, f"Ordem final {actual} != esperada {ASCENDING}"
