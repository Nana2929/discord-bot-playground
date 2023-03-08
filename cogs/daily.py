# %%
from typing import List
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
import discord
from discord import ui
from discord import app_commands
from discord.ext.forms import Form, Validator, ReactionForm, ReactionMenu
import math
import api.daily as daily_adapter

# %%
# from utils.logger import L


class DailyAddModal(ui.Modal):
    def __init__(self, title="新增 daily", **kwargs):

        super().__init__(title=title)

        self.add_item(ui.TextInput(
            label="Name",
            required=True,
            max_length=127
        ))
        self.add_item(ui.TextInput(
            label="Description",
            required=True,
            style=discord.TextStyle.paragraph,
            max_length=255
        ))

    async def on_submit(self, interaction: discord.Interaction):

        name = self.children[0].value
        description = self.children[1].value
        user_id = interaction.user.id
        server_id = interaction.guild.id

        print(name, description, user_id, server_id)

        if daily_adapter.add_task(
            user_id=str(user_id),
            server_id=str(server_id),
            name=str(name),
            description=str(description)
        ):
            embed = discord.Embed(
                title="新增 daily 成功",
                description=f"Name: {name}\nDescription: {description}",
                color=discord.Color.green()
            )
            await interaction.response.edit_message(
                content=None, view=None, embed=embed)
        else:
            await interaction.response.edit_message(
                content=f"新增 daily 失敗", view=None)


class Daily(commands.Cog, name="daily", description=""):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="daily",
        description="",
    )
    @checks.not_blacklisted()
    async def daily(self, ctx: Context):

        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed...")

    @daily.command(
        name="add",
        description="新增 daily task",
    )
    @checks.not_blacklisted()
    async def daily_add(self, ctx: Context):

        view = ui.View()
        open_button = ui.Button(
            label="點我新增 daily", style=discord.ButtonStyle.primary)

        async def callback(interaction: discord.Interaction):
            modal = DailyAddModal()
            await interaction.response.send_modal(modal)

        open_button.callback = callback
        view.add_item(open_button)

        await ctx.send(view=view)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Daily(bot))