from behave import when, then

from pages.web_tables_page import WebTablesPage
from utils.data_factory import build_record


def _tables(context) -> WebTablesPage:
    if not hasattr(context, "web_tables"):
        context.web_tables = WebTablesPage(context.driver)
    return context.web_tables


def _assert_row_has(tables, email, data):
    text = tables.row_text(email)
    for value in data.values():
        assert value in text, f"'{value}' não encontrado na linha: {text!r}"


# ---------- CRUD ----------
@when("crio um novo registro")
def step_create_record(context):
    context.record = build_record()
    _tables(context).add_record(context.record)


@then("o registro criado aparece na tabela")
def step_record_created(context):
    _assert_row_has(_tables(context), context.record["email"], context.record)


@when("edito o registro criado")
def step_edit_record(context):
    novo = build_record()
    changes = {
        "first_name": novo["first_name"],
        "salary": novo["salary"],
        "department": novo["department"],
    }
    _tables(context).edit_record(context.record["email"], changes)
    context.record.update(changes)


@then("o registro editado aparece na tabela com os novos dados")
def step_record_edited(context):
    _assert_row_has(_tables(context), context.record["email"], context.record)


@when("deleto o registro criado")
def step_delete_record(context):
    _tables(context).delete_record(context.record["email"])


@then("o registro não existe mais na tabela")
def step_record_deleted(context):
    assert not _tables(context).record_exists(context.record["email"])


# ---------- Bônus: 12 registros ----------
@when("exibo 50 linhas por página")
def step_show_all_rows(context):
    _tables(context).show_all_rows()


@when("crio {quantidade:d} novos registros dinamicamente")
def step_create_many(context, quantidade):
    tables = _tables(context)
    context.records = []
    context.counts = []
    for _ in range(quantidade):
        record = build_record()
        tables.add_record(record)
        context.records.append(record)
        context.counts.append(len(tables.emails_in_table()))

@then("os {quantidade:d} registros criados aparecem na tabela")
def step_many_created(context, quantidade):
    assert len(context.records) == quantidade
    for record in context.records:
        assert _tables(context).record_exists(record["email"]), f"Faltou: {record['email']}"
    _tables(context).mark_session()



@when("deleto todos os registros criados")
def step_delete_many(context):
    tables = _tables(context)
    cliques = 0
    for record in context.records:
        if not tables.record_exists(record["email"]):
            # O DemoQA reinicia a tabela ao deletar uma linha, então os demais
            # registros criados já não existem mais neste ponto.
            continue
        tables.delete_record(record["email"])
        cliques += 1
    assert cliques >= 1, "Nenhuma exclusão foi executada"

@then("nenhum dos registros criados permanece na tabela")
def step_none_remaining(context):
    for record in context.records:
        assert not _tables(context).record_exists(record["email"]), f"Ainda existe: {record['email']}"
