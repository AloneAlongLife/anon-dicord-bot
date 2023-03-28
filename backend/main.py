from api import api
from bot import client
from config import CONFIG

from uvicorn import Config, Server

if __name__ == "__main__":

    config = Config(
        app=api,
        host=CONFIG.api.host,
        port=CONFIG.api.port
    )
    server = Server(config)

    client.loop.create_task(server.serve())

    client.run(CONFIG.discord.token)
