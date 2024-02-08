import yaml

with open('config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.BaseLoader)

DISCORD_SERVER_ID = config['bot']['DISCORD_SERVER_ID']
CALENDY_API_KEY = config['calendy']['CALENDY_API_KEY']
DISCORD_BOT_TOKEN = config['bot']['DISCORD_BOT_TOKEN']