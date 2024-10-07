from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os


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

def setup_driver():
    print(style.BLUE+"Setting up the WebDriver..."+style.RESET)
    options = Options()
    options.add_argument("--user-data-dir=/tmp/chrome-data")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def read_numbers(file_path):
    print(style.YELLOW+f"Reading phone numbers from {file_path}..."+style.RESET)
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def read_message(file_path):
    print(style.YELLOW+f"Reading message from {file_path}..."+style.RESET)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def send_message(driver, number, message):
    print(f"Preparing to send message to {number}...")
    url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
    driver.get(url)
    
    try:
        # Wait for the send button to be clickable
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-tab='11' and @aria-label='Send']"))
        )
        send_button.click()
        print(f"Message sent to {number}")
        sleep(5)  # Wait after sending each message
    except Exception as e:
        print(style.RED+f"Failed to send message to {number}. Error: {str(e)}"+style.RESET)

def main():
    numbers = read_numbers("numbers.txt")
    message = read_message("message.txt")
    
    print("Initializing WebDriver...")
    driver = setup_driver()

    
    
    print("Opening WhatsApp Web...")
    driver.get("https://web.whatsapp.com")
    input("Please scan the QR code and press Enter once WhatsApp Web is loaded...")
    
    for i, number in enumerate(numbers, 1):
        print(f"\nProcessing number {i} of {len(numbers)}")
        send_message(driver, number, message)
        sleep(10)  # Additional delay between numbers
    
    print("\nAll messages sent. Closing the browser...")
    driver.quit()

if __name__ == "__main__":
    main()