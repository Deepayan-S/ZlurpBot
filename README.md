# ZlurpBot

ZlurpBot is a Discord bot designed to easily download videos and audio from YouTube and Instagram directly within your Discord server. It also includes a standalone CLI script for local downloads.

## Features

- **Video Download**: Download videos from YouTube and Instagram using the `!dl` command.
- **Audio Download**: Extract and download audio from YouTube videos using the `!dlaudio` command.
- **Link Detection**: Automatically detects YouTube and media links in chat (functionality can be extended).
- **File Size Management**: Checks file sizes to ensure they fit within Discord's upload limits (8MB for non-Nitro users).
- **CLI Tool**: A separate script (`scraperScript.py`) for downloading media locally via the terminal.

## Prerequisites

- **Python 3.8+**
- **FFmpeg**: Required for media processing.
  - **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH.
  - **Linux/Mac**: Install via your package manager (e.g., `sudo apt install ffmpeg`).

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Deepayan-S/ZlurpBot.git
    cd ZlurpBot
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup**:
    - Create a `.env` file in the root directory.
    - Add your Discord Bot Token:
        ```
        DISCORD_TOKEN=your_discord_bot_token_here
        ```

## Configuration

The bot is currently configured for a Linux environment (e.g., Railway/Render) with the FFmpeg path hardcoded to `/usr/bin/ffmpeg` in `bot.py`.

**If running on Windows:**
You may need to modify `bot.py` to remove the `ffmpeg_location` argument or set it to your local FFmpeg path if it's not automatically detected.

## Usage

### Running the Bot
Start the bot using Python:
```bash
python bot.py
```

### Discord Commands
- `!dl <url>`: Download video from the provided URL.
  - Example: `!dl https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- `!dlaudio <url>`: Download audio from the provided URL.
  - Example: `!dlaudio https://www.youtube.com/watch?v=dQw4w9WgXcQ`

### Running the CLI Script
You can also use the scraper script to download media locally:
```bash
python scraperScript.py
```
Follow the on-screen prompts to enter a URL and choose between video or audio.

## Deployment

The repository includes a `render.yaml` file, making it ready for deployment on [Render](https://render.com/).

## License

This project is open source.
