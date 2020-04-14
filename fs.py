#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import os
import urllib
import time
#sys.setdefaultencoding('utf-8')
import unidecode
# apt-get install python-mysql.connector

def get_os_path():
    disk = "e:"
    main_folder = "Py"
    project_category = "fs-analysis"
    project_output_folder = "fs"
    return os.path.join(disk + os.sep, main_folder, project_category, project_output_folder)

def getList(): 
    with open('stock_list_ETF.txt','r') as txt:
        stock_list = []
        stock_list = txt.read().split('\n')
    return stock_list

def write_data(data = "", file_name = "", switch = 0): 
    with open(file_name,'a') as txt:
        buf_1 = data
        txt.write(buf_1)
        if switch == 1:
            txt.write(",")
        else: 
            txt.close()
    return txt.close()

def getFinancialStatements(reportID):
        stock_list = getList();
        output_error_file_name = os.path.join(get_os_path(), 'err.txt')

        for ticker in stock_list:
            output_file_name = os.path.join(get_os_path(), ticker + "_" + reportID + ".csv")
            url = "http://finance.vietstock.vn/" + ticker + "/tai-chinh.htm"
            driver = webdriver.PhantomJS()
            driver.get(url)

            # Wait for 10 seconds until the desired tab is clickable
            WebDriverWait(driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="' + reportID + '"]')))

            driver.find_element(by = 'id', value = reportID).click()
            driver.implicitly_wait(1)
            driver.find_element_by_xpath('//*[@id="BR_selectTimeLevel"]/option[1]').click()
            driver.implicitly_wait(1)
            driver.find_element_by_xpath('//*[@id="viewRpt"]').click()
            driver.implicitly_wait(5)
        
            try:
                driver.implicitly_wait(15)
                WebDriverWait(driver, timeout=10).until(
                    EC.text_to_be_present_in_element((By.ID,'BR_tBody'), 'B. V'))

                for tr in driver.find_elements_by_xpath('//*[@id="BR_tBody"]//tr'):
                    td = tr.find_elements_by_tag_name('td')
                    for cell in td:
                        cell = unidecode.unidecode(cell.text)   
                        cell = cell.replace(',', '').strip()
                        write_data(cell, output_file_name, 1)
                    write_data("\n", output_file_name)
                print ticker + "_" + reportID + " downloaded successfully."

            except TimeoutException:
                write_data(ticker + "_" + reportID + " downloaded failed: Timeout Exception", output_error_file_name)
                write_data("\n", output_error_file_name)

            except StaleElementReferenceException:
                write_data(ticker + "_" + reportID + " downloaded failed: Stale Element Reference Exception", output_error_file_name)
                write_data("\n", output_error_file_name)

            time.sleep(2)
            driver.close()

def main():
    print "Downloading data..."
    getFinancialStatements('CDKT')

main()