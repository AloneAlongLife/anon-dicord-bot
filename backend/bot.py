from config import CONFIG
from model import Message
from swap import MESSAGE_QUEUE

from asyncio import CancelledError, sleep as asleep
from datetime import datetime
from uuid import uuid1

from discord import ButtonStyle, Client, Embed, Intents, Interaction
from discord.ui import View, Button

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)


@client.event
async def on_ready():
    client.loop.create_task(
        send_message(), name="Send message to admin channel.")


@client.event
async def on_interaction(interaction: Interaction):
    if interaction.channel_id != CONFIG.discord.channel.admin:
        return
    channel = client.get_channel(CONFIG.discord.channel.broadcast)

    message = interaction.message
    embed = message.embeds[0]
    if interaction.custom_id == "allow":
        new_embed = embed.copy()
        embed.color = 0x00ff00
        embed.add_field(name="Operation", value=f"Allow by {interaction.user.mention}")
        reply_message = "Allow the message."
        await channel.send(embed=new_embed)
    else:
        embed.color = 0xff0000
        embed.add_field(name="Operation", value=f"Block by {interaction.user.mention}")
        reply_message = "Block the message."
    await interaction.message.edit(embed=embed, view=None)
    await interaction.response.send_message(reply_message, ephemeral=True)


async def send_message():
    channel = client.get_channel(CONFIG.discord.channel.admin)
    try:
        while True:
            if MESSAGE_QUEUE.empty():
                await asleep(1)
                continue
            message: Message = await MESSAGE_QUEUE.get()

            uuid = str(uuid1())
            # uuid = uuid1().hex
            
            embed = Embed(title="NCKU CSIE 112 Anonymous Message", color=0xbaff, timestamp=message.create_time)
            embed.set_author(name=message.sign, icon_url=client.user.display_avatar.url)
            embed.add_field(name="Content", value=message.context)
            embed.set_footer(text=f"UUID: {uuid}")

            accept = Button(style=ButtonStyle.success,
                            label="Allow", custom_id="allow")
            block = Button(style=ButtonStyle.danger,
                           label="Block", custom_id="block", )
            view = View(accept, block)

            await channel.send(embed=embed, view=view)
    except CancelledError:
        return
