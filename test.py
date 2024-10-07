from selenium import webdriver


try:
    
    browser = webdriver.Chrome()
    browser.get('http://selenium.dev/')

except Exception as e:
    print(e)