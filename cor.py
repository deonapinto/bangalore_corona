from selenium import webdriver
import csv
from threading import Thread
import threading
import schedule
import time
import os
from selenium.webdriver.common.keys import Keys

class WebScraper(Thread):
    thread_stop = False

    def __init__(self, callback=None):
        super().__init__()
        self.callback_func = callback
        print('WebScraper -> init')
        self.scheduler = schedule.Scheduler()

    def scrape_data(self):
        chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', 'C:\bin\chromedriver.exe')
        print('scrape_data -> started', threading.get_ident())
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        options.add_argument('disable-infobars')
        options.add_argument('disable-notifications')
        if os.environ.get('GOOGLE_CHROME_SHIM', None) is not None:
            options.binary_location = chrome_bin


        print("corona data file is being created.... please wait.")
        driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        driver.get('https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/')

        state_district = []
        

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        # page=driver.find_element_by_id('page')
        for skgm_state in driver.find_elements_by_class_name("skgm-states"):
            
            state = skgm_state.find_element_by_class_name("show-district").text.replace('\n','').lower()

            skgm_tds = skgm_state.find_elements_by_xpath('.//div[contains(@class,"skgm-districts")]/div[@class="skgm-tr"]/child::div[@class="skgm-td"]')

            districts = []
            
            for i in range(0, len(skgm_tds), 5):

                district = skgm_tds[i].get_attribute('innerHTML').strip().replace('\n','').lower()
                case = skgm_tds[i+1].get_attribute('innerHTML').strip().replace('\n','')
                cured = skgm_tds[i+2].get_attribute('innerHTML').strip().replace('\n','')
                active = skgm_tds[i+3].get_attribute('innerHTML').strip().replace('\n','')
                death = skgm_tds[i+4].get_attribute('innerHTML').strip().replace('\n','')
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                districts.append([state,district, case, cured, active, death])
            print('Got values for state :', state)
            state_district.extend(districts)

        f = open("sample.csv", "w+")
        f.truncate()
        writer = csv.DictWriter(f, fieldnames=['state','district', 'case', 'cured', 'active', 'death'])
        writer.writeheader()
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(state_district)
        f.close()
        driver.close()
        print('scrape_data -> end')

    def run(self):
        print("web_scraper_thread -> started", threading.get_ident())
        if self.callback_func is not None:
            self.scrape_data()
            self.callback_func()
        else:
            self.scheduler.every().day.at("15:20").do(self.scrape_data)
            # self.scheduler.every(5).minutes.do(self.scrape_data)
            # self.scrape_data()
            while not self.thread_stop:
                self.scheduler.run_pending() 
                time.sleep(1)