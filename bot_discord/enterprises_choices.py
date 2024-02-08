import discord
from discord.ext import commands
from discord.ui import View, Select, Button
from datetime import datetime
import model
import os
import pickle
import logging

LOG = logging

class DropdownView(View):
    """
    Dropdown for the internship offers
    """
    def __init__(self, companies):
        super().__init__(timeout=None)
        self.companies = companies
        self.selected_companies = []
        self.add_item(InternshipOfferSelect(self.companies, self.selected_companies))

class InternshipOfferSelect(Select):
    """
    View that will handle the dropdown of the jobs offers, the message and the callback
    """
    def __init__(self, companies, selected_companies):
        options = [discord.SelectOption(label=company) for company in companies if company not in selected_companies]
        options.append(discord.SelectOption(label="None", description="Finish selecting"))
        super().__init__(placeholder='Choose a company...', min_values=1, max_values=1, options=options)
        self.selected_companies = selected_companies

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected != "None":
            self.selected_companies.append(selected)

        companies_blockquote = "\n> ".join(self.view.companies)
        selected_companies_list = "\n".join(f"{index + 1} - {company}" for index, company in enumerate(self.selected_companies))
        
        if selected == "None" or len(self.selected_companies) >= 3:
            content = (f"**List of Available Interviews**:\n\n> {companies_blockquote}"
                       f"\n\n**Your selections:**\n{selected_companies_list}"
                       "\n\nPlease confirm your choices or restart the selection.")
            self.view.clear_items()
            self.view.add_item(ValidationButton(self.selected_companies))
            self.view.add_item(RestartButton(self.view.companies))
        else:
            content = (f"**List of Available Interviews**:\n\n> {companies_blockquote}"
                       f"\n\n**Your selections so far:**\n{selected_companies_list}"
                       "\n\nPlease select your next interview or choose 'None' to finish:")
            self.view.clear_items()
            self.view.add_item(InternshipOfferSelect(self.view.companies, self.selected_companies))
        
        await interaction.response.edit_message(content=content, view=self.view)

class ValidationButton(Button):
    """
    Validation of the selected companies
    """
    def __init__(self, selected_companies):
        super().__init__(style=discord.ButtonStyle.green, label="Validate")
        self.selected_companies = selected_companies

    async def callback(self, interaction: discord.Interaction):
        user_data = {
            "username": interaction.user.name,
            "timestamp": datetime.now(),
            "choices": {index + 1: company for index, company in enumerate(self.selected_companies)}}
        file_name = "users_choices.pkl"        # To be changed with real database
        if os.path.exists(file_name):
            with open(file_name, 'rb') as file:
                try:
                    all_users_data = pickle.load(file)  # To be changed with real database
                except EOFError:
                    all_users_data = []
        else:
            all_users_data = []             
        all_users_data.append(user_data)        
        with open(file_name, 'wb') as file:     
            pickle.dump(all_users_data, file)   # To be changed with real database

        await interaction.response.send_message(f'You have selected: {", ".join(self.selected_companies)}', ephemeral=True)

class RestartButton(Button):
    """
    Restart the Dropdown and select companies again
    """
    def __init__(self, companies):
        super().__init__(style=discord.ButtonStyle.red, label="Restart")
        self.companies = companies


    async def callback(self, interaction: discord.Interaction):
        new_view = DropdownView(self.companies)
        content = "Please select a company:"
        await interaction.response.edit_message(content=content, view=new_view)

def get_companies():
    """
    Get the internship offers list, to be linked with the precedent step
    """
    data = model.Company.select()  # To be changed with real database, sqlite3 for handling the csv's for now
    companies = []
    for chunk in data:
        if chunk.entreprise:
            companies.append(chunk.entreprise)
    return companies

class Choices(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="select_interest", description="Select your interest level for each offers.")
    async def select_interest(self, ctx: discord.ApplicationContext):
        companies = ["Groupe Mutuel - Data analyst",
                      "Groupe mutuel - Dev Web",
                      "Bobst - Web Full Stack",
                      "Infomaniak - Sysadmin"] # Hardcoded for the demo, and company / position are merged
      #  companies = get_companies() # deactivate for the demo
        companies_list = "\n> ".join(companies)
        content = f"**List of Available Interviews**:\n\n> {companies_list}\n\nPlease select an interview:"
        view = DropdownView(companies)
        await ctx.respond(content, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(Choices(bot))
