from datetime import timedelta, timezone
from os.path import isfile
from typing import Union

try:
    from orjson import loads as rl, dumps as rd, OPT_INDENT_2
    loads = rl
    dumps = lambda x: rd(x, option=OPT_INDENT_2)
except:
    from json import loads as rl, dumps as rd
    loads = rl
    dumps = lambda x: rd(x, indent=2, ensure_ascii=False).encode()

from pydantic import BaseModel, Field, validator


class DiscordChannelConfig(BaseModel):
    admin: int
    broadcast: int


class DiscordConfig(BaseModel):
    token: str
    channel: DiscordChannelConfig


class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class Config(BaseModel):
    discord: DiscordConfig
    api: APIConfig
    tz: float = Field(alias="timezone")

    @validator("tz")
    def timezone_validator(cls, value: Union[timezone, timedelta, float]):
        if type(value) is timedelta:
            value = timezone(value)
        else:
            value = timezone(timedelta(hours=value))
        return value


if isfile("config.json"):
    with open("config.json", mode="rb") as config_file:
        config = loads(config_file.read())
else:
    print("Config not found...")
    config = {
        "discord": {
            "token": input("Enter discord bot token > "),
            "channel": {
                "admin": int(input("Enter admin channel id > ")),
                "broadcast": int(input("Enter broadcast channel id > ")),
            },
        },
        "api": {
            "host": input("Set api host (default: 0.0.0.0) >") or "0.0.0.0",
            "port": int(input("Set api port (default: 8080) >") or 8080),
        },
        "timezone": float(input("Set timezone (hours)(default: 8) >") or 8)
    }
    with open("config.json", mode="wb") as config_file:
        config_file.write(dumps(config))

CONFIG = Config(**config)
