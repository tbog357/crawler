# Crawling tool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def crawl_summary(job_data, job_element):
    job_title = job_element.find_element(By.CSS_SELECTOR, ".job-title")
    job_data["job_title"] = job_title.text
    job_data["link"] = job_title.get_attribute("href")

    # company_name
    company_name = job_element.find_element(By.CSS_SELECTOR, ".mt-1.company-name")
    job_data["company_name"] = company_name.text
    
    # location
    location = job_element.find_element(By.CSS_SELECTOR, ".location")
    job_data["location"] = location.text

    # posted_date
    posted_date = job_element.find_element(By.CSS_SELECTOR, ".posted-date")
    job_data["posted_date"] = posted_date.text

    # remaining_days
    remaining_days = posted_date.find_element(By.CSS_SELECTOR, "span > strong")
    job_data["remaining_days"] = remaining_days.text
    return job_data, job_title

def crawl_detail(driver, job_data):
    # Assume crawling on new tab
    # description
    job_description = driver.find_element(By.CSS_SELECTOR, ".job-description > .description").text
    job_data["job_description"] = job_description

    # requirements
    job_requirements = driver.find_element(By.CSS_SELECTOR, ".job-requirements > .requirements").text
    job_data["job_requirements"] = job_requirements

    # address  
    address = driver.find_element(By.CSS_SELECTOR, ".job-locations > .location").text
    job_data["address"] = address

    return job_data