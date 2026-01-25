import os
from dotenv import load_dotenv
import discord

import events
from utils.offers_processer import notify_offers

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
events.register_all(client)

token = os.getenv("TOKEN")

client.run(token if token else "")