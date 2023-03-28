from config import CONFIG
from model import Message
from swap import MESSAGE_QUEUE

from asyncio import CancelledError, sleep as asleep

from discord import ButtonStyle, Client, Intents, Interaction
from discord.ui import View, Button

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

ADMIN_CHANNEL = client.get_channel(CONFIG.discord.channel.admin)
BROADCAST_CHANNEL = client.get_channel(CONFIG.discord.channel.broadcast)


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
    if interaction.custom_id == "allow":
        pass
    else:
        pass
    await message.edit(
        content=content,
        view=None
    )


async def send_message():
    try:
        while True:
            if MESSAGE_QUEUE.empty():
                await asleep(1)
                continue
            message: Message = await MESSAGE_QUEUE.get()

            context = [
                f"Create Time: {message.create_time.isoformat()}",
                "-----Content Start-----",
                message.context,
                f"Sign: {message.sign}"
                "-----Content End-----",
            ]

            accept = Button(
                style=ButtonStyle.success,
                label="Allow",
                custom_id="allow"
            )
            block = Button(
                style=ButtonStyle.danger,
                label="Block",
                custom_id="block"
            )
            view = View(
                accept, block
            )

            await ADMIN_CHANNEL.send(
                content="\n\n".join(context),
                view=view
            )
    except CancelledError:
        return
