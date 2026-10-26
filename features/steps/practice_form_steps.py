from behave import when, then

from pages.practice_form_page import PracticeFormPage
from utils.data_factory import build_student


@when("preencho todo o formulário com valores aleatórios")
def step_fill_form(context):
    context.form = PracticeFormPage(context.driver)
    context.student = build_student()
    context.form.fill(context.student)


@when("envio o formulário")
def step_submit_form(context):
    context.form.submit()


@then("um popup de confirmação é exibido com os dados informados")
def step_validate_modal(context):
    student = context.student
    assert context.form.modal_title() == "Thanks for submitting the form"

    values = context.form.modal_values()
    assert values["Student Name"] == f"{student['first_name']} {student['last_name']}"
    assert values["Student Email"] == student["email"]
    assert values["Gender"] == student["gender"]
    assert values["Mobile"] == student["mobile"]
    assert values["Subjects"] == student["subject"]
    assert set(values["Hobbies"].split(", ")) == set(student["hobbies"])
    assert values["Picture"] == "upload.txt"
    assert values["Address"] == " ".join(student["address"].split())
    assert values["State and City"] == f"{student['state']} {student['city']}"


@when("fecho o popup")
def step_close_modal(context):
    context.form.close_modal()


@then("o popup não é mais exibido")
def step_modal_closed(context):
    assert not context.form.is_modal_visible(), "O popup continua aberto"
