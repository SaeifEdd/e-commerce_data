import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data_path = "data/raw/tunisianet_smartphones.csv"
num_pages = 5 #choose nb of pages to scrape

def init_driver():
    options = Options()
    options.binary_location = "./chrome-linux64/chrome"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    service = Service(executable_path="./chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_page(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.product-miniature"))
    )
    product_containers = driver.find_elements(By.CSS_SELECTOR, "article.product-miniature")

    product_names, product_links, product_references = [], [], []
    product_descriptions, product_images = [], []
    product_prices, product_availability = [], []

    for container in product_containers:
        try:
            name = container.find_element(By.CSS_SELECTOR, "h2.h3.product-title a")
            product_names.append(name.text)
            product_links.append(name.get_attribute("href"))

            try:
                ref = container.find_element(By.CSS_SELECTOR, "span.product-reference")
                product_references.append(ref.text.replace('[', '').replace(']', ''))
            except:
                product_references.append("N/A")

            try:
                desc = container.find_element(By.CSS_SELECTOR, "div[id^='product-description-short']")
                description = ' '.join(desc.get_attribute('textContent').split())
                product_descriptions.append(description)
            except:
                product_descriptions.append("N/A")

            try:
                img = container.find_element(By.CSS_SELECTOR, "img.center-block.img-responsive")
                product_images.append(img.get_attribute("src"))
            except:
                product_images.append("N/A")

        except Exception as e:
            print(f"Error extracting product: {e}")

    prices = [
        el.text.strip()
        for el in driver.find_elements(By.CSS_SELECTOR, "span.price")
        if el.text.strip()
    ]
    availability = [
        el.text.strip()
        for el in driver.find_elements(By.XPATH, "//div[@id='stock_availability']/span")
        if el.text.strip()
    ]

    product_prices.extend(prices)
    product_availability.extend(availability)

    return pd.DataFrame({
        "Product references": product_references,
        "descriptions": product_descriptions,
        "Product Name": product_names,
        "Price": product_prices,
        "Product URL": product_links,
        "Image URL": product_images,
        "availability": product_availability
    })


def scrape_all_pages(num_pages, base_url="https://www.tunisianet.com.tn/596-smartphone-tunisie"):
    driver = init_driver()
    all_dataframes = []
    try:
        for page in range(1, num_pages + 1):
            page_url = f"{base_url}?page={page}" if page > 1 else base_url
            print(f"Scraping {page_url}")
            df = scrape_page(driver, page_url)
            all_dataframes.append(df)
            time.sleep(5)
    finally:
        driver.quit()

    return pd.concat(all_dataframes, ignore_index=True)


def save_to_csv(df, data_path):
    df.to_csv(data_path, index=False)
    print(f"Saved data to {data_path}")

def extract_data(data_path):
    df = scrape_all_pages(num_pages)
    save_to_csv(df, data_path)

if __name__ == "__main__":
    extract_data()
