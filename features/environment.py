import logging
import os


def before_all(context):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def before_scenario(context, scenario):
    # Driver só é criado para cenários de UI (@ui); API não precisa de browser.
    # effective_tags inclui as tags herdadas da Funcionalidade.
    if "ui" in scenario.effective_tags:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from utils.config import HEADLESS

        opts = Options()
        if HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--disable-popup-blocking")
        # "eager": não espera anúncios/recursos externos terminarem de carregar.
        opts.page_load_strategy = "eager"
        context.driver = webdriver.Chrome(options=opts)


def after_scenario(context, scenario):
    driver = getattr(context, "driver", None)
    if driver:
        if scenario.status == "failed":
            os.makedirs("screenshots", exist_ok=True)
            safe = "".join(c if c.isalnum() else "_" for c in scenario.name)
            try:
                driver.save_screenshot(f"screenshots/{safe}.png")
                with open(f"screenshots/{safe}.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
            except Exception:
                pass
        driver.quit()