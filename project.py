from playwright.sync_api import sync_playwright
import time
from thefuzz import fuzz
import sys
import re
import pandas as pd
from tabulate import tabulate

def get_products():
    product_list = []
    try:
        while True:
            product_name = input("Enter the product you want to compare (e.g., Amul Milk 1L): ")
            product_list.append(product_name)
    except KeyboardInterrupt:
        print("")
        return product_list

def initialize_result(product_list):
    return [{
        'Product Item': '',
        'Blinkit': sys.maxsize,
        'Swiggy Instamart': sys.maxsize,
        'Jio Mart': sys.maxsize,
    } for _ in product_list]

def extract_numeric_price(text):
    return float(re.sub(r'[^\d.]', '', text))

def get_details(product_list):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    final_result = initialize_result(product_list)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # Blinkit
        page.goto("https://blinkit.com/")
        print("")
        print("Browser launched and page loaded!\n")
        print("Page title:", page.title())
        page.get_by_placeholder("search delivery location").fill("Koramangala 5th Block, Bengaluru, Karnataka 560095")
        page.wait_for_selector('.LocationSearchList__LocationListContainer-sc-93rfr7-0.lcVvPT', state="visible")
        page.locator('.address-container-v1').first.click()
        time.sleep(5)

        print("Scraping data from Blinkit...")
        for i in range(len(product_list)):
            page.goto(f"https://blinkit.com/s/?q={product_list[i]}")
            final_result[i]['Product Item'] = product_list[i]
            query = product_list[i].split()
            quantity = query[-1]
            for j in range(20):
                page.wait_for_selector('div.tw-text-300.tw-font-semibold.tw-line-clamp-2', timeout=10000)
                item_blinkit = page.locator('div.tw-text-300.tw-font-semibold.tw-line-clamp-2').nth(j).inner_text()
                score = fuzz.token_set_ratio(item_blinkit.lower(), product_list[i].lower())
                if score > 60:
                    page.wait_for_selector('div.tw-text-200.tw-font-medium.tw-line-clamp-1', timeout=10000)
                    qty_item = page.locator('div.tw-text-200.tw-font-medium.tw-line-clamp-1').nth(j).inner_text()
                    qty_item.replace('ltr','l')
                    qty_score = fuzz.token_set_ratio(qty_item.lower(), quantity.lower())
                    if qty_score > 50 and ' x ' not in qty_item.lower():
                        page.wait_for_selector('div.tw-text-200.tw-font-semibold', timeout=5000)
                        price_item = page.locator('div.tw-text-200.tw-font-semibold').nth(j).inner_text()
                        price_num = float(re.sub(r'[^\d.]', '', price_item))
                        if price_num < final_result[i]['Blinkit']:
                            final_result[i]['Blinkit'] = price_num
        print("Data scraped from Blinkit\n")

        #Swiggy Instamart
        page.goto("https://www.swiggy.com/instamart")
        print("Page title:", page.title())
        page.locator('.D4XVE').click()
        page.get_by_placeholder('Search for area, street name…').fill('Koramangala 5th Block, Bengaluru, Karnataka 560095')
        page.wait_for_selector('._11n32', state="visible")
        page.locator('._11n32').first.click()
        time.sleep(3)
        page.locator('div._2xPHa._2qogK').click()


        print("Scraping data from Swiggy Instamart...")
        for i in range(len(product_list)):
            page.goto(f"https://www.swiggy.com/instamart/search?custom_back=true&query={product_list[i]}")
            query = product_list[i].split()
            quantity = query[-1]
            for j in range(20):
                page.wait_for_selector('div.sc-aXZVg.kyEzVU._1sPB0', timeout=10000)
                item_swiggy = page.locator('div.sc-aXZVg.kyEzVU._1sPB0').nth(j).inner_text()
                score = fuzz.token_set_ratio(item_swiggy.lower(), product_list[i].lower())
                if score > 60:
                    page.wait_for_selector('div.sc-aXZVg.entQHA._3eIPt', timeout=10000)
                    qty_item = page.locator('div.sc-aXZVg.entQHA._3eIPt').nth(j).inner_text()
                    qty_item.replace('ltr','l')
                    qty_score = fuzz.token_set_ratio(qty_item.lower(), quantity.lower())
                    if qty_score > 50 and ' x ' not in qty_item.lower():
                        page.wait_for_selector('div.sc-aXZVg.jLtxeJ._1bWTz', timeout=5000)
                        price_item = page.locator('div.sc-aXZVg.jLtxeJ._1bWTz').nth(j).inner_text()
                        price_num = float(re.sub(r'[^\d.]', '', price_item))
                        u = final_result[i]
                        if price_num < u['Swiggy Instamart']:
                            u['Swiggy Instamart'] = price_num
        print("Data scraped from Swiggy Instamart\n")

        #Jio Mart
        page.goto("https://www.jiomart.com/")
        print("Page title:", page.title())
        page.get_by_text('Select Location Manually').click()
        u = page.get_by_placeholder('Search for area, landmark')
        u.click()
        u.type('Koramangala 5th Block, Bengaluru, Karnataka 560095', delay=50)
        page.get_by_text("5th Block, KHB Colony, 5th Block, Koramangala, Bengaluru").first.click()
        page.get_by_text(' Confirm Location ').click()

        print("Scraping data from JioMart...")
        for i in range(len(product_list)):
            page.goto(f"https://www.jiomart.com/search/{product_list[i]}")
            for j in range(10):
                item_jio = page.locator('.plp-card-details-name.line-clamp.jm-body-xs.jm-fc-primary-grey-80').nth(j).inner_text()
                score = fuzz.token_set_ratio(item_jio.lower(), product_list[i].lower())
                if score > 60:
                    price_item = page.locator('.jm-heading-xxs.jm-mb-xxs').nth(j).inner_text()
                    price_num = float(re.sub(r'[^\d.]', '', price_item))
                    u = final_result[i]
                    if price_num < u['Jio Mart']:
                        u['Jio Mart'] = price_num
        print("Data scraped from JioMart\n")

        print("Inserting data into database...")
        #Output
        with open("Grocer_Spy.txt","w") as f:
            sys.stdout = f
            df = pd.DataFrame(final_result)

            platforms = ['Blinkit', 'Swiggy Instamart', 'Jio Mart']
            df['Best Platform'] = df[platforms].idxmin(axis=1)

            print(tabulate(df, headers=['Product name', 'Blinkit', 'Swiggy Instamart', 'Jio Mart', 'Best Platform'],
                                         tablefmt= 'outline',stralign='center', numalign='center'))

        print("Data successfully saved to Price_Scrapper.db")

def main():
    product_list = get_products()
    get_details(product_list)

if __name__ == "__main__":
    main()
