"""
Permission and Validation Utilities
"""

import discord
from discord.ext import commands
from database.config import SessionLocal
from database.models import Player, Club, League, Setting
import logging

logger = logging.getLogger(__name__)

async def has_permission(ctx, required_role_id):
    """Check if user has required role"""
    if not required_role_id:
        return False
    return discord.utils.get(ctx.author.roles, id=required_role_id) is not None

async def get_player(ctx, discord_id=None):
    """Get player from database"""
    db = SessionLocal()
    try:
        if discord_id is None:
            discord_id = ctx.author.id
        player = db.query(Player).filter(Player.discord_id == discord_id).first()
        return player
    except Exception as e:
        logger.error(f"Error getting player: {e}")
        return None
    finally:
        db.close()

async def get_club_by_manager(ctx, manager_id=None):
    """Get club managed by user"""
    db = SessionLocal()
    try:
        if manager_id is None:
            manager_id = ctx.author.id
        
        player = await get_player(ctx, manager_id)
        if not player:
            return None
        
        club = db.query(Club).filter(Club.manager_id == player.id).first()
        return club
    except Exception as e:
        logger.error(f"Error getting club: {e}")
        return None
    finally:
        db.close()

async def get_league(ctx, guild_id=None):
    """Get league for guild"""
    db = SessionLocal()
    try:
        if guild_id is None:
            guild_id = ctx.guild.id
        league = db.query(League).filter(League.guild_id == guild_id).first()
        return league
    except Exception as e:
        logger.error(f"Error getting league: {e}")
        return None
    finally:
        db.close()

async def get_settings(ctx, guild_id=None):
    """Get league settings"""
    db = SessionLocal()
    try:
        if guild_id is None:
            guild_id = ctx.guild.id
        league = await get_league(ctx, guild_id)
        if not league:
            return None
        settings = db.query(Setting).filter(Setting.league_id == league.id).first()
        return settings
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return None
    finally:
        db.close()

def is_organizer():
    """Check if user is organizer"""
    async def predicate(ctx):
        settings = await get_settings(ctx)
        if not settings or not settings.role_organizer:
            await ctx.send("❌ Organizer role not configured", ephemeral=True)
            return False
        return await has_permission(ctx, settings.role_organizer)
    return commands.check(predicate)

def is_league_admin():
    """Check if user is league admin"""
    async def predicate(ctx):
        settings = await get_settings(ctx)
        if not settings or not settings.role_league_admin:
            await ctx.send("❌ League Admin role not configured", ephemeral=True)
            return False
        return await has_permission(ctx, settings.role_league_admin)
    return commands.check(predicate)

def is_manager():
    """Check if user is manager"""
    async def predicate(ctx):
        club = await get_club_by_manager(ctx)
        if not club:
            await ctx.send("❌ You are not a manager of any club", ephemeral=True)
            return False
        return True
    return commands.check(predicate)

def is_player():
    """Check if user has player profile"""
    async def predicate(ctx):
        player = await get_player(ctx)
        if not player:
            await ctx.send("❌ You don't have a player profile", ephemeral=True)
            return False
        return True
    return commands.check(predicate)
