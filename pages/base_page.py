import sys

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import BASE_URL, TIMEOUT

SELECT_ALL = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL


class BasePage:
    """Ações genéricas reutilizadas por todas as Page Objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def open(self, path: str = ""):
        self.driver.get(f"{BASE_URL}{path}")
        self.remove_ads()

    def select_card(self, name: str):
        """Escolhe um card na página inicial (Forms, Elements, Widgets...)."""
        self.click((By.XPATH, f"//div[contains(@class,'card-body')]//h5[normalize-space()='{name}']"))

    def select_menu(self, name: str):
        """Clica em um item do menu lateral (Practice Form, Web Tables...)."""
        self.click((By.XPATH, f"//li[starts-with(@id,'item-')]//span[normalize-space()='{name}']"))

    def remove_ads(self):
        """Esconde banner fixo, rodapé e iframes de anúncio via CSS.

        Esconder (em vez de remover do DOM) evita conflito com o React.
        """
        self.driver.execute_script(
            """
            if (!document.getElementById('qa-hide-ads')) {
                const style = document.createElement('style');
                style.id = 'qa-hide-ads';
                style.textContent =
                    '#fixedban, footer, iframe, [id^="google_ads"] { display: none !important; }';
                document.head.appendChild(style);
            }
            """
        )

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def click(self, locator):
        self.remove_ads()
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.scroll_to(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text: str, retries: int = 3):
        """Limpa o campo (select-all + backspace, funciona com React) e digita.

        Refaz a busca do elemento se o React o recriar durante a digitação.
        """
        for attempt in range(retries):
            try:
                element = self.visible(locator)
                self.scroll_to(element)
                element.click()
                element.send_keys(SELECT_ALL, "a", Keys.BACKSPACE)
                element.send_keys(text)
                return
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise

    def text_of(self, locator) -> str:
        return self.visible(locator).text

    def wait_invisible(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))
