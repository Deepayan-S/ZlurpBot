import discord
from discord.ext import commands
import re

# Intents let your bot access specific data (like messages)
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

# Set command prefix (e.g., "!help") and pass in intents
bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ This event runs when the bot is logged in and ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ✅ This event runs whenever someone sends a message
@bot.event
async def on_message(message):
    # Prevent bot from responding to itself
    if message.author == bot.user:
        return

    # 📌 REGEX: Detect YouTube links or media links
    youtube_regex = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+"
    media_regex = r"(https?://\S+\.(mp4|mp3|m4a|wav|avi|mov))"

    # 🔍 Search message content for links
    youtube_match = re.search(youtube_regex, message.content)
    media_match = re.search(media_regex, message.content)

    # 🧠 If a YouTube link is detected
    if youtube_match:
        await message.channel.send("🎬 YouTube link detected! Your file will be processed soon.")
        
        # 🛠️ TODO: Your friend can add YouTube video/audio downloading logic here
        # Example: Use pytube, yt-dlp, or any scraper
        # file_path = download_video_from_youtube(youtube_match.group())
        # await message.channel.send(file=discord.File(file_path))

    # 🎧 If a direct media link is detected
    elif media_match:
        await message.channel.send("🎵 Media link detected! Preparing to download...")
        
        # 🛠️ TODO: Your friend can add logic to download and return audio/video here

    # ✅ Process other commands (required if you're using commands.Bot)
    await bot.process_commands(message)

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
bot.run(os.getenv("DISCORD_TOKEN"))
