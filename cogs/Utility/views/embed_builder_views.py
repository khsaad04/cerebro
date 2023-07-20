from __future__ import annotations

from typing import Any

import discord
from discord import ButtonStyle, Embed, Interaction, SelectOption
from discord.ui import Button, Modal, Select, TextInput, View, button, select

from utils import Context

__all__ = (
    "Template",
    "EmbedBuilderSelect",
)


class EmbedBuilderSelect(View):
    def __init__(self, embed: Embed, ctx: Context):
        super().__init__()
        self.embed: Embed = embed
        self.ctx: Context = ctx

    @select(
        placeholder="Edit your embed",
        options=[
            SelectOption(label="Title and description", value="td"),
            SelectOption(label="Color", value="color"),
            SelectOption(label="Url", value="url"),
            SelectOption(label="Image", value="image"),
            SelectOption(label="Thumbnail", value="thumbnail"),
            SelectOption(label="Author", value="author"),
            SelectOption(label="Footer", value="footer"),
            SelectOption(label="Add field", value="field"),
            SelectOption(label="Remove field", value="rfield"),
        ],
        max_values=1,
        row=0,
    )
    async def select_callback(self, interaction: Interaction, select: Select):
        match select.values[0]:
            case "td":
                await Template.set_title_description(self.embed, interaction)
            case "color":
                await Template.set_color(self.embed, interaction)
            case "url":
                await Template.set_url(self.embed, interaction)
            case "image":
                await Template.set_image(self.embed, interaction)
            case "thumbnail":
                await Template.set_thumbnail(self.embed, interaction)
            case "author":
                await Template.set_author(self.embed, interaction)
            case "footer":
                await Template.set_footer(self.embed, interaction)
            case "field":
                await Template.add_field(self.embed, interaction)
            case "rfield":
                await Template.remove_field(self.embed, interaction)
        await interaction.message.edit(
            embed=self.embed, view=EmbedBuilderSelect(embed=self.embed, ctx=self.ctx)
        )

    @button(label="Done", style=ButtonStyle.green, row=1)
    async def done_callback(self, interaction: Interaction, button: Button):
        view = View()
        view.add_item(ChannelSelect(embed=self.embed))
        await interaction.message.edit(
            content="Where would you like to send the embed?", embed=None, view=view
        )

    @button(label="Cancel", style=ButtonStyle.danger, row=1)
    async def cancel_callback(self, interaction: Interaction, button: Button):
        await interaction.response.defer()
        for childrens in self.children:
            childrens.disabled = True

        await interaction.message.edit(content="Aight", embed=None, view=self)

    async def interaction_check(self, interaction: Interaction):
        if interaction.user != self.ctx.author:
            interaction.response.send_message(
                "Let bro do his thing, you can use your own builder", ephemeral=True
            )
            return False
        else:
            return True


class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self, embed: Embed, *args: Any, **kwargs: Any):
        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Select channel...",
            max_values=1,
            *args,
            **kwargs,
        )
        self.embed: Embed = embed

    async def callback(self, interaction: Interaction):
        embed = self.embed
        channel = self.values[0]
        destination = await channel.fetch()
        await interaction.response.defer()
        await destination.send(embed=embed)
        await interaction.message.edit(
            content=f"Successfully sent the embed in {destination.mention}", view=None
        )


class Template:
    def get_default_embed() -> Embed:
        embed = Embed(
            title="Embed creator",
            description="Select the options below to edit this embed",
        )
        return embed

    async def set_title_description(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Edit title and description")
        modal.add_item(TextInput(label="Title", required=False, default=embed.title))
        modal.add_item(
            TextInput(
                label="Description",
                style=discord.TextStyle.long,
                default=embed.description,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        title = str(modal.children[0])
        description = str(modal.children[1])
        embed.title = title
        embed.description = description

    async def set_color(embed: Embed, interaction: Interaction):
        color = ""
        modal = ModalInput(title="Edit color")
        modal.add_item(
            TextInput(
                label="hex code",
                required=False,
                default=color,
                placeholder="Leave empty for default color",
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        color = str(modal.children[0]) or int()
        if not isinstance(color, int):
            color = int(color, 16)
        embed.color = color

    async def set_url(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Edit url")
        modal.add_item(TextInput(label="Url", required=False, default=embed.url))
        await interaction.response.send_modal(modal)
        await modal.wait()
        url = str(modal.children[0])
        embed.url = url

    async def set_image(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Edit image")
        modal.add_item(TextInput(label="Url", required=False, default=embed.image.url))
        await interaction.response.send_modal(modal)
        await modal.wait()
        url = str(modal.children[0])
        embed.set_image(url=url)

    async def set_thumbnail(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Edit thumbnail")
        modal.add_item(
            TextInput(label="Url", required=False, default=embed.thumbnail.url)
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        url = str(modal.children[0])
        embed.set_thumbnail(url=url)

    async def set_author(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Edit author")
        modal.add_item(
            TextInput(label="Name", required=False, default=embed.author.name)
        )
        modal.add_item(TextInput(label="Url", required=False, default=embed.author.url))
        modal.add_item(
            TextInput(
                label="Icon url",
                required=False,
                default=embed.author.icon_url,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        name = str(modal.children[0])
        url = str(modal.children[1])
        icon_url = str(modal.children[2])
        embed.set_author(name=name, url=url, icon_url=icon_url)

    async def set_footer(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Edit footer")
        modal.add_item(
            TextInput(label="Text", required=False, default=embed.footer.text)
        )
        modal.add_item(
            TextInput(
                label="Icon url",
                required=False,
                default=embed.footer.icon_url,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        text = str(modal.children[0])
        icon_url = str(modal.children[1])
        embed.set_footer(text=text, icon_url=icon_url)

    async def add_field(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Add field")
        modal.add_item(TextInput(label="Name", required=False))
        modal.add_item(
            TextInput(label="Value", required=False, style=discord.TextStyle.long)
        )
        modal.add_item(TextInput(label="Inline", required=False, placeholder="yes/no"))
        await interaction.response.send_modal(modal)
        await modal.wait()
        name = str(modal.children[0])
        value = str(modal.children[1])
        if str(modal.children[2]).lower() == "yes":
            inline = True
        else:
            inline = False
        if name:
            embed.add_field(name=name, value=value, inline=inline)

    async def remove_field(embed: Embed, interaction: Interaction):
        modal = ModalInput(title="Remove embed")
        modal.add_item(TextInput(label="Index", placeholder="starts from 0"))
        await interaction.response.send_modal(modal)
        await modal.wait()
        index = int(str(modal.children[0]))
        embed.remove_field(index=index)


class ModalInput(Modal):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
