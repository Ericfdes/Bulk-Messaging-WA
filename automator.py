from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

#new
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from selenium.common.exceptions import StaleElementReferenceException


from time import sleep
from urllib.parse import quote
import os

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(style.BLUE)
print("Staring.....")
print(style.RESET)

f = open("message.txt", "r", encoding="utf8")
message = f.read()
f.close()

print(style.YELLOW + '\nThis is your message-')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)

numbers = []
f = open("numbers.txt", "r")
for line in f.read().splitlines():
	if line.strip() != "":
		numbers.append(line.strip())
f.close()
total_number=len(numbers)
print(style.RED + 'We found ' + str(total_number) + ' numbers in the file' + style.RESET)
delay = 30

# Initialize the WebDriver
# driver_path = ChromeDriverManager().install()
# driver = webdriver.Chrome(executable_path=driver_path, options=options)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
print('Once your browser opens up sign in to web whatsapp')
driver.get('https://web.whatsapp.com')
input(style.MAGENTA + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER..." + style.RESET)



# ... (rest of your imports and code)

def is_message_sent(driver):
    try:
        # Check for the presence of the "message sent" tick
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-testid='msg-dblcheck']"))
        )
        return True
    except:
        return False

for idx, number in enumerate(numbers):
    number = number.strip()
    if number == "":
        continue
    print(style.YELLOW + '{}/{} => Sending message to {}.'.format((idx+1), total_number, number) + style.RESET)
    try:
        url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
        sent = False
        for i in range(3):
            if not sent:
                driver.get(url)
                try:
                    # Wait for the input box
                    input_box = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
                    )
                    
                    # Clear any existing text in the input box
                    input_box.clear()
                    
                    # Type the message
                    input_box.send_keys(message)
                    
                    # Try to click the send button
                    try:
                        click_btn = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']"))
                        )
                        click_btn.click()
                    except (TimeoutException, ElementClickInterceptedException):
                        # If clicking fails, try sending with Enter key
                        input_box.send_keys(Keys.ENTER)
                    
                    # Check if the message was actually sent
                    if is_message_sent(driver):
                        sent = True
                        print(style.GREEN + 'Message sent to: ' + number + style.RESET)
                    else:
                        print(style.YELLOW + 'Message may not have been sent to: ' + number + style.RESET)
                    
                    sleep(3)
                except Exception as e:
                    print(style.RED + f"\nFailed to send message to: {number}, retry ({i+1}/3)")
                    print("Make sure your phone and computer are connected to the internet.")
                    print("If there is an alert, please dismiss it." + style.RESET)
                    print(f"Error: {str(e)}")
            
            if sent:
                break
        
        if not sent:
            print(style.RED + f"Failed to send message to {number} after 3 attempts." + style.RESET)
    
    except Exception as e:
        print(style.RED + 'Failed to send message to ' + number + str(e) + style.RESET)

driver.quit() # Use quit() instead of close() to ensure the browser is fully closed

# for idx, number in enumerate(numbers):
# 	number = number.strip()
# 	if number == "":
# 		continue
# 	print(style.YELLOW + '{}/{} => Sending message to {}.'.format((idx+1), total_number, number) + style.RESET)
# 	try:
# 		url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
# 		sent = False
# 		for i in range(3):
# 			if not sent:
# 				driver.get(url)
# 				try:
# 					click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']")))
# 				except Exception as e:
# 					print(style.RED + f"\nFailed to send message to: {number}, retry ({i+1}/3)")
# 					print("Make sure your phone and computer is connected to the internet.")
# 					print("If there is an alert, please dismiss it." + style.RESET)
# 				else:
# 					sleep(1)
# 					click_btn.click()
# 					sent=True
# 					sleep(3)
# 					print(style.GREEN + 'Message sent to: ' + number + style.RESET)
# 	except Exception as e:
# 		print(style.RED + 'Failed to send message to ' + number + str(e) + style.RESET)
# driver.close()
