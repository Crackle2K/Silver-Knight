# Tropic

A modular Discord bot built with discord.py featuring slash commands, embeds, and a clean cog-based structure.

## Features

- 🎯 Slash Commands (Application Commands)
- 📦 Modular Cog System
- 🎨 Custom Embeds
- ⚙️ Easy Configuration
- 🛡️ Moderation Commands
- 📊 Server & User Info Commands

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Bot

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   PREFIX=!
   STATUS=with commands
   ```

### 3. Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to the "Bot" section and click "Add Bot"
4. Copy the token and paste it in your `.env` file
5. Enable these Privileged Gateway Intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent

### 4. Invite the Bot

1. Go to OAuth2 → URL Generator
2. Select scopes: `bot` and `applications.commands`
3. Select bot permissions (Administrator recommended for testing)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 5. Run the Bot

```bash
python bot.py
```

## Project Structure

```
Tropic/
├── bot.py              # Main bot file (entry point)
├── config.py           # Configuration settings
├── .env                # Environment variables (create from .env.example)
├── .env.example        # Example environment file
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── cogs/              # Command modules
│   ├── __init__.py
│   ├── general.py     # General commands (ping, hello, userinfo, etc.)
│   └── moderation.py  # Moderation commands (kick, ban, clear)
└── utils/             # Utility modules
    ├── __init__.py
    └── embeds.py      # Embed helper functions
```

## Available Commands

### General Commands
- `/ping` - Check bot latency
- `/hello` - Get a greeting from the bot
- `/userinfo [member]` - Get information about a user
- `/serverinfo` - Get information about the server

### Moderation Commands (Requires Permissions)
- `/kick <member> [reason]` - Kick a member from the server
- `/ban <member> [reason]` - Ban a member from the server
- `/clear <amount>` - Clear messages in a channel (1-100)

## Adding New Commands

### Create a New Cog

1. Create a new file in the `cogs/` directory (e.g., `fun.py`):

```python
import discord
from discord import app_commands
from discord.ext import commands
from config import Config
from utils.embeds import create_embed

class Fun(commands.Cog):
    """Fun commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="The message to say")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Fun(bot))
```

2. The bot will automatically load it on startup!

## Using Embeds

The `utils/embeds.py` module provides helper functions for creating embeds:

```python
from utils.embeds import create_embed, create_success_embed, create_error_embed

# Custom embed
embed = create_embed(
    title="My Title",
    description="My Description",
    color=Config.COLOR_PRIMARY
)

# Quick success embed
embed = create_success_embed("Operation completed!")

# Quick error embed
embed = create_error_embed("Something went wrong!")
```

## Configuration

Edit `config.py` to customize:
- Bot prefix
- Embed colors
- Bot status
- Other settings

## Troubleshooting

### Commands not showing up?
- Make sure you've enabled `applications.commands` scope when inviting the bot
- Wait a few minutes for Discord to sync the commands
- Try kicking and re-inviting the bot

### Bot not responding?
- Check that Message Content Intent is enabled
- Verify your token is correct in `.env`
- Check the console for error messages

## License

MIT License - Feel free to use and modify!
