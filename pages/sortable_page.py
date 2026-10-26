from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage

ASCENDING = ["One", "Two", "Three", "Four", "Five", "Six"]


class SortablePage(BasePage):
    ITEMS = (By.CSS_SELECTOR, ".vertical-list-container .list-group-item")

    def items(self) -> list:
        self.visible(self.ITEMS)
        return self.driver.find_elements(*self.ITEMS)

    def items_text(self) -> list:
        return [item.text.strip() for item in self.items()]

    def sort_ascending(self, attempts_per_item: int = 3):
        """Ordena por seleção: leva cada item para a sua posição via drag and drop."""
        for index, label in enumerate(ASCENDING):
            for _ in range(attempts_per_item):
                items = self.items()
                if items[index].text.strip() == label:
                    break
                source = next(item for item in items if item.text.strip() == label)
                self._drag_onto(source, items[index])
                self._wait_position(index, label)

    def _wait_position(self, index: int, label: str):
        try:
            WebDriverWait(self.driver, 3).until(
                lambda d: self.items()[index].text.strip() == label
            )
        except Exception:
            pass  # o loop externo tenta novamente

    def _drag_onto(self, source, target):
        """Arrasta em passos pequenos: jQuery UI Sortable exige vários mousemove."""
        self.scroll_to(source)
        distance = target.location["y"] - source.location["y"]
        total = distance - 5 if distance < 0 else distance + 5
        sign = 1 if total > 0 else -1
        full_steps, remainder = divmod(abs(total), 10)

        actions = ActionChains(self.driver)
        actions.click_and_hold(source).pause(0.2)
        for _ in range(int(full_steps)):
            actions.move_by_offset(0, sign * 10).pause(0.02)
        if remainder:
            actions.move_by_offset(0, int(sign * remainder))
        actions.pause(0.2).release().perform()
