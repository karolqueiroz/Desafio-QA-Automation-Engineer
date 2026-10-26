from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class ProgressBarPage(BasePage):
    START_STOP = (By.ID, "startStopButton")
    RESET = (By.ID, "resetButton")
    BAR = (By.CSS_SELECTOR, "#progressBar [role='progressbar']")

    def value(self) -> int:
        element = self.find(self.BAR)
        raw = element.get_attribute("aria-valuenow") or element.text.replace("%", "")
        return int(raw)

    def start(self):
        self.js_click(self.START_STOP)

    def stop_when_reaches(self, target: int = 20):
        """Faz polling curto e clica em Stop assim que atingir `target`%.

        O alvo (20) deixa folga até o limite de 25% para a latência do Selenium.
        """
        WebDriverWait(self.driver, 30, poll_frequency=0.01).until(lambda d: self.value() >= target)
        self.js_click(self.START_STOP)

    def wait_until_complete(self):
        WebDriverWait(self.driver, 30, poll_frequency=0.1).until(lambda d: self.value() >= 100)

    def reset(self):
        self.click(self.RESET)
