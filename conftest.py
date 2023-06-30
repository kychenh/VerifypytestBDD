# conftest.py

import pytest, allure, re
from playwright.sync_api import (Page, BrowserContext, sync_playwright)
from playwright.async_api import async_playwright
import asyncio
from settings import *
import helper.micellenuous as micel
import csv 
import pathlib, os
from appium import webdriver


# pytest hook to capture the screenshot after each step
@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    # Get the current page from the step_func_args
    page = None
    
    # if 'idriver' in step_func_args : 
    #     driver = step_func_args['idriver']
    #     if isinstance(driver, Page) :
    #         page = driver     
    if 'page' in step_func_args : 
        page: Page = step_func_args['page']
    else : 
        page = None
        print(f"can not get Page object for this step {step}")
    # Capture a screenshot using playwright
    screenshot_path = f"screenshots/scrshoot_{micel.getTimestampStr()}.png"

    page.screenshot(path=screenshot_path)

    # Attach the screenshot to the allure report
    allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True)
# Register the pytest hooks
def pytest_bdd_before_scenario(request, feature, scenario):
    trace_name = TRACE_TMP_FILENAME
    context = request.getfixturevalue('context')
    # browser = request.getfixturevalue('browser')
    # playwright = request.getfixturevalue('playwright')
    # page = request.getfixturevalue('page')
    # iphone_13 = playwright.devices['iPhone 13']
    # browser = playwright.webkit.launch(headless=False)
    # context = browser.new_context(
    #     **iphone_13,
    # )
    context.tracing.start(screenshots=True, snapshots=True)


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_scenario(request, feature, scenario):
    context = request.getfixturevalue('context')
    page = request.getfixturevalue('page')
    # page = request.getfixturevalue('idriver')
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
    # if page.is_closed()==False : page.close()
    
    filename = f"videotmp_{micel.getTimestampStr() }"    
    
    try:
        page.video.save_as("videos/"+ filename)    
    except Exception:
        print("[info]try close page before save as video!!") 
        page.close()
        # page = context.new_page()
        page.video.save_as("videos/"+ filename)

    print(f"video file path {page.video.path()}")    

    with open(page.video.path(), "rb") as video_file:         
        allure.attach(video_file.read(),name=f"recording video {filename}", attachment_type=allure.attachment_type.WEBM)
    page.close()
    context.close()
    
    
    

# @pytest.fixture(scope="session")
# def browser_type_launch_args(browser_type_launch_args):
#     """
#     overwrite fixture "browser_type_launch_args" to maximize window when initilize browser.

#     """
#     # in playwright package, an completed function to overwrite fixture "browser_type_launch_args" to maximize window when initilize browser
#     return {
#         **browser_type_launch_args,
#         # 'devtools' : True,
#         "traces_dir": TRACE_FOLDER,        
#         "args": ["--start-maximized"],
#     }

# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args, playwright):
#     """
#     overwrite the fixture of playwright : browser_context_args
#     and add some paramaters such as recorad video size, viewport.
#     """
#     # uncomment when added device OR use pytest.ini file with below argument
#     # --device="iPhone 11 Pro"
    
#     # iphone_11 = playwright.devices['iPhone 11 Pro']
        
#     print("create browser contesxt _arg fixtures is called")
#     record_video_dir = VIDEO_FOLDER
#     if not os.path.exists(record_video_dir):
#         os.makedirs(record_video_dir)

#     return {
#         **browser_context_args,
#         "record_video_size": {"width": screensize_width, "height": screensize_height},
#         "no_viewport": True,
#         "record_video_dir": record_video_dir,        
#         # "viewport": {"width": screensize_width, "height": screensize_height},
#         # **iphone_11    # added device size
#     }

def pytest_addoption(parser):
    parser.addoption("--output-tests-csv", action="store", default=None , help="out the execution intention test case to a csv file")
    parser.addoption("--filter", action="store", default=None , help="filter out by provided regular expression")
    parser.addoption("--testcasefile", action="store",default=None , help="use this test case list to determine which case is run, \n csv file format with 2 col ( testcase name, yes/no)")



def pytest_collection_modifyitems(config, items):
    csv_out = config.getoption("--output-tests-csv")
    reg_exp = config.getoption("--filter")
    testcasefile = config.getoption("--testcasefile")
    colidx = {
        "caseID":"caseid",
        "selected": "selected"
    } # column with value yes/no to detemine test case to run. 
    header = []

    if csv_out:
        tests = []
        # collect all tests with matching markers
        # for item in items:
        #     tests.append(item.name)
                    
        # write tests in csv (one line per marker)
        with open(csv_out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for item in items:
                print(item.name)
                writer.writerow([item.name, item.location, item.parent, item.path, item.config] + item.user_properties )
    
    result = [item for item in items]
    if reg_exp:
        
        filtered_items = []
        for item in items:
            if re.match(reg_exp, item.name):
                filtered_items.append(item)
        result = filtered_items
    
    tmp = []
    if testcasefile: 
        if not os.path.isabs(testcasefile) : 
            testcasefile = os.path.abspath(testcasefile)
        print(f"test case file path = {testcasefile}")
        tmp = result if result else items # incase two argument --filter and --testcasefile co-existing, we take the result effect. 
        result= []
        testcases= micel.csvfile(testcasefile)
        print(testcases)
        print(f"After filter we have {tmp}")
        header = testcases.get_datalist()[0]
        header = [str.lower(x) for x in header] # lower the case of header to avoid header case sensitive before compare

        testcases = testcases.get_datalist()[1:] # eliminate header row
        print(testcases)
        testcases = filter(lambda x: re.search("(yes|y)", x[header.index(colidx["selected"])], re.IGNORECASE), testcases)
        testcases = [i for i in testcases]
        for item in tmp: 
            print(f"process item {item.name}")
            for case in testcases: 
                
                print(f"case  = {case[header.index(colidx['caseID'])]}")
                if re.search(f"{case[header.index(colidx['caseID'])]}", item.name, re.IGNORECASE):
                    if not item in result : 
                        print(f"found item startith {case[header.index(colidx['caseID'])]}")
                        
                        result.append(item)
                        
                    # continue

    items[:] = result


# @pytest.fixture(scope="session")
# def idriver (request, playwright):
#     param = "web"
#     driver = playwright.chromium.launch(headless=False).new_context().new_page()
#     yield driver
#     # driver.close()
        
@pytest.fixture()
def context(playwright):
    
    context = playwright.chromium.launch().new_context(
        record_video_dir=VIDEO_FOLDER
    )
    yield context
    # context.close()

@pytest.fixture()
def page(context):
    page = context.new_page()
    yield page
    # page.close()
