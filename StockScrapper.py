from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs
from datetime import datetime


class StockScrapper:
    def __init__(self, headless=True):
        self.initialize_driver(headless)
        self.data_tests = ['PREV_CLOSE-value', 'OPEN-value', 'BID-value', 'ASK-value']
        
    def initialize_driver(self, headless=True):
        options = webdriver.ChromeOptions() 
        if headless:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options) 
        try: # Accepting yahoo's cookies
            self.driver.get("https://finance.yahoo.com/")    
            self.driver.find_element(by="id", value="scroll-down-btn").click()
            self.driver.find_element(By.XPATH, '//button[1]').click()
        except:
            pass
    
    def scrap(self, symbol: str):
        url = f"https://finance.yahoo.com/quote/{symbol}"
        try:
            self.driver.get(url)
            page_content = self.driver.page_source
            out = dict()            
            for td in bs(page_content, "html.parser").find_all("td"):
                property = td.get("data-test") 
                if (property is not None) and (property in self.data_tests):
                    out[property] = td.get_text()
            
            if len(out)==0:
                return "ERROR1"
            out["symbol"] = symbol
            out["datetime"] = str(datetime.now())

            return out
        except:
            return "ERROR2"