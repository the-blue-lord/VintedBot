import console
from utils.offers_processer import notify_offers

async def main(client):
    console.log(f"Logged in as {client.user} (ID: {client.user.id})")
    await notify_offers(client)


def register(client):
    @client.event
    async def on_ready():
        await main(client)

def unregister(client):
    @client.event
    async def on_ready():
        pass
