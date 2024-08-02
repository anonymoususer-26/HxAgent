from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from error import CannotPerformActionError
from abc import abstractmethod
from time import sleep

class Action:
    def __init__(self, xpath, description = None, description_detail = None):
        self.xpath = xpath
        self.description = description
        self.description_detail = description_detail

    @abstractmethod
    def _perform(self, driver):
        pass

    @abstractmethod
    def _toSeleniumScript(self):
        pass

    def perform(self, driver):
        try:
            is_flight_task = None
            try:
                wrap_element = driver.find_element(By.ID, "wrap")
                if (wrap_element.tag_name == "iframe"):
                    driver.switch_to.frame(driver.find_element(By.ID, "wrap"))
                    driver.get_lis_html()
                    is_flight_task = True
            except NoSuchElementException:
                pass
            self._perform(driver)
            if (is_flight_task):
                driver.switch_to.default_content()
        except Exception as e:
            if (is_flight_task):
                driver.switch_to.default_content()
            raise CannotPerformActionError(e, self.xpath)

    def toSeleniumScript(self):
        return self._toSeleniumScript()
    
    def __str__(self):
        return self.description


class ClickAction(Action):
    def __init__(self, xpath, description = "Click"):
        super().__init__(xpath)
        self.description = description

    def _perform(self, driver):
        driver.find_element(By.XPATH, self.xpath).click()
    
    def _toSeleniumScript(self):
        return f"driver.find_element(By.XPATH, '{self.xpath}').click()"

class InputAction(Action):
    def __init__(self, xpath, content, description = "Input"):
        super().__init__(xpath, description)
        self.content = content

    def _perform(self, driver):
        element = driver.find_element(By.XPATH, self.xpath)
        element.clear()
        element.send_keys(self.content)
    
    def _toSeleniumScript(self):
        return f"""element = driver.find_element(By.XPATH, '{self.xpath}')
element.clear()
element.send_keys('{self.content}')"""