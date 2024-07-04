from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

LINKEDIN_URL = "https://www.linkedin.com/login"
PROFILE_URL = "https://www.linkedin.com/in/nainia-mohammed-7655ab167/recent-activity/all/"
USERNAME = "nainiaaxie3@gmail.com"
PASSWORD = "Simo@1997"

def extract_hashtags(text):
    return re.findall(r'#\w+', text)

def scrape_linkedin_posts(profile_url, username, password):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(LINKEDIN_URL)
    wait = WebDriverWait(driver, 60)

    # Log in
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    print("Please complete CAPTCHA if required, then press Enter in the terminal...")
    input()

    print("Login completed. Navigating to the target profile activity page...")
    driver.get(profile_url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    posts = []
    NUM_POSTS_TO_SCRAPE = 10  # <---- Modify this value to change the number of posts to scrape
    while len(posts) < NUM_POSTS_TO_SCRAPE:
        print(f"Scrolling to load more posts... currently have {len(posts)} posts")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Click on "see more" buttons
        see_more_buttons = driver.find_elements(By.XPATH, "//*[@class='feed-shared-inline-show-more-text__see-more-less-toggle see-more t-14 t-black--light t-normal hoverable-link-text']")
        for button in see_more_buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(0.5)
            except:
                continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        feeds = soup.find_all("div", class_="feed-shared-update-v2")
        print(f"Found {len(feeds)} posts on this load")
        
        for feed in feeds:
            if len(posts) >= NUM_POSTS_TO_SCRAPE:
                break
            try:
                post_text = feed.select_one("span.break-words").get_text(strip=True) if feed.select_one("span.break-words") else ""
                hashtags = extract_hashtags(post_text)
                if not hashtags:
                    print("No hashtags found in post text:", post_text)
                likes = feed.select_one("span.social-details-social-counts__reactions-count").get_text(strip=True) if feed.select_one("span.social-details-social-counts__reactions-count") else "0"
                
                # Extracting comments using the provided regex pattern
                regex = re.compile('.*social-details-social-counts__comments.*')
                try:
                    comments = feed.find('li', {'class': regex}).get_text().replace('\n', '').replace(' ', '')
                except:
                    comments = "0"

                posts.append({
                    "text": post_text,
                    "hashtags": hashtags,
                    "likes": likes,
                    "comments": comments
                })
            except Exception as e:
                print(f"Error extracting post data: {e}")

    driver.quit()
    print("Browser closed.")
    
    # Convert the list of posts to a pandas DataFrame
    df = pd.DataFrame(posts)
    
    # Save the DataFrame to an Excel file
    excel_filename = "linkedin_posts.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Data saved to {excel_filename}")
    
    return excel_filename

if __name__ == "__main__":
    excel_file = scrape_linkedin_posts(PROFILE_URL, USERNAME, PASSWORD)
    print(f"Excel file created: {excel_file}")
