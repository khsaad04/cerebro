from typing import Any, List, Mapping, Optional

import discord
from discord import Embed, SelectOption
from discord.ext.commands import Cog, Command, Group, HelpCommand

__all__ = ("MyHelp",)


class MyHelpEmbed(Embed):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.color = 0xC246B3
        text = "Use help [command] or help [category] for more information\n<> is required | [] is optional"
        self.set_footer(text=text)


class MyHelp(HelpCommand):
    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command]]):
        embed = MyHelpEmbed(title="Help", description="Cerebro's help command")
        embed.set_thumbnail(url=self.context.me.display_avatar)
        for cog, command in mapping.items():
            filtered = await self.filter_commands(command, sort=True)
            command_names = [c.qualified_name for c in filtered]
            if command_names:
                cog_name = getattr(cog, "qualified_name", "Misc")
                embed.add_field(
                    name=cog_name,
                    value="```\n" + "\n".join(command_names) + "```",
                    inline=True,
                )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog: Cog):
        embed = MyHelpEmbed(
            title=f"**{cog.qualified_name}**" or "Misc",
            description=cog.description or "`Yet to document`",
        )
        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                embed.add_field(
                    name=command.name,
                    value=self.get_command_signature(command),
                    inline=False,
                )
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group: Group):
        embed = MyHelpEmbed(title=group.qualified_name)
        embed.description = group.description or "`Yet to document`"
        for commands in group.walk_commands():
            embed.add_field(
                name=commands.qualified_name,
                value="\n".join([commands.signature, commands.description]),
            )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command: Command):
        embed = MyHelpEmbed(title=command.qualified_name)
        embed.description = command.description or "`Yet to document`"
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        embed.add_field(name="Usage", value=self.get_command_signature(command))
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error: str):
        embed = Embed(
            title="Not Found",
            description=f"```py\n{error}```",
            color=discord.Color.red(),
        )

        channel = self.get_destination()
        await channel.send(embed=embed)
