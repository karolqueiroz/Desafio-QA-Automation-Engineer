from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from utils.config import UPLOAD_FILE
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import SELECT_ALL
from selenium.common.exceptions import TimeoutException

class PracticeFormPage(BasePage):
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    MOBILE = (By.ID, "userNumber")
    BIRTH_DATE = (By.ID, "dateOfBirthInput")
    SUBJECTS = (By.ID, "subjectsInput")
    UPLOAD = (By.ID, "uploadPicture")
    ADDRESS = (By.ID, "currentAddress")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    SUBMIT = (By.ID, "submit")
    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    MODAL_CLOSE = (By.ID, "closeLargeModal")
    MODAL_ROWS = (By.CSS_SELECTOR, ".modal-body tbody tr")

    def fill(self, student: dict):
        self.type(self.FIRST_NAME, student["first_name"])
        self.type(self.LAST_NAME, student["last_name"])
        self.type(self.EMAIL, student["email"])
        self.click((By.XPATH, f"//label[normalize-space()='{student['gender']}']"))
        self.type(self.MOBILE, student["mobile"])
        self._fill_birth_date(student["birth_date"])
        self._fill_subject(student["subject"])
        for hobby in student["hobbies"]:
            self.click((By.XPATH, f"//label[normalize-space()='{hobby}']"))
        self.find(self.UPLOAD).send_keys(UPLOAD_FILE)
        self.type(self.ADDRESS, student["address"])
        self._select_dropdown(self.STATE, student["state"])
        self._select_dropdown(self.CITY, student["city"])

    def _fill_birth_date(self, date_text: str):
        # Clica só para focar; as teclas vão para o elemento focado, sem guardar
        # referência, porque o React recria o input quando o calendário abre.
        self.click(self.BIRTH_DATE)
        (
            ActionChains(self.driver)
            .key_down(SELECT_ALL).send_keys("a").key_up(SELECT_ALL)
            .send_keys(date_text)
            .send_keys(Keys.ENTER)
            .perform()
        )

    def _fill_subject(self, subject: str):
        field = self.find(self.SUBJECTS)
        self.scroll_to(field)
        field.send_keys(subject)
        field.send_keys(Keys.ENTER)

    def _select_dropdown(self, container, option_text: str):
        self.click(container)
        container_id = container[1]
        self.click((
            By.XPATH,
            f"//div[@id='{container_id}']//div[contains(@class,'option') and normalize-space()='{option_text}']",
        ))

    def submit(self):
        self.remove_ads()
        self.js_click(self.SUBMIT)

    def modal_title(self) -> str:
        return self.text_of(self.MODAL_TITLE)

    def modal_values(self) -> dict:
        """Retorna {rótulo: valor} da tabela exibida no popup."""
        self.visible(self.MODAL_TITLE)
        values = {}
        for row in self.driver.find_elements(*self.MODAL_ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                values[cells[0].text.strip()] = " ".join(cells[1].text.split())
        return values

    def close_modal(self):
        self.click(self.MODAL_CLOSE)  # clique real, com fallback para JS
        try:
            self.wait_invisible(self.MODAL_TITLE)
        except TimeoutException:
            # fallback: ESC fecha o modal do react-bootstrap
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            self.wait_invisible(self.MODAL_TITLE)

    def is_modal_visible(self) -> bool:
        return len(self.driver.find_elements(*self.MODAL_TITLE)) > 0
