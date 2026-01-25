import console

async def main(client, message):
    if message.author == client.user:
        return
    
    console.log(f"Received message: {message.content}")
    
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

def register(client):
    @client.event
    async def on_message(message):
        await main(client, message)

def unregister(client):
    @client.event
    async def on_ready():
        pass
        