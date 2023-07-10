import os
from os.path import join, dirname
# from dotenv import load_dotenv
from configparser import ConfigParser
import helper.micellenuous as micel


# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

BASEDIR = dirname(__file__)
TESTDATA_FOLDER=join(BASEDIR, "testdata/")
TRACE_FOLDER = join(BASEDIR, "traces")
TRACE_TMP_FILENAME = join(TRACE_FOLDER, "trace_tmp.zip")
TRACEVIEWER_URL = "https://trace.playwright.dev"
SCREENSHOOT_FOLDER = join(BASEDIR,"screenshoots")
VIDEO_FOLDER = join(BASEDIR,"videos")
REPORT_FOLDER = join(BASEDIR,"allure-report")
REMOTE_DIRSEP = "/"
LOCAL_DIRSEP = "\\"
LOG_FOLDER = join(BASEDIR, "logs")
DBCONFIG_FILE = join(BASEDIR,"DBconfig.ini")
CONFIGDATA = join(BASEDIR, "configs/browser_args.json")

# get screensize 
resolution = micel.get_monitor_resolution()
if resolution :    
    screensize_width = resolution[0]
    screensize_height = resolution[1]
else : 
    screensize_width = 0
    screensize_height = 0

# parameters fro appium 
# APPIUM = {
#     "Server_url" :"http://127.0.0.1:4723/wd/hub", 

# }


# _conf = ConfigParser()
# _conf.read(DBCONFIG_FILE)

# API_URL = _conf.get("test_env_" + _conf.get("database","test_env"),"api_base_url")
# BILLING_DEL_BILL = _conf.get("var_name","BillDelDill")

