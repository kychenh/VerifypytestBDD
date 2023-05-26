# conftest.py

import pytest, allure
from playwright.sync_api import Page

# pytest hook to capture the screenshot after each step
@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    # Get the current page from the step_func_args
    if step_func_args['page'] : 
        page: Page = step_func_args['page']
    else : 
        page = None
        print(f"can not get Page object for this step {step}")
    # Capture a screenshot using playwright
    screenshot_path = f"screenshots/{scenario.feature.name}_{scenario.name}_{step.keyword}_{step.name}.png"
    page.screenshot(path=screenshot_path)

    # Attach the screenshot to the allure report
    allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)

