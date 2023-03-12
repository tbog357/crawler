# Crawling tool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Command line tool
import argparse

# Json manipulation
import json
import os 

# Others
from tqdm import tqdm
import time

# local import 
from utils import crawl_summary, crawl_detail

def setup_webdriver(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.vietnamworks.com/")

    # Go to the jobs page
    elem = driver.find_element(By.CSS_SELECTOR, "a.sc-fzomME.hhnKZs")
    link = elem.get_attribute("href")
    driver.get(link)

    # Being redirected to another link
    driver.refresh()

    # Searching term
    search_bar = driver.find_element(By.ID, "main-search-bar")
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.RETURN)
    driver.implicitly_wait(3) # wait for page loading
    return driver

def job_crawling(driver):
    # Store crawled data
    data = []

    # Init values
    next_page_ava = True
    page_count = 0

    while next_page_ava:
        next_link = driver.find_elements(By.CSS_SELECTOR, "a.page-link")
        next_link = driver.find_elements(By.PARTIAL_LINK_TEXT, ">")

        # Scroll down to the end of the page
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(3) # wait for content-loaded

        # Crawling all jobs information
        jobs = driver.find_element(By.CSS_SELECTOR, "div.block-job-list")
        jobs = jobs.find_elements(By.CSS_SELECTOR, "div.job-item.animated.fadeIn.position-relative")
        
        # Verbose 
        print(f"Page {page_count}: {len(jobs)} jobs")

        # Collecting the data
        for j in tqdm(jobs):
            job_data = {}
            job_data, job_title = crawl_summary(job_data, j)

            # Open new tab by the link from title
            driver.execute_script("arguments[0].click();", job_title)
            driver.switch_to.window(driver.window_handles[1])

            # Crawl details informatin by access link
            job_data = crawl_detail(driver, job_data)

            # Close new tab and focust back to the main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            data.append(job_data)

        page_count += 1

        # Check if next page is available
        if len(next_link) != 0:
            next_page_ava = True
            driver.execute_script("arguments[0].click();", next_link[0])
            driver.implicitly_wait(1)
        else:
            next_page_ava = False

    return data

        

if __name__ == "__main__":
    # Command line tools
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword")
    
    args = parser.parse_args()

    # Crawling process
    driver = setup_webdriver(args.keyword)
    jobs = job_crawling(driver)
    driver.close()
    
    # Dumps to json file
    FOLDER = "some_samples_output"
    data = {}
    data["keyword"] = args.keyword
    data["jobs"] = jobs
    path_file = os.path.join(FOLDER, args.keyword + ".json")
    json.dump(data, open(path_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    

