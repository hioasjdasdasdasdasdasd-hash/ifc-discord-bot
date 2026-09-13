"""
IFC Discord Bot - Main Entry Point
International Futbol Confederation League Management System
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Load cogs
async def load_cogs():
    """Load all cog extensions"""
    cog_dirs = [
        "cogs/admin",
        "cogs/clubs",
        "cogs/players",
        "cogs/signings",
        "cogs/transfers",
        "cogs/contracts",
        "cogs/loans",
        "cogs/lfp",
        "cogs/budgets",
        "cogs/valuations",
        "cogs/matches",
        "cogs/config"
    ]
    
    for cog_dir in cog_dirs:
        try:
            for file in os.listdir(cog_dir):
                if file.endswith(".py") and not file.startswith("_"):
                    cog_name = f"{cog_dir.replace('/', '.')}.{file[:-3]}"
                    await bot.load_extension(cog_name)
                    logger.info(f"Loaded cog: {cog_name}")
        except FileNotFoundError:
            logger.warning(f"Cog directory not found: {cog_dir}")
        except Exception as e:
            logger.error(f"Error loading cogs from {cog_dir}: {e}")

@bot.event
async def on_ready():
    """Bot startup event"""
    logger.info(f"Bot logged in as {bot.user}")
    logger.info(f"Connected to {len(bot.guilds)} guild(s)")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="IFC League | /help for commands"
    ))

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    logger.error(f"Command error: {error}")
    await ctx.send(f"❌ An error occurred: {str(error)}", ephemeral=True)

async def main():
    """Main startup function"""
    try:
        # Load database
        logger.info("Initializing database...")
        from database.init_db import init_database
        await init_database()
        
        # Load cogs
        logger.info("Loading cogs...")
        await load_cogs()
        
        # Start bot
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("DISCORD_TOKEN not found in .env file")
        
        logger.info("Starting bot...")
        await bot.start(token)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
