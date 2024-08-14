import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path = r"C:\Windows\chromedriver-win64\chromedriver.exe" 
# Set up Chrome WebDriver to operate in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

# Initialize the WebDriver service
chrome_service = Service(driver_path)
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Set retry parameters for page loading attempts
max_retries = 3  # page loading
retry_delay = 10  # Delay in seconds between retry attempts

try:
    for attempt in range(1, max_retries + 1):
        print("Trying to load the website...")
        browser.get("https://hprera.nic.in/PublicDashboard")

        try:
            # Wait until a specific element is located on the page to confirm full loading
            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[onclick^='tab_project_main_ApplicationPreview']"))
            )
            print("Website loaded successfully.")
            break 
        except Exception as error:
            print(f"Attempt {attempt}: Page load failed. Retrying...")
            print(error)
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                print("Maximum retries reached. Please rerun the script.")
                browser.quit()
                exit()

    # Identify project cards on the webpage
    print("Searching for project cards...")
    project_elements = browser.find_elements(By.CSS_SELECTOR, "a[onclick^='tab_project_main_ApplicationPreview']")
    
    # Limit processing to the first 6 project cards found
    print(f"{len(project_elements)} projects found. Processing the first 6.")

    project_list = []

    for idx, project in enumerate(project_elements[:6]):
        print(f"Accessing details of project {idx + 1}...")
        project.click()

        try:
           
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//td[text()='Name']/following-sibling::td"))
            )
            
            
            project_name = browser.find_element(By.XPATH, "//td[text()='Name']/following-sibling::td").text
            project_pan = browser.find_element(By.XPATH, "//td[text()='PAN No.']/following-sibling::td/span").text
            project_gstin = browser.find_element(By.XPATH, "//td[text()='GSTIN No.']/following-sibling::td/span").text
            project_address = browser.find_element(By.XPATH, "//td[text()='Permanent Address']/following-sibling::td/span").text

            project_details = {
                "Name": project_name,
                "PAN No.": project_pan,
                "GSTIN No.": project_gstin,
                "Permanent Address": project_address
            }

            project_list.append(project_details)
        except Exception as error:
            print(f"Error extracting data from project {idx + 1}: {error}")

        try:
        
            close_btn = browser.find_element(By.XPATH, "//button[text()='Close']")
            if close_btn:
                close_btn.click()
                WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[onclick^='tab_project_main_ApplicationPreview']"))
                )
            else:
                browser.back()
                WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[onclick^='tab_project_main_ApplicationPreview']"))
                )
            print(f"Closed details view for project {idx + 1}")
        except Exception as error:
            print(f"Error closing details view for project {idx + 1}: {error}")

    
    project_df = pd.DataFrame(project_list)

    # Save the DataFrame to a CSV file
    output_filename = 'output.csv'
    project_df.to_csv(output_filename, index=False)

    print(f'CSV file "{output_filename}" has been successfully created.')

   
    print("\nCollected data from the first 6 projects:")
    print(project_df)

finally:
   
    print("Shutting down the browser...")
    browser.quit()
