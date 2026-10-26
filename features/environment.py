from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.config import HEADLESS

def before_scenario(context, scenario):
    if "ui" in scenario.tags:
        opts = Options()
        if HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        context.driver = webdriver.Chrome(options=opts)

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        if scenario.status == "failed":
            context.driver.save_screenshot(f"screenshot_{scenario.name}.png")
        context.driver.quit()