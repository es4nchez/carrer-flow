import discord
from discord.ext import commands
import pandas as pd
import pickle
from collections import defaultdict

class GetTables(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="get_slots")
    async def export_allocation(self, ctx):
        """
        Get the filled slots in a xlsx document
        """
        file_name = "users_choices.pkl"
        
        try:
            with open(file_name, 'rb') as file:
                all_users_data = pickle.load(file)
        except FileNotFoundError:
            await ctx.send("No data file found.")
            return
        
        allocations = defaultdict(list)
        sorted_data = sorted(all_users_data, key=lambda x: x['timestamp'])
        
        for entry in sorted_data:
            username = entry['username']
            for preference, company in entry['choices'].items():
                allocations[company].append(username)
        
        max_len = max(len(v) for v in allocations.values())
        df_dict = {company: (usernames + [''] * (max_len - len(usernames))) for company, usernames in allocations.items()}
        df = pd.DataFrame(df_dict)
        
        excel_file = "allocations.xlsx"
        df.to_excel(excel_file, index=False, engine='openpyxl')

        with open(excel_file, 'rb') as file:
            await ctx.send("Here are the user allocations for each company:", file=discord.File(file, "allocations.xlsx"))


def setup(bot):
    bot.add_cog(GetTables(bot))
