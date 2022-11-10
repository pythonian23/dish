import shlex
import subprocess
import typing

import discord

from dish.configfile import ConfigFile, Dish


async def _default_postinit(_):
    return None


async def _default_handler(_):
    return False


async def respond(msg: discord.Message, content: str, client: discord.Client):
    lines = content.splitlines(keepends=True)
    buf = ""
    for line in lines:
        if len(buf) + len(line) + 12 > 2000:
            msg = await msg.reply(f"```ansi\n{buf}\n```", mention_author=False)
            msg = client.get_message(msg.id)
            buf = ""
        buf += line
    if buf:
        await msg.reply(f"```ansi\n{buf}\n```", mention_author=False)


class Bot(discord.Client):
    def __init__(self, config: ConfigFile, **kwargs: typing.Any):
        super().__init__(
            intents=discord.Intents(messages=True, message_content=True),
            **kwargs,
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

    async def on_message(self, msg: discord.Message):
        if await self.config.get("handler", _default_handler)(msg):
            return
        if msg.author == self.user:
            return

        argv = shlex.split(msg.content)
        if argv[0] in self.dishes.keys():
            argv = shlex.split(self.dishes[argv[0]]["run"]) + argv[1:]
            proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            out = proc.stdout.decode("utf-8")
            err = proc.stderr.decode("utf-8")
            if proc.returncode != 0:
                await respond(msg, f"Error: {proc.returncode}\n\n{err}", self)
            else:
                await respond(msg, out, self)

    def run(self):
        self.config.get("preinit", lambda _: None)(self)
        super().run(self.config["token"])
