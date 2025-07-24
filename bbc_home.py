from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Set up Selenium WebDriver (automatically)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # uncomment to run headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the page
driver.get("https://www.bbc.com")

# Prepare CSV file (added Image Link column)
csv_file = open(r"D:\Python\New_folder\bbc_home.csv", mode="w", newline="", encoding="utf-8-sig")
writer = csv.writer(csv_file)
writer.writerow(["Heading", "Link", "Image Link"])  # CSV headers

# Wait for at least one headline element to appear
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//h2[@data-testid="card-headline"]'))
)

# Find all headline elements
h2_elements = driver.find_elements(By.XPATH, '//h2[@data-testid="card-headline"]')

# Extract heading, link, and image link
for idx, h2 in enumerate(h2_elements, start=1):
    heading = h2.text.strip()
    link = None
    image_link = ""  # default empty if no image found

    try:
        # Find closest ancestor <a> tag for the link
        link_element = h2.find_element(By.XPATH, "./ancestor::a[1]")
        link = link_element.get_attribute("href")

        # Try to find an <img> inside the <a> tag
        try:
            img_element = link_element.find_element(By.XPATH, ".//img")
            image_link = img_element.get_attribute("src")
        except:
            # If not found, try searching nearby grandparent div for an image
            try:
                grandparent = h2.find_element(By.XPATH, "./ancestor::div[3]")
                img_element = grandparent.find_element(By.XPATH, ".//img")
                image_link = img_element.get_attribute("src")
            except:
                pass  # no image found nearby
    except:
        pass  # no link found

    if heading and link:
        print(f"{idx}. {heading} -> {link} | Image: {image_link}")
        writer.writerow([heading, link, image_link])

# Close CSV file and quit browser
csv_file.close()
driver.quit()
