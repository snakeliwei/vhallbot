# task.py
#!/usr/bin/env python3
# encoding: utf-8
# Author: lyndon

import os
import time
import asyncio
from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
from config import huey


async def meeting_join(url, data):
    options = webdriver.ChromeOptions()
    prefs = {'profile.content_settings.exceptions.plugins': {
                    "http://e.vhall.com:80,*": {
                        "last_modified": "13169358065549109",
                        "setting": 1
                    },
                    "http://live.vhall.com:80,*": {
                        "last_modified": "13171618834348431",
                        "setting": 1
                    },
                    "https://live.vhall.com:443,*": {
                        "last_modified": "13172056641866684",
                        "setting": 1
                    }
                }
            }
            
    options.add_experimental_option('prefs', prefs)
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    browser = webdriver.Chrome(chrome_options = options)
    browser.get(url)
    browser.implicitly_wait(10)
    browser.find_element_by_css_selector('#join-webinar').click()
    await asyncio.sleep(3)
    browser.switch_to.frame(browser.find_element_by_xpath(".//*[@class='layui-layer-content']/iframe"))
    browser.find_element_by_xpath(".//*[@class='input-name']/input").send_keys(data['name'])
    browser.find_element_by_xpath(".//*[@class='input-mobile']/input").send_keys(data['mobile'])
    browser.find_element_by_xpath(".//*[contains(@data-questions,'医院')]//textarea").send_keys(data['hosp'])
    browser.find_element_by_xpath(".//*[contains(@data-questions,'科室')]//textarea").send_keys(data['dept'])
    browser.find_element_by_xpath(".//*[contains(@data-questions,'职称')]//textarea").send_keys(data['title'])
    browser.find_element_by_xpath(".//*[@class='action']//input").click()
    await asyncio.sleep(60*5)
    browser.save_screenshot(data['mobile']+'.png')
    await asyncio.sleep(60*60*20)
    browser.quit()

@huey.task()
def addjob(url, users):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [meeting_join(url, user) for user in users]
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception as err:
        print(err)
    finally:    
        loop.close()
