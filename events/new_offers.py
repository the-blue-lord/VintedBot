import console
import json

from utils.embed_builder import buildEmbed
from utils.vinted_db_scraper import asyncGetItem

async def main(client, offers):
    console.log(f"New offers detected:\n" + json.dumps([[r["url"] for r in offers[key]] for key in offers], indent=4))

    for key in offers:
        for offer in offers[key]:
            data = await asyncGetItem(offer["id"])
            offer.update(data)
            element = offer.get("element", {})

            publisher = element.get("user", {})
    

            image = element.get("photos", [{}])[0]
            image_link = image.get("url", "")
            publication_time = image.get("high_resolution", {}).get("timestamp", 0)

            embed = buildEmbed(
                country="IT",
                title=offer["title"],
                link=offer["url"],
                description=offer.get("description", None),

                user_url=publisher.get("profile_url", None),
                username=publisher.get("login", None),
                user_image_url=(publisher.get("photo", {}) or {}).get("url", None),

                publication_time=publication_time,
                size=offer.get("size", None),
                brand=element.get("brand_title", None),
                conditions=offer.get("conditions", None),
                reviews=f"{f"{offer.get("rating", "-")}/5" if f"{offer.get("rating", "-")}" != "None" else ""} ({offer.get("reviews_number", "-")})",
                price=offer.get("price", None),
                currency=offer.get("currency", None),

                image_url=image_link
            )
            for channel_id in offer["channels"]:
                channel = client.get_channel(int(channel_id))
                if channel:
                    await channel.send(embed=embed)

def register(client):
    @client.event
    async def on_new_offers(offers):
        await main(client, offers)

def unregister(client):
    @client.event
    async def on_new_offers(offers):
        pass
