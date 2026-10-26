from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class BrowserWindowsPage(BasePage):
    NEW_WINDOW_BUTTON = (By.ID, "windowButton")
    SAMPLE_HEADING = (By.ID, "sampleHeading")

    def __init__(self, driver):
        super().__init__(driver)
        self.original_handle = driver.current_window_handle

    def open_new_window(self):
        self.original_handle = self.driver.current_window_handle
        self.click(self.NEW_WINDOW_BUTTON)
        self.wait.until(EC.number_of_windows_to_be(2))
        new_handle = next(h for h in self.driver.window_handles if h != self.original_handle)
        self.driver.switch_to.window(new_handle)

    def sample_message(self) -> str:
        return self.text_of(self.SAMPLE_HEADING)

    def close_new_window(self):
        self.driver.close()
        self.driver.switch_to.window(self.original_handle)
        self.wait.until(EC.number_of_windows_to_be(1))

    def open_windows_count(self) -> int:
        return len(self.driver.window_handles)
