import typing
import discord

from dish.dishfile import DishFile


class ConfigFile(typing.TypedDict):
    token: str
    preinit: typing.Callable[[discord.Client], None]
    postinit: typing.Callable[[discord.Client], typing.Coroutine[typing.Any, typing.Any, None]]
    handler: typing.Callable[[discord.Message], typing.Coroutine[typing.Any, typing.Any, bool]]

    dishes: typing.List[DishFile | str]
