import typing
import discord

from dish.configfile import ConfigFile


class Bot(discord.Client):
    def __init__(self, config: ConfigFile, **kwargs: typing.Any):
        super().__init__(**kwargs)
        self.config: ConfigFile = config

    async def on_ready(self):
        await self.config["postinit"](self)

    async def on_message(self, message: discord.Message):
        if await self.config["handler"](message):
            return
        if message.author == self.user:
            return

    def run(self):
        self.config["preinit"](self)
        super().run(self.config["token"])
