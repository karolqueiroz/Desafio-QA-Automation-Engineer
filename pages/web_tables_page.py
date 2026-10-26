from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class WebTablesPage(BasePage):
    ADD_BUTTON = (By.ID, "addNewRecordButton")
    SUBMIT = (By.ID, "submit")
    MODAL = (By.CSS_SELECTOR, ".modal-content")
    PAGE_SIZE = (By.CSS_SELECTOR, "select.form-control")

    FIELDS = {
        "first_name": (By.ID, "firstName"),
        "last_name": (By.ID, "lastName"),
        "email": (By.ID, "userEmail"),
        "age": (By.ID, "age"),
        "salary": (By.ID, "salary"),
        "department": (By.ID, "department"),
    }

    @staticmethod
    def _row_xpath(email: str) -> str:
        # A tabela agora é <table>/<tr>/<td> comum; o e-mail identifica a linha.
        return f"//tr[.//td[normalize-space()='{email}']]"

    def _row(self, email: str) -> tuple:
        return (By.XPATH, self._row_xpath(email))

    def show_all_rows(self):
        """Exibe 50 linhas por página (máximo do select) para evitar paginação."""
        element = self.find(self.PAGE_SIZE)
        self.scroll_to(element)
        Select(element).select_by_value("50")

    def _fill_form(self, data: dict):
        for key, value in data.items():
            self.type(self.FIELDS[key], value)

    def _submit_form(self):
        self.js_click(self.SUBMIT)
        self.wait_invisible(self.MODAL)

    def add_record(self, record: dict):
        self.click(self.ADD_BUTTON)
        self.visible(self.MODAL)
        self._fill_form(record)
        self._submit_form()

    def edit_record(self, email: str, changes: dict):
        self.click((By.XPATH, self._row_xpath(email) + "//*[@title='Edit' or starts-with(@id,'edit-record')]"))
        self.visible(self.MODAL)
        self._fill_form(changes)
        self._submit_form()

    def delete_record(self, email: str):
        row = self._row(email)
        button = (By.XPATH, self._row_xpath(email)
                  + "//*[@title='Delete' or starts-with(@id,'delete-record')]")
        found = self.driver.find_elements(*button)
        assert found, (
            f"Linha de {email} não encontrada para deletar. "
            f"E-mails atuais na tabela: {self.emails_in_table()}"
        )
        self.scroll_to(found[0])
        self.driver.execute_script("arguments[0].click();", found[0])
        self.wait.until(EC.invisibility_of_element_located(row))

    def emails_in_table(self) -> list:
        cells = self.driver.find_elements(By.XPATH, "//tr//td[contains(text(),'@')]")
        return [cell.text for cell in cells]
    
    def row_text(self, email: str) -> str:
        return self.visible(self._row(email)).text

    def record_exists(self, email: str) -> bool:
        return len(self.driver.find_elements(*self._row(email))) > 0
