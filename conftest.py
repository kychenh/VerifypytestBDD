# conftest.py

import pytest, allure
from playwright.sync_api import (Page, BrowserContext)
from settings import *
import helper.micellenuous as micel

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


@pytest.hookimpl(tryfirst=True)
# Register the pytest hooks
def pytest_bdd_before_scenario(request, feature, scenario):
    trace_name = TRACE_TMP_FILENAME
    context = request.getfixturevalue('context')
    context.tracing.start(screenshots=True, snapshots=True)

    

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_scenario(request, feature, scenario):
    context = request.getfixturevalue('context')
    context.tracing.stop(path=TRACE_TMP_FILENAME)

    trace_filepath = TRACE_TMP_FILENAME
    zip_new_name = trace_filepath.replace(
                    ".zip", micel.getTimestampStr() + ".zip"
                )
    # move this file to new dir and rename.
    os.rename(trace_filepath, zip_new_name)
    allure.attach.file(source=zip_new_name, name="Scenario Trace Zip file")
    
    # Attach the video to the allure report
    # allure.attach.video(path=VIDEO_FOLDER)

    
    

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    overwrite fixture "browser_type_launch_args" to maximize window when initilize browser.

    """
    # in playwright package, an completed function to overwrite fixture "browser_type_launch_args" to maximize window when initilize browser
    return {
        **browser_type_launch_args,
        # 'devtools' : True,
        "traces_dir": TRACE_FOLDER,
        "args": ["--start-maximized"],
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    overwrite the fixture of playwright : browser_context_args
    and add some paramaters such as recorad video size, viewport.
    """
    # uncomment when added device OR use pytest.ini file with below argument
    # --device="iPhone 11 Pro"

    # iphone_11 = playwright.devices['iPhone 11 Pro']
    record_video_dir = VIDEO_FOLDER
    if not os.path.exists(record_video_dir):
        os.makedirs(record_video_dir)

    return {
        **browser_context_args,
        "record_video_size": {"width": screensize_width, "height": screensize_height},
        # "no_viewport": True,
        "record_video_dir": record_video_dir,
        "viewport": {"width": screensize_width, "height": screensize_height},
        # **iphone_11    # added device size
    }