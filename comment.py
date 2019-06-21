from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from slack import sendSlack

# set up driver & get url
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=chrome_options)

url = 'https://central.xero.com/s/question/0D51N00004XQXg5SAH/xero-support'
driver.get(url)
sleep(3) 

# go to laurens posts
authors = driver.find_elements_by_css_selector("span[data-id='005o0000002mTivAAE']")

if authors:
    count = 0
    # go to each post
    for author in authors:
        if 'Lauren' in author.text:
            # scroll into view
            sleep(1)
            author.location_once_scrolled_into_view

            # expand post if it exists
            try:
                link = driver.find_element_by_link_text('Expand Post')
                link.click()
                image_name = 'image_' + str(count) + '.png'
                driver.save_screenshot(image_name)
                count += 1
                sendSlack(image_name, url)
            except :
                image_name = 'image_' + str(count) + '.png'
                driver.save_screenshot(image_name)
                count += 1
                sendSlack(image_name, url)
        else: pass
    driver.close()        
        
else:
    driver.close()

