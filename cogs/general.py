import discord
from discord import app_commands
from discord.ext import commands
from config import Config
from utils.embeds import create_embed
import time

class General(commands.Cog):
    """General commands for the bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):

        ws_latency = round(self.bot.latency * 1000)
        
        # Calculate API latency
        start_time = time.perf_counter()
        await interaction.response.defer()
        end_time = time.perf_counter()
        api_latency = round((end_time - start_time) * 1000)
        
        embed = create_embed(
            title="🏓 Pong!",
            color=Config.COLOR_SUCCESS
        )
        
        embed.add_field(name="Websocket Latency", value=f"`{ws_latency}ms`", inline=True)
        embed.add_field(name="API Latency", value=f"`{api_latency}ms`", inline=True)
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, interaction: discord.Interaction):
        """Slash command to greet the user"""
        embed = create_embed(
            title="👋 Hello!",
            description=f"Hi {interaction.user.mention}! How can I help you today?",
            color=Config.COLOR_PRIMARY
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="Get information about a user")
    @app_commands.describe(member="The member to get info about")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        """Slash command to display user information"""
        member = member or interaction.user
        
        embed = create_embed(
            title=f"User Info - {member.name}",
            color=Config.COLOR_PRIMARY
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Username", value=str(member), inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, 'R'), inline=True)
        
        # Only show joined_at if available
        if member.joined_at:
            embed.add_field(name="Joined Server", value=discord.utils.format_dt(member.joined_at, 'R'), inline=True)
        
        embed.add_field(name="Roles", value=f"{len(member.roles) - 1}", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo", description="Get information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        """Slash command to display server information"""
        guild = interaction.guild
        
        embed = create_embed(
            title=f"Server Info - {guild.name}",
            color=Config.COLOR_PRIMARY
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(guild.created_at, 'R'), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
