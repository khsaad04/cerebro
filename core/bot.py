import os
from logging import getLogger
from typing import Any, Union

from discord import Intents, Interaction, Message
from discord.ext import commands

from utils import Context, MyHelp

__all__ = ("Bot",)

log = getLogger("Bot")


class Bot(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any):
        help_command = MyHelp()
        super().__init__(
            command_prefix=commands.when_mentioned_or(">"),
            intents=Intents.all(),
            case_insensitive=True,
            help_command=help_command,
        )

    async def on_connect(self):
        log.info(f"Connected to discord as {self.user}(ID:{self.user.id})")

    async def on_disconnect(self):
        log.info("Bot disconnected")

    async def on_resumed(self):
        log.info("Bot resumed")

    async def on_ready(self):
        log.info("Bot ready")

    async def setup_hook(self):
        log.info("Running setup...")
        for file in os.listdir("./cogs"):
            if not file.startswith("_"):
                try:
                    await self.load_extension(f"cogs.{file}.plugin")
                except Exception as e:
                    log.info(f"Couldn't load {file}\n{e}")
        try:
            await self.load_extension("utils.error")
            log.info("Error handler ready")
        except Exception as e:
            log.info(f"Couldn't load error handler")
        synced_commands = await self.tree.sync()
        log.info(f"Synced {len(synced_commands)} commands")
        log.info("Setup complete.")

    async def get_context(self, origin: Union[Message, Interaction], *, cls=Context):
        return await super().get_context(origin, cls=cls)
