from typing import Optional

from discord import Embed, Member, app_commands
from discord.ext import commands

from cogs import Plugin
from cogs.Utility.views import CalculatorView, EmbedBuilderSelect, Template
from core import Bot
from utils import Context


class Utility(Plugin):
    """
    This is the Utility cog, it contains useful utility commands.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.hybrid_command(name="ping", description="Shows the latency of the bot.")
    async def ping_command(self, ctx: Context) -> None:
        await ctx.send(f"{self.bot.latency*1000:.2f} ms", create_embed=True)

    @commands.hybrid_command(name="embed", description="Embed builder")
    async def embed_constructor_command(self, ctx: Context) -> None:
        embed = Template.get_default_embed()
        view = EmbedBuilderSelect(embed=embed, ctx=ctx)
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(name="calc", description="Calculator made using buttons")
    async def calculator_command(self, ctx: Context) -> None:
        view = CalculatorView(ctx)
        embed = Embed(description="```                            \n \n ```")

        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(name="userinfo", description="Shows a user's information")
    @app_commands.describe(member="The person's info you want(leave empty for yours)")
    async def userinfo_command(self, ctx: Context, member: Optional[Member]) -> None:
        if not member:
            member = ctx.author

        embed = Embed(
            title="User Info", description=f"{member}'s user info", color=member.color
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Account created", value=member.created_at, inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at, inline=False)
        embed.add_field(
            name="Roles",
            value=", ".join([role.mention for role in member.roles][1:]),
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="avatar", description="Shows the avatar of the user")
    @app_commands.describe(member="The person's info you want(leave empty for yours)")
    async def avatar_command(self, ctx: Context, member: Optional[Member]) -> None:
        if not member:
            member = ctx.author

        embed = Embed(
            title="Avatar", description=f"{member}'s avatar", color=member.color
        )
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Utility(bot))
