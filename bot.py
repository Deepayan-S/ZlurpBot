import discord
from discord.ext import commands
import re
import yt_dlp
import os
import tempfile
from urllib.parse import urlparse
import shutil

# Intents let your bot access specific data (like messages)
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

# Set command prefix (e.g., "!help") and pass in intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Helper function to validate URLs
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_media(url, mode='video'):
    with tempfile.TemporaryDirectory() as temp_dir:
        if mode == 'audio':
            opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': '/usr/bin/ffmpeg',  # Updated for Railway
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '64',
                }],
            }
        else:  # video
            opts = {
                'format': 'mp4',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location':'/usr/bin/ffmpeg',  # Updated for Railway
            }
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                # Find the actual file in the temp directory
                for file in os.listdir(temp_dir):
                    if file.startswith(info['title']):
                        downloaded_file = os.path.join(temp_dir, file)
                        persistent_temp = os.path.join(tempfile.gettempdir(), file)
                        shutil.copy(downloaded_file, persistent_temp)
                        return persistent_temp, info['title']
                return None, "No file found after download"
            except Exception as e:
                return None, str(e)

# ✅ This event runs when the bot is logged in and ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Discord file upload limit (8MB for non-Nitro users)
DISCORD_FILE_LIMIT = 8 * 1024 * 1024

@bot.command(name='dl')
async def download_command(ctx, url: str):
    if not is_valid_url(url):
        await ctx.send("❌ Please provide a valid URL")
        return
    if 'youtube.com' in url or 'youtu.be' in url or 'instagram.com' in url:
        await ctx.send("⏳ Downloading video, please wait...")
        file_path, title = download_media(url, mode='video')
        if file_path and os.path.exists(file_path):
            try:
                if os.path.getsize(file_path) > DISCORD_FILE_LIMIT:
                    await ctx.send(f"❌ The video file is too large to send on Discord (>{DISCORD_FILE_LIMIT // (1024*1024)}MB). Try a shorter or lower quality video.")
                    os.remove(file_path)
                    return
                await ctx.send(f"✅ Here's your video: {title}", file=discord.File(file_path))
                os.remove(file_path)
            except Exception as e:
                await ctx.send(f"❌ Error sending file: {str(e)}")
        else:
            await ctx.send(f"❌ Error downloading video: {title}")
    else:
        await ctx.send("❌ Only YouTube and Instagram links are supported")

@bot.command(name='dlaudio')
async def download_audio_command(ctx, url: str):
    if not is_valid_url(url):
        await ctx.send("❌ Please provide a valid URL")
        return
    if 'youtube.com' in url or 'youtu.be' in url or 'instagram.com' in url:
        await ctx.send("⏳ Downloading audio, please wait...")
        file_path, title = download_media(url, mode='audio')
        if file_path and os.path.exists(file_path):
            try:
                if os.path.getsize(file_path) > DISCORD_FILE_LIMIT:
                    await ctx.send(f"❌ The audio file is too large to send on Discord (>{DISCORD_FILE_LIMIT // (1024*1024)}MB). Try a shorter or lower quality video.")
                    os.remove(file_path)
                    return
                await ctx.send(f"✅ Here's your audio: {title}", file=discord.File(file_path))
                os.remove(file_path)
            except Exception as e:
                await ctx.send(f"❌ Error sending file: {str(e)}")
        else:
            await ctx.send(f"❌ Error downloading audio: {title}")
    else:
        await ctx.send("❌ Only YouTube and Instagram links are supported")

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
        # Optionally, you can auto-trigger download here if you want

    # 🎧 If a direct media link is detected
    elif media_match:
        await message.channel.send("🎵 Media link detected! Preparing to download...")
        # Optionally, you can auto-trigger download here if you want

    # ✅ Process other commands (required if you're using commands.Bot)
    await bot.process_commands(message)

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
bot.run(os.getenv("DISCORD_TOKEN"))
