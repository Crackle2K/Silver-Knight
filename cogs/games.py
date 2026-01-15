import discord
from discord import app_commands
from discord.ext import commands
from discord_games import button_games

class InteractionContext:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.author = interaction.user
        self.bot = interaction.client
        self.channel = interaction.channel
        self.guild = interaction.guild
    
    async def send(self, *args, **kwargs):
        if not self.interaction.response.is_done():
            await self.interaction.response.send_message(*args, **kwargs)
            return await self.interaction.original_response()
        else:
            return await self.interaction.followup.send(*args, **kwargs)

class Games(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="reactiontest", description="Test your reaction time")
    async def reactiontest(self, interaction: discord.Interaction):
        ctx = InteractionContext(interaction)
        game = button_games.BetaReactionGame()
        await game.start(ctx, timeout=60)

async def setup(bot):
    await bot.add_cog(Games(bot))
