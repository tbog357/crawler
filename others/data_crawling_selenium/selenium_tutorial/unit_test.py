import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(chrome_options=options)

    def test_search_in_python_org(self):
        driver = self.driver

        driver.get("http://python.org")

        self.assertIn("Python", driver.title)

        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()