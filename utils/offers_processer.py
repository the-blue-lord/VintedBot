import json
from hashlib import md5
import time

import console
import utils.vinted_db_scraper as scraper

async def notify_offers(client):
    while True:
        offers = await check_new_offers()
        if not offers: continue
        if len([offers[key] for key in offers if len(offers[key])]): client.dispatch("new_offers", offers)
        time.sleep(5)

async def check_new_offers(searches = None):
    settings = {}
    with open("settings.json", "r") as f:
        settings = json.load(f)

    if not searches: searches = settings["searches"]
    if not searches:
        console.error("No searches to execute were found")
        return {}

    all_new_offers = {}
    for search_data in searches:
        try:
            search_results = await executeSearch(search_data, all_new_offers)

            if not search_results:
                return

            all_new_offers.update(search_results)
            console.log(f"New offers so far: {json.dumps(all_new_offers, indent=4)}" + "\n", list(search_results.keys())[0])

        except Exception as e:
            console.error(f"Error while checking offers: {e}")

    console.log("Returning all new offers")
    return all_new_offers

async def executeSearch(search_data, new_offers_retrived, testing_active = False, testing_results = []):
    search = search_data["query"]
    if not search:
        console.error("No search to execute was found")
        return None
    md5_hash = md5(str(search_data).encode()).hexdigest()
    if md5_hash in new_offers_retrived:
        new_result_object = new_offers_retrived[md5_hash]
        new_result_object["channels"] += [search_data["channel"]]
        return {md5_hash: new_result_object}
    console.log(f"--- Checking search: {search} ------------------------------", md5_hash)
    filename = f"cache/{md5_hash}.json"
    console.log(f"Search hash: {md5_hash}" + "\n", md5_hash)

    cached_list = []

    try:
        # retrive old offers
        with open(filename, "r") as f:
            cached_data = json.load(f)

        cached_list = [x for x in cached_data["items"]]
        console.log(f"Cached offers found: {len(cached_list)}", md5_hash)
        console.log(f"Cache contents: {cached_list}" + "\n", md5_hash)

    except FileNotFoundError:
        cached_data = {}
        cached_list = []
        console.log("No cached offers found.", md5_hash)

    cached_min_id = cached_data["min"] if cached_data else 0

    # retrive current offers
    raw_data =  await scraper.asyncQueryVintedDb(search) if not testing_active else testing_results


    if not raw_data:
        console.error("No offers found.", md5_hash)
        return None

    scraped_data = {
        str(item["id"]): {
            "id": str(item["id"]),
            "title": item["title"],
            "price": item["price"]["amount"],
            "currency": item["price"]["currency_code"],
            "url": item["url"],
            "channels": [search_data["channel"]],
            "element": item
        }
        for item in raw_data
    }

    console.log(f"Current offers found: {len(raw_data)}", md5_hash)
    console.log(f"Current contents: {[element['id'] for element in raw_data]}" + "\n", md5_hash)

    new_offers = []

    whitelist = search_data.get("white_list", [])
    blacklist = search_data.get("black_list", [])

    if cached_list:
        # check what current offers are not in cache
        new_offers = [scraped_data[key] for key in scraped_data
            if int(key) > int(cached_min_id)
            and len([x for x in whitelist if str(x).lower() not in str(scraped_data[key]["title"]).lower()]) == 0
            and len([x for x in blacklist if str(x).lower() in str(scraped_data[key]["title"]).lower()]) == 0
        ]

    console.log(f"New offers found: {len(new_offers)}", md5_hash)

    # current offers to cache
    scraped_ids = [key for key in scraped_data]

    min_id = scraped_ids[0]

    with open(filename, "w") as f:
        json.dump({
            "min": min_id,
            "items": scraped_data
        }, f, indent=4)

    console.log(f"\nCache updated: {len(scraped_ids)} offers saved." + "\n" + f"Cache contents: {scraped_ids}" + "\n\n", md5_hash)

    return {md5_hash: new_offers}