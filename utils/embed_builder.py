import discord

def buildEmbed(
        country = "[countrycode]",
        title="[title]",
        link="https://example.com",
        description="[description]",

        username="[username]",
        user_image_url="https://i.imgur.com/3a1sUjo.png",
        user_url="https://example.com/user",

        publication_time=1618953630,
        size="/",
        brand="/",
        conditions="/",
        reviews="[reviews]",
        price=None,
        currency=None,

        image_url="https://images1.vinted.net/t/01_00790_jpx3odQxvjHAurLxrSssAuVf/f800/1769069810.webp?s=15b6ad2bd27ad015487a5b3d4015ae3d55ab1016"
    ):
    embed = discord.Embed(
        #title=f"({country}) {title} | {price} {currency}",
        title=f"{title} | {price} {currency}",
        url=link,
        description=description,
        color=discord.Color.green()
    )

    embed.set_image(url=image_url)

    embed.add_field(name="Caricato", value=f"<t:{publication_time}:R>", inline=True)
    embed.add_field(name="Taglia", value=size, inline=True)
    embed.add_field(name="Marca", value=brand, inline=True)
    embed.add_field(name="Codizioni", value=conditions, inline=True)
    embed.add_field(name="Recensioni", value=reviews, inline=True)
    embed.add_field(name="Prezo", value=(f"{price} {currency}" if price and currency else "/"), inline=True)

    embed.set_author(name=username, icon_url=user_image_url, url=user_url)

    return embed