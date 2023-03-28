from datetime import timedelta, timezone
from os.path import isfile
from typing import Union

from orjson import loads, dumps, OPT_INDENT_2
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
    tz: timezone = Field(alias="timezone")

    @validator("timezone", pre=True)
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
        config_file.write(dumps(config, option=OPT_INDENT_2))

CONFIG = Config(**config)
