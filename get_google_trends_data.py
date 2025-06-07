import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random

# Random wait time to mimic human behavior


def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder created at: {folder_path}")

# def download_google_trends_data(keywords, folder_path):
#     # Set up the Chrome WebDriver
#     USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
#     ]

#     # Set up Selenium WebDriver with stealth mode
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run in headless mode
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--window-size=1920x1080")
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")  # Random user agent

#     # Path to Chrome WebDriver
#     chrome_driver_path = "path/to/chromedriver"  # UPDATE THIS PATH
#     service = Service(chrome_driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     for keyword in keywords:
#         # Navigate to Google Trends
#         time.sleep(random.randint(5, 15))
#         keyword = keyword.replace(' ', '%20')
#         driver.get('https://trends.google.com/trends/explore?hl=en-US')

#         print(driver.title)

#         # search_btn = driver.find_element(By.XPATH, '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
#         # driver.get(f'https://trends.google.com/trends/explore?q={keyword}&date=now%201-d&geo=GB&hl=en-US')

#         # explore_btn = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[4]/div[1]/c-wiz[1]/div/div[1]/div[3]/div/div/div[3]/div/button')
#         # explore_btn.click()
#         # print(driver.title)

#         # Search for the keyword
#         # search_box = driver.find_element(By.XPATH, '//*[@id="input-24"]')
#         # search_box.click()
#         # search_box.send_keys(keyword)
#         # search_box.send_keys(Keys.RETURN)

#         # Wait for the page to load
#         time.sleep(random.randint(5, 15))
#         print(driver.title)

#         # click the "country" dropdown
#         country_dropdown = driver.find_element(By.XPATH, '//*[@id="compare-pickers-wrapper"]/div/hierarchy-picker[1]/ng-include/div[1]')
#         country_dropdown.click()

#         # Select the desired country
#         country_input = driver.find_element(By.XPATH, '//*[@id="input-8"]')
#         country_input.send_keys(country)
#         country_click = driver.find_element(By.XPATH, '//*[@id="ul-156"]/li/md-autocomplete-parent-scope/div')
#         country_click.click()

#         # Click on the "Download" button to download the CSV file
#         download_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')
#         download_button.click()

#         # Wait for the download to complete
#         time.sleep(5)

#         # Move the downloaded file to the specified folder
#         download_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'multiTimeline.csv')
#         new_file_path = os.path.join(folder_path, f'{keyword}.csv')
#         os.rename(download_path, new_file_path)
#         print(f"Downloaded and moved file to: {new_file_path}")

#     # Close the WebDriver
#     driver.quit()

# # Example usage
# virus = 'flu'
# country = 'United States'
# folder_country = country.lower().replace(' ', '_')
# keywords = ['flu', 'influenza', 'flu symptoms']

# folder_path = f'/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/{virus}_{folder_country}_raw_data'
# create_folder(folder_path)
# download_google_trends_data(keywords, folder_path)



# Set up the Chrome WebDriver
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
]

# Set up Selenium WebDriver with stealth mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--log-level=3")  # Suppress logs
chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")  # Random user agent

# Path to Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)


# List of keywords & countries
keywords = ["flu symptoms", "covid cases", "pneumonia symptoms"]
countries = ["US", "GB", "IN"]

# Output folder
output_folder = "google_trends_data"
os.makedirs(output_folder, exist_ok=True)

def fetch_trends(keyword, country):
    """Fetch Google Trends data while avoiding rate limits."""
    print(f"Fetching {keyword} in {country}...")

    try:
        # Open Google Trends
        driver.get("https://trends.google.com/trends/explore")
        time.sleep(random.uniform(5, 10))  # Random delay

        # Search keyword
        search_box = driver.find_element(By.XPATH, "//input[@class='placeholder']")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(random.uniform(5, 10))

        # Select country
        country_dropdown = driver.find_element(By.XPATH, "//div[contains(text(),'Worldwide')]")
        country_dropdown.click()
        time.sleep(random.uniform(3, 6))

        country_option = driver.find_element(By.XPATH, f"//div[contains(text(),'{country}')]")
        country_option.click()
        time.sleep(random.uniform(5, 10))

        # Download CSV (wait longer to avoid detection)
        download_button = driver.find_element(By.XPATH, "//button[contains(text(),'Download')]")
        download_button.click()
        time.sleep(random.uniform(10, 15))  # Extended delay for downloading

        # Move CSV file
        download_path = os.path.expanduser("~/Downloads")
        csv_file = os.path.join(download_path, f"{keyword.replace(' ', '_')}_{country}.csv")

        if os.path.exists(csv_file):
            new_path = os.path.join(output_folder, f"{keyword.replace(' ', '_')}_{country}.csv")
            os.rename(csv_file, new_path)
            print(f"✅ Saved: {new_path}")
        else:
            print(f"⚠️ CSV not found for {keyword} in {country}")

    except Exception as e:
        print(f"❌ Error fetching {keyword} in {country}: {str(e)}")

    # Random sleep to avoid getting blocked
    sleep_time = random.uniform(15, 30)
    print(f"Sleeping for {sleep_time:.2f} seconds to avoid detection...")
    time.sleep(sleep_time)

# Run scraper with delays
for keyword in keywords:
    for country in countries:
        fetch_trends(keyword, country)

# Close the browser
driver.quit()
print("🎉 Data collection completed!")