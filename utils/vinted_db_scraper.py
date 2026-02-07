from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from urllib.parse import urlencode
import json
import re

public_url = "https://www.vinted.it/catalog"
catalog_url = "https://www.vinted.it/api/v2/catalog/items"
items_url = "https://www.vinted.it/items"

additional_params = "per_page=10&page=1order=newest_first"

token_generator_url = f"{public_url}?search_text=shirt"

def syncScrapeVintedDb(query_data: dict[str, str]):
    query_data.setdefault("search_text", "shirt")
    query_data["search_text"] = query_data["search_text"].replace(" ", "+")
    query_data.update({
        "order": "price_low_to_high",
        "per_page": "960",
        "page": "1"
    })
    query = urlencode(query_data)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(token_generator_url)
        except:
            return []

        try:
            page.goto(f"{catalog_url}?{query}")
        except:
            return []
        
        element_text = page.text_content("pre")
        browser.close()

        res_obj = json.loads(str(element_text))["items"]

        return res_obj
    
async def asyncScrapeVintedDb(query_data: dict[str, str]):
    query_data.setdefault("search_text", "shirt")
    query_data["search_text"] = query_data["search_text"].replace(" ", "+")
    query_data.update({
        "order": "price_low_to_high",
        "per_page": "960",
        "page": "1"
    })
    query = urlencode(query_data)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(token_generator_url)
        except:
            return None

        try:
            await page.goto(f"{catalog_url}?{query}")
        except:
            return None

        element_text = await page.text_content("pre")
        await browser.close()

        res_obj = json.loads(str(element_text))["items"]
        return res_obj

def syncQueryVintedDb(query):
    url = f"{catalog_url}?{query}&{additional_params}"
    element_text = "{}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(token_generator_url)
        except:
            return []

        try:
            page.goto(url)
        except:
            return []
        
        element_text = page.text_content("pre")
        browser.close()

    return json.loads(str(element_text))["items"]

async def asyncQueryVintedDb(query):
    url = f"{catalog_url}?{query}&order=newest_first"
    element_text = "{}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(token_generator_url)
        except:
            return []

        try:
            await page.goto(url)
        except:
            return []
        
        element_text = await page.text_content("pre")
        await browser.close()

    return json.loads(str(element_text))["items"]

async def asyncGetItem(item_id):
    data = {
        "id": item_id,
        "url": f"{items_url}/{item_id}"
    }


    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(data["url"])
        except:
            return {}
        #uploaded = await page.text_content('[data-testid="item-attributes-upload_date"] span.web_ui__Text__bold')
        #price = await page.text_content('[data-testid="item-price"] p')
        #try: brand = await page.text_content('a[itemprop="url"] span[itemprop="name"]')
        #except: pass

        size = None
        conditions = None
        description = None
        rating = None
        aria_label = None
        reviews_number = None
        country_id = None

        try: size = await page.text_content('[data-testid="item-attributes-size"] span.web_ui__Text__bold', timeout=3000)
        except: print("error with size")
        try: conditions = await page.text_content('[data-testid="item-attributes-status"] span.web_ui__Text__bold', timeout=3000)
        except: print("error with conditions")
        try: description = await page.text_content('div[itemprop="description"] span.web_ui__Text__format > span', timeout=3000)
        except: print("error with descrtiption")
        try: aria_label = await page.get_attribute('div.web_ui__Rating__rating', 'aria-label', timeout=3000)
        except: print("error with aria label")
        try: reviews_number = await page.text_content('div.web_ui__Rating__label > span', timeout=3000) or "(0)"
        except: print("error with reviews number")
        
        try:
            if aria_label:
                match = re.search(r"valutazione di (\d(?:\.\d)?) su 5", aria_label)
                rating = match.group(1) if match else None
        except: print("error with rating extraction")


        await browser.close()

    data.update({
        #"uploaded": uploaded if uploaded else "",
        #"price": price if price else "",
        #"brand": brand if brand else "",
        "size": size if size else None,
        "conditions": conditions if conditions else None,
        "description": description if description else None,
        "rating": rating if rating else None,
        "reviews_number": reviews_number if reviews_number else None,
        "country": country_id if country_id else None
    })

    return data

def clean(text: str | None) -> str | None:
    if text:
        return text.strip()
    return None