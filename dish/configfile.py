from typing import *
import discord


class PermGroup(TypedDict):
    users: List[int]
    roles: List[int]


class Dish(TypedDict):
    aliases: List[str]
    description: str
    run: str

    permgroup: str
    ignore: bool


class ConfigFile(TypedDict):
    token: str
    preinit: Callable[[discord.Client], None]
    postinit: Callable[[discord.Client], Coroutine[Any, Any, None]]
    handler: Callable[[discord.Message], Coroutine[Any, Any, bool]]

    dishes: Dict[str, Dish]
    permgroups: Dict[str, PermGroup]
