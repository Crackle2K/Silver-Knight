import discord
from datetime import datetime
from config import Config

def create_embed(
    title: str = None,
    description: str = None,
    color: int = None,
    footer: str = None,
    footer_icon: str = None,
    thumbnail: str = None,
    image: str = None,
    author_name: str = None,
    author_icon: str = None,
    timestamp: bool = True
) -> discord.Embed:
    """
    Create a Discord embed with common styling
    
    Args:
        title: Embed title
        description: Embed description
        color: Embed color (hex)
        footer: Footer text
        footer_icon: Footer icon URL
        thumbnail: Thumbnail image URL
        image: Main image URL
        author_name: Author name
        author_icon: Author icon URL
        timestamp: Whether to add timestamp (default: True)
    
    Returns:
        discord.Embed: Configured embed object
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color or Config.COLOR_PRIMARY,
        timestamp=datetime.utcnow() if timestamp else None
    )
    
    if footer:
        embed.set_footer(text=footer, icon_url=footer_icon)
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if image:
        embed.set_image(url=image)
    
    if author_name:
        embed.set_author(name=author_name, icon_url=author_icon)
    
    return embed


def create_success_embed(description: str, title: str = "✅ Success") -> discord.Embed:
    """Create a success embed"""
    return create_embed(
        title=title,
        description=description,
        color=Config.COLOR_SUCCESS
    )


def create_error_embed(description: str, title: str = "❌ Error") -> discord.Embed:
    """Create an error embed"""
    return create_embed(
        title=title,
        description=description,
        color=Config.COLOR_ERROR
    )


def create_warning_embed(description: str, title: str = "⚠️ Warning") -> discord.Embed:
    """Create a warning embed"""
    return create_embed(
        title=title,
        description=description,
        color=Config.COLOR_WARNING
    )


def create_info_embed(description: str, title: str = "ℹ️ Info") -> discord.Embed:
    """Create an info embed"""
    return create_embed(
        title=title,
        description=description,
        color=Config.COLOR_PRIMARY
    )
