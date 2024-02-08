import discord
from discord.ext import commands
import os
import logging

LOG = logging

class Rappel(commands.Cog):
    """
    Cog to send rappel to student who haven't yet uploaded their cv 
    """
    def __init__(self, bot):
        LOG.info(f"Initialized {self.__class__.__name__}")
        self.bot = bot
        self.cv_path = "./cvs/"
        self.registered_users = ["es4nchez", "__vincent"] # Hardcoded for now, need to connect to the 42 intra to get the list

    @commands.slash_command(name="rappel_cv", description="Send a message to registered users who haven't uploaded their CV.")
    async def rappel_cv(self, ctx):
        """
        Command: Send rappel to registered student who haven't yet uploaded their CV
        """
        missing_cv_users = []
        for user in self.registered_users:
            cv_filename = f"{self.cv_path}{user}_cv.pdf"

            if not os.path.exists(cv_filename):
                missing_cv_users.append(user)

        if missing_cv_users:
            missing_users_message = "**Sending rappel to :**\n"
            missing_users_message += "\n".join(missing_cv_users)
            await ctx.respond(missing_users_message, ephemeral=True)
        else:
            await ctx.respond("All registered users have uploaded their CV.", ephemeral=True)

        for user in missing_cv_users:
                member = discord.utils.get(ctx.guild.members, name=user)  # Maybe a more efficient way to get the user
                dm_message = f"Hello {member.name}, it seems you haven't uploaded your CV yet for the Career Fair. Please do so as soon as possible."
                await member.send(dm_message)
       

def setup(bot):
    bot.add_cog(Rappel(bot))