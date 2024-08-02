from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from config import GLOBAL_CONFIG
import difflib
import base64
import time

class Simulator(webdriver.Chrome):
    def __init__(self, force_headless=False):
        self.url = ""
        chrome_options = Options()
        if GLOBAL_CONFIG['simulator']['headless'] or force_headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--lang=en-GB")
        chrome_options.add_argument("--disable-web-security");
        chrome_options.add_argument(f"user-data-dir={GLOBAL_CONFIG['simulator']['user_data_dir']}")
        super().__init__(options=chrome_options)

    def restart(self, url=None):
        if url:
            self.get(url)
            self.url = url
        else:
            self.get(self.url)
        if ("miniwob" in self.url):
            div_element = self.find_element(By.ID, "sync-task-cover")
            div_element.click()

    def init(self, url):
        self.url = url
        self.get(url)
        if ("miniwob" in self.url):
            div_element = self.find_element(By.ID, "sync-task-cover")
            div_element.click()

    def crawl(self):
        js_file_path = "script/html_extractor.js" 
        with open(js_file_path, "r") as js_file:
            js_script = js_file.read()
        html = self.execute_script(js_script)
        return html
    
    def get_clickables(self):
        js_file_path = ""
        if (".html" in self.url):
            if ("wrapper.html" in self.url):
                js_file_path = "script/miniwob_clickable_extractor_flight.js"
            else:
                js_file_path = "script/miniwob_clickable_extractor.js"
        else:
            js_file_path = "script/clickable_extractor.js" 
        with open(js_file_path, "r") as js_file:
            js_script = js_file.read()
        parameters = {
            "expression": js_script,
            "includeCommandLineAPI": True,
            "returnByValue": True,
        }
        html = self.execute_cdp_cmd("Runtime.evaluate", parameters)
        return html['result']['value']
    
    def get_screenshot_url(self):
        screenshot = self.find_element(By.TAG_NAME, 'body').screenshot_as_png
        data = base64.b64encode(screenshot).decode()
        data_uri = f'data:image/png;base64,{data}'
        return data_uri
    
    def get_screenshot_base64(self):
        screenshot = self.find_element(By.TAG_NAME, 'body').screenshot_as_png
        data = base64.b64encode(screenshot).decode()
        return data

    def get_lis_html(self):
        js_file_path =  "script/li_et_al_extractor.js" 
        if ("wrapper.html" in self.url):
            js_file_path = "script/li_et_al_extractor_flight.js"
        with open(js_file_path, "r") as js_file:
            js_script = js_file.read()
        parameters = {
            "expression": js_script,
            "includeCommandLineAPI": True,
            "returnByValue": True,
        }
        html = self.execute_cdp_cmd("Runtime.evaluate", parameters)
        return html['result']['value']
    
    def has_reach_end(self):
        if "miniwob" in self.url:
            re = self.__get_miniwob_result()
            return re['reward'] != '-'
        return False
    
    def is_successful(self):
        if "miniwob" in self.url:
            re = self.__get_miniwob_result()
            return  float(re['reward'])>= 0
        return None

    def __get_miniwob_result(self):
        js_file_path = "script/miniwob_result_extractor.js" 

        with open(js_file_path, "r") as js_file:
            js_content = js_file.read()

        js_script = f"""
        {js_content}
        """
        re = self.execute_script(js_script)
        return re
