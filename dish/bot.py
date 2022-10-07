import typing
import discord
import toml

from dish.configfile import ConfigFile
from dish.dishfile import DishFile


async def _default_postinit(_):
    return None


async def _default_handler(_):
    return False


class Bot(discord.Client):
    def __init__(self, config: ConfigFile, **kwargs: typing.Any):
        super().__init__(**kwargs)
        self.config: ConfigFile = config
        self.dishes: typing.List[DishFile]
        self._get_dishes()
        print(self.dishes)

    def _get_dishes(self):
        self.dishes = []
        for dish in self.config.get("dishes", []):
            if isinstance(dish, str):
                self.dishes.append(toml.load(dish, _dict=DishFile))
            else:
                self.dishes.append(dish)

    async def on_ready(self):
        await self.config.get("postinit", _default_postinit)(self)

    async def on_message(self, message: discord.Message):
        if await self.config.get("handler", lambda _: False)(message):
            return
        if message.author == self.user:
            return

    def run(self):
        self.config.get("preinit", lambda _: None)(self)
        super().run(self.config["token"])
