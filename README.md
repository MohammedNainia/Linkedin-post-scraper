 LinkedIn Profile Scraper

This project automates the process of logging into LinkedIn, navigating to a specific user's profile, and scraping their recent posts, including text, hashtags, likes, and comments. The extracted data is then saved into an Excel file for easy analysis.

 Project Highlights
- Automated Login: Utilizes Selenium to securely log into LinkedIn.
- Profile Navigation: Automatically navigates to the specified profile’s recent activity page.
- Data Extraction: Scrapes post text, hashtags, likes, and comments using BeautifulSoup.
- Data Handling: Converts the scraped data into a structured pandas DataFrame.
- Output: Saves the extracted data into an Excel file for easy analysis.

 Technologies Used
- Selenium for browser automation
- BeautifulSoup for HTML parsing
- pandas for data manipulation
- Regular expressions for hashtag extraction

 Installation and Usage
1. Install the required packages:
   - `pip install selenium`
   - `pip install beautifulsoup4`
   - `pip install pandas`
   
2. Download and install the ChromeDriver that matches your Chrome version.

3. Update the script with your LinkedIn username, password, and the profile URL you want to scrape.

4. Run the script:
   - `python linkedin_scraper.py`

 Applications
- Social media analytics
- Content performance tracking
- Trend analysis

Feel free to check out the project and let me know if you have any questions or feedback. Happy to discuss and collaborate on further improvements!



 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements.


