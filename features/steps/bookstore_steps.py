import random

from behave import given, when, then

from api.account_client import AccountClient
from api.bookstore_client import BookStoreClient
from utils.data_factory import build_user


@given("que crio um novo usuário com dados válidos")
def step_create_user(context):
    context.account = AccountClient()
    context.bookstore = BookStoreClient()
    context.user = build_user()

    response = context.account.create_user(**context.user)

    assert response.status_code == 201, (
        f"Esperado 201 ao criar usuário, veio {response.status_code}: {response.text}"
    )
    body = response.json()
    assert body["username"] == context.user["user_name"], "username retornado difere do enviado"
    assert body["userID"], "userID não retornado"
    assert body["books"] == [], "usuário novo não deveria ter livros"
    context.user_id = body["userID"]


@given("gero um token de acesso para o usuário")
def step_generate_token(context):
    response = context.account.generate_token(**context.user)

    assert response.status_code == 200, (
        f"Esperado 200 ao gerar token, veio {response.status_code}: {response.text}"
    )
    body = response.json()
    assert body["status"] == "Success", f"Falha ao gerar token: {body}"
    assert body["token"], "token vazio"
    context.token = body["token"]


@when("confirmo que o usuário está autorizado")
def step_check_authorized(context):
    response = context.account.is_authorized(**context.user)

    assert response.status_code == 200, (
        f"Esperado 200 em Authorized, veio {response.status_code}: {response.text}"
    )
    assert response.json() is True, f"Usuário não autorizado: {response.text}"


@when("listo os livros disponíveis")
def step_list_books(context):
    response = context.bookstore.list_books()

    assert response.status_code == 200, (
        f"Esperado 200 ao listar livros, veio {response.status_code}: {response.text}"
    )
    books = response.json()["books"]
    assert len(books) >= 2, "É preciso ao menos 2 livros disponíveis para reservar"
    context.available_books = books


@when("reservo dois livros de livre escolha")
def step_add_two_books(context):
    context.chosen_books = random.sample(context.available_books, 2)
    isbns = [book["isbn"] for book in context.chosen_books]

    response = context.bookstore.add_books(context.user_id, isbns, context.token)

    assert response.status_code == 201, (
        f"Esperado 201 ao reservar livros, veio {response.status_code}: {response.text}"
    )
    returned_isbns = {book["isbn"] for book in response.json()["books"]}
    assert returned_isbns == set(isbns), f"ISBNs retornados {returned_isbns} != enviados {set(isbns)}"


@then("os detalhes do usuário exibem os dois livros reservados")
def step_validate_user_details(context):
    response = context.account.get_user(context.user_id, context.token)

    assert response.status_code == 200, (
        f"Esperado 200 ao detalhar usuário, veio {response.status_code}: {response.text}"
    )
    body = response.json()
    assert body["username"] == context.user["user_name"]
    assert len(body["books"]) == 2, f"Esperado 2 livros, vieram {len(body['books'])}"

    expected = {book["isbn"] for book in context.chosen_books}
    actual = {book["isbn"] for book in body["books"]}
    assert actual == expected, f"Livros do usuário {actual} != reservados {expected}"
