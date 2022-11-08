import shlex
import subprocess
import typing
import discord

from dish.configfile import ConfigFile, Dish


async def _default_postinit(_):
    return None


async def _default_handler(_):
    return False


class Bot(discord.Client):
    def __init__(self, config: ConfigFile, **kwargs: typing.Any):
        super().__init__(
            intents=discord.Intents(messages=True, message_content=True), **kwargs
        )
        self.config: ConfigFile = config
        self.dishes: typing.Dict[str, Dish]
        self._get_dishes()

    def _get_dishes(self):
        self.dishes: typing.Dict[str, Dish] = {}
        for command, dish in self.config.get("dishes", {}).items():
            self.dishes[command] = dish
            for alias in dish.get("aliases", []):
                self.dishes[alias] = dish

    async def on_ready(self):
        await self.config.get("postinit", _default_postinit)(self)

    async def on_message(self, message: discord.Message):
        if await self.config.get("handler", _default_handler)(message):
            return
        if message.author == self.user:
            return

        argv = shlex.split(message.content)
        if argv[0] in self.dishes.keys():
            argv = shlex.split(self.dishes[argv[0]]["run"]) + argv[1:]
            proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            await message.reply(f"```ansi\n" + proc.stdout.decode("utf-8") + "\n```")

    def run(self):
        self.config.get("preinit", lambda _: None)(self)
        super().run(self.config["token"])
