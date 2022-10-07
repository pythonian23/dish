import typing
import discord


class Config(typing.TypedDict):
    token: str
    preinit: typing.Callable[[discord.Client], None]
    postinit: typing.Callable[[discord.Client], typing.Coroutine[typing.Any, typing.Any, None]]
    handler: typing.Callable[[discord.Message], typing.Coroutine[typing.Any, typing.Any, bool]]
