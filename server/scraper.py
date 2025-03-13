from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time

def linkedin_scraper(page_id: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = f"https://www.linkedin.com/company/{page_id}"
        driver.get(url)
        time.sleep(5) 

        soup = BeautifulSoup(driver.page_source, "html.parser")

        meta_title = soup.find("title")
        title = meta_title.text.strip() if meta_title else "No title found"


        meta_description = soup.find("meta", {"name": "description"})
        description = meta_description["content"].strip() if meta_description else "No description found"


        profile_pic = None
        try:
            img_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'EntityPhoto-square')]"))
            )
            profile_pic = img_element.get_attribute("src")
        except Exception:
            profile_pic = None

 
        followers = None
        if "followers on LinkedIn" in description:
            try:
                followers_text = description.split("followers on LinkedIn")[0].strip().split(" ")[-1]
                followers = int(followers_text.replace(",", ""))
            except ValueError:
                followers = None 

      
        data = {
            "page_id": page_id,
            "title": title,
            "url": url,
            "description": description,
            "profile_picture": profile_pic,
            "followers": followers,
            "scraped_at": datetime.now().isoformat(),
        }

        return data

    except Exception as e:
        print(f"Scraping failed: {e}")
        return None  

    finally:
        driver.quit()
