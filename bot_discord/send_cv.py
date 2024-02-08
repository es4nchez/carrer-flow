from discord.ext import commands
from discord.commands import slash_command
import logging
import PyPDF2
import asyncio
import os

LOG = logging

class SendCV(commands.Cog):
    """
    Cog to send CV for the Career Fair
    """
    def __init__(self, bot):
        LOG.info(f"Initialized {self.__class__.__name__}")
        self.bot = bot
        self.cv_path = "./cvs/"

    @slash_command(name="send_cv")
    async def send_cv(self, ctx):
        """
        Command: Send a CV for Career Fair
        """
        await ctx.author.send("Please respond to this message with a .pdf CV in the next 2 minutes.")
        await ctx.respond(content="Message sended in your PM's", ephemeral=True)

        try:
            response_message = await self.bot.wait_for(
                "message",
                timeout=120,
                check=lambda message: message.author == ctx.author and message.attachments and message.guild is None
            )
            attachment = response_message.attachments[0]
            file_content = await attachment.read()

            temp_filename = f"{self.cv_path}temp_{ctx.author.name}_cv.pdf"
            with open(temp_filename, "wb") as temp_file:
                temp_file.write(file_content)

            try:
                with open(temp_filename, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    if len(pdf_reader.pages) > 0:
                        filename = f"{self.cv_path}{ctx.author.name}_cv.pdf"
                        os.rename(temp_filename, filename)
                        await ctx.author.send(f"CV file '{attachment.filename}' received and processed successfully.")
                    else:
                        os.remove(temp_filename)
                        await ctx.author.send("The received file is not a valid PDF. Please send a valid PDF file.")

            except:
                os.remove(temp_filename)
                await ctx.author.send(f"The received file is not a valid PDF. Please send a valid PDF file")

        except asyncio.TimeoutError:
            await ctx.send("No response received. Please use the command again to send your cv.")

def setup(bot):
    bot.add_cog(SendCV(bot))
