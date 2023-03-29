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
    print("Start")
    client.loop.create_task(
        send_message(), name="Send message to admin channel.")


@client.event
async def on_interaction(interaction: Interaction):
    if interaction.channel_id != CONFIG.discord.channel.admin:
        return
    channel = client.get_channel(CONFIG.discord.channel.broadcast)
    message = interaction.message
    content = message.content
    if interaction.custom_id == "allow":
        reply_message = "Allow the message."
        edit_message = "\n".join(
            [
                content,
                f"Allow by {interaction.user.mention} <t:{int(datetime.now(CONFIG.tz).timestamp())}:R>.",
            ]
        )
        message = "\n".join([
            content,
            "匿名發言 >",
            "成為審查者 >"
        ])
        await channel.send(message)
    else:
        reply_message = "Block the message."
        edit_message = "\n".join(
            [
                content,
                f"Block by {interaction.user.mention} <t:{int(datetime.now(CONFIG.tz).timestamp())}:R>.",
            ]
        )
    await interaction.message.edit(content=edit_message, view=None)
    await interaction.response.send_message(reply_message, ephemeral=True)


async def send_message():
    channel = client.get_channel(CONFIG.discord.channel.admin)
    try:
        while True:
            if MESSAGE_QUEUE.empty():
                await asleep(1)
                continue
            message: Message = await MESSAGE_QUEUE.get()

            uuid = uuid1().hex
            
            embed = Embed(title="NCKU CSIE 112 匿名發言系統", color=0xbaff, timestamp=message.create_time)
            embed.set_author(name=message.sign)
            embed.add_field(name="內容", value=message.context)
            embed.set_footer(text=uuid)

            accept = Button(style=ButtonStyle.success,
                            label="Allow", custom_id="allow")
            block = Button(style=ButtonStyle.danger,
                           label="Block", custom_id="block", )
            view = View(accept, block)

            await channel.send(content=f"#{uuid}", embed=embed, view=view)
    except CancelledError:
        return
