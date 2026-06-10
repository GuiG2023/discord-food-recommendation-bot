import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# load env
load_dotenv()

class FoodOracleBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Bot Hook Function"""
        await self.load_extension("bot.commands.search")
        await self.tree.sync()
        print("🔄 Slash commands synced!")

bot = FoodOracleBot()

@bot.event
async def on_ready():
    print(f'✅ Bot is online! Logged in as {bot.user} (ID: {bot.user.id})')
    print('-----------------------------------')

if __name__ == '__main__':
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("❌ DISCORD_TOKEN not found in .env file!")
    
    bot.run(TOKEN)