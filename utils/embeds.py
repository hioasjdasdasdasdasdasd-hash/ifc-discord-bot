"""
Embed Templates and Utilities
"""

import discord
from datetime import datetime

class IFCEmbed(discord.Embed):
    """Custom IFC Embed with standard formatting"""
    
    def __init__(self, title="", description="", **kwargs):
        super().__init__(
            title=title,
            description=description,
            color=discord.Color.blue(),
            timestamp=datetime.utcnow(),
            **kwargs
        )

def create_player_card(player, club=None):
    """Create player profile embed"""
    embed = IFCEmbed(
        title=f"👤 {player.roblox_username or 'Player'}",
        description=f"Overall: **{player.overall}**"
    )
    embed.add_field(name="Position", value=player.position or "N/A", inline=True)
    embed.add_field(name="Country", value=player.country or "N/A", inline=True)
    embed.add_field(name="Status", value=player.status.value, inline=True)
    
    if club:
        embed.add_field(name="Club", value=f"**{club.name}**", inline=False)
    
    embed.add_field(name="Market Value", value=f"${player.market_value:,.0f}", inline=True)
    embed.add_field(name="Valuation Tier", value=player.valuation_tier.value, inline=True)
    
    embed.add_field(
        name="Statistics",
        value=f"🎯 {player.matches_played}M | ⚽ {player.goals}G | 🅰️ {player.assists}A | ⭐ {player.avg_rating}",
        inline=False
    )
    
    return embed

def create_signing_announcement(player, club, transfer_fee=None, contract_months=None):
    """Create signing announcement embed"""
    embed = IFCEmbed(
        title="✅ PLAYER SIGNED",
        description=f"**{player.roblox_username}** has signed with **{club.name}**!"
    )
    embed.add_field(name="Position", value=player.position or "N/A", inline=True)
    embed.add_field(name="Overall", value=str(player.overall), inline=True)
    embed.add_field(name="Market Value", value=f"${player.market_value:,.0f}", inline=True)
    
    if transfer_fee:
        embed.add_field(name="Transfer Fee", value=f"${transfer_fee:,.0f}", inline=True)
    if contract_months:
        embed.add_field(name="Contract", value=f"{contract_months} months", inline=True)
    
    return embed

def create_transfer_announcement(player, from_club, to_club, fee):
    """Create transfer announcement embed"""
    embed = IFCEmbed(
        title="🔄 PLAYER TRANSFERRED",
        description=f"**{player.roblox_username}** has transferred from **{from_club.name}** to **{to_club.name}**"
    )
    embed.add_field(name="Transfer Fee", value=f"${fee:,.0f}", inline=True)
    embed.add_field(name="Market Value", value=f"${player.market_value:,.0f}", inline=True)
    embed.add_field(name="Position", value=player.position or "N/A", inline=True)
    
    return embed

def create_loan_announcement(player, owner_club, loan_club, loan_fee=None):
    """Create loan announcement embed"""
    embed = IFCEmbed(
        title="➡️ PLAYER LOANED",
        description=f"**{player.roblox_username}** loaned from **{owner_club.name}** to **{loan_club.name}**"
    )
    if loan_fee:
        embed.add_field(name="Loan Fee", value=f"${loan_fee:,.0f}", inline=True)
    embed.add_field(name="Market Value", value=f"${player.market_value:,.0f}", inline=True)
    embed.add_field(name="Position", value=player.position or "N/A", inline=True)
    
    return embed

def create_club_embed(club):
    """Create club profile embed"""
    embed = IFCEmbed(
        title=f"⚽ {club.name}",
        description=f"Budget: ${club.budget:,.0f}"
    )
    
    if club.logo_url:
        embed.set_thumbnail(url=club.logo_url)
    
    embed.add_field(name="Roster", value=f"0/{club.roster_limit}", inline=True)
    embed.add_field(name="Manager", value="N/A", inline=True)
    
    return embed

def create_error_embed(title, description):
    """Create error embed"""
    embed = discord.Embed(
        title=f"❌ {title}",
        description=description,
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    return embed

def create_success_embed(title, description):
    """Create success embed"""
    embed = discord.Embed(
        title=f"✅ {title}",
        description=description,
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    return embed
