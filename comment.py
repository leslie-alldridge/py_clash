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

# open file with URLs
f=open("urls.txt", "r")
web_urls = f.read().splitlines()

session_id = driver.session_id
count = 0
# go to each url and find Laurens posts
for url in web_urls:
    # maintain the same session
    driver.session_id = session_id
    driver.get(url)
    sleep(3) 

    # go to laurens posts
    authors = driver.find_elements_by_css_selector("span[data-id='005o0000002mTivAAE']")

    if authors:
        
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
                
            
    else:
        print('No author found')
driver.close()

print('Done')

