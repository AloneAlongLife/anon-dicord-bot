from config import CONFIG
from model import Message
from swap import MESSAGE_QUEUE

from asyncio import CancelledError, sleep as asleep
from typing import Optional

from discord import ButtonStyle, Client, Intents, Interaction
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
    message = interaction.message
    content = message.content
    print(interaction.data)
    if interaction.custom_id == "allow":
        pass
    else:
        pass
    # await message.edit(content=content, view=None)


async def send_message():
    channel = client.get_channel(CONFIG.discord.channel.admin)
    try:
        while True:
            if MESSAGE_QUEUE.empty():
                await asleep(1)
                continue
            message: Message = await MESSAGE_QUEUE.get()

            context = [
                f"Create Time: <t:{int(message.create_time.timestamp())}:R>",
                f"Sign: {message.sign}",
                "------",
                message.context,
                "------",
            ]

            accept = Button(style=ButtonStyle.success,
                            label="Allow", custom_id="allow")
            block = Button(style=ButtonStyle.danger,
                           label="Block", custom_id="block", )
            view = View(accept, block)

            await channel.send(content="\n".join(context), view=view)
    except CancelledError:
        return
