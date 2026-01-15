import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        # Only enable members intent if you need it (requires privileged intent)
        # intents.members = True
        
        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Load all cogs when the bot starts"""
        print("Loading cogs...")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✓ Loaded cog: {filename[:-3]}')
                except Exception as e:
                    print(f'✗ Failed to load cog {filename[:-3]}: {e}')
        
        # Sync slash commands with Discord
        print("Syncing commands...")
        await self.tree.sync()
        print("Commands synced!")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        print(f'\n{self.user} is now online!')
        print(f'Bot ID: {self.user.id}')
        print(f'Discord.py version: {discord.__version__}')
        print('-' * 40)
        
        # Set bot status
        await self.change_presence(
            activity=discord.Game(name=Config.STATUS),
            status=discord.Status.online
        )

async def main():
    # Check if token is configured
    if not Config.TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env file!")
        return
    
    bot = DiscordBot()
    try:
        async with bot:
            await bot.start(Config.TOKEN)
    except discord.errors.PrivilegedIntentsRequired:
        print("\nERROR: Privileged intents are not enabled!")
    except discord.errors.LoginFailure:
        print("\nERROR: Invalid bot token!")
        print("Please check your DISCORD_TOKEN in the .env file")
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
