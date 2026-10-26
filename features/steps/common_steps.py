from behave import given, when

from pages.base_page import BasePage


@given("que acesso o site DemoQA")
def step_open_home(context):
    context.page = BasePage(context.driver)
    context.page.open("/")


@when('escolho a opção "{card}" na página inicial')
def step_select_card(context, card):
    context.page.select_card(card)


@when('clico no submenu "{menu}"')
def step_select_menu(context, menu):
    context.page.select_menu(menu)
