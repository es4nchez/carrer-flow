import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import logging
import asyncio
import model
import config

LOG = logging

class ExportImport(commands.Cog):
    """
    Cog to import and export csv to the database
    """
    def __init__(self, bot):
        LOG.info(f"Initialized {self.__class__.__name__}")
        self.bot = bot
        self.file_name = "export.csv"
        self.cv_path = "./cvs/"

    @slash_command()
    async def send_csv(self, ctx, table: Option(str, "Choose the table", choices=['Company', 'Student', 'Offer', 'StudentOffer'])):
        """
        Command: Import a csv in the database
        """
        await ctx.author.send("Respond to this message with the csv in the next 2 minutes.")
        await ctx.respond(content="Message sended in your PM's", ephemeral=True)

        try:
            response_message = await self.bot.wait_for(
                "message",
                timeout=120,
                check=lambda message: message.author == ctx.author and message.attachments and message.guild is None
            )
            attachment = response_message.attachments[0]
            file_content = await attachment.read()

            with open(self.file_name, "wb") as temp_file:
                temp_file.write(file_content)

            model.import_from_csv(model.MODELS[table], self.file_name)

        except asyncio.TimeoutError:
            await ctx.send("No response received. Please use the command again to send your cv.")

    @slash_command(guild_ids=[int(config.DISCORD_SERVER_ID)])
    async def get_csv(self, ctx, table: Option(str, "Choose the table", choices=['Company', 'Student', 'Offer', 'StudentOffer'])):
        """
        Command: Export a csv of the database
        """
        model.export_to_csv(model.MODELS[table], self.file_name)



        

        with open(self.file_name, 'rb') as file:
            await ctx.author.send("Here are the user allocations for each company:", file=discord.File(file, "export.csv"))


def setup(bot):
    bot.add_cog(ExportImport(bot))