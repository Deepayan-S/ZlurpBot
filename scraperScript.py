import yt_dlp
import os
from datetime import datetime
import re

class MediaScraper:
    def __init__(self, output_path="downloads"):
        self.output_path = output_path
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Configure yt-dlp options
        self.ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,  # Don't download playlists
            'quiet': False,
            'no_warnings': False,
        }

    def get_platform(self, url):
        """Determine the platform from the URL."""
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'instagram.com' in url:
            return 'instagram'
        else:
            return 'unknown'

    def get_media_info(self, url):
        """Get information about the media without downloading it."""
        try:
            platform = self.get_platform(url)
            if platform == 'unknown':
                print("Unsupported platform. Please provide a YouTube or Instagram URL.")
                return None

            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'description': info.get('description'),
                    'platform': platform
                }
        except Exception as e:
            print(f"Error getting media info: {str(e)}")
            return None

    def download_video(self, url, format='best'):
        """Download a video."""
        try:
            platform = self.get_platform(url)
            if platform == 'unknown':
                print("Unsupported platform. Please provide a YouTube or Instagram URL.")
                return False

            # Update format in options
            self.ydl_opts['format'] = format
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                print(f"Downloading video from: {url}")
                ydl.download([url])
                print("Download completed successfully!")
                return True
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return False

    def download_audio(self, url):
        """Download only the audio from a video."""
        try:
            platform = self.get_platform(url)
            if platform == 'unknown':
                print("Unsupported platform. Please provide a YouTube or Instagram URL.")
                return False
            if platform == 'instagram':
                print("Audio download is not supported for Instagram reels.")
                return False

            # Update format to audio only
            self.ydl_opts['format'] = 'bestaudio[ext=m4a]'
            # Remove FFmpeg postprocessor
            if 'postprocessors' in self.ydl_opts:
                del self.ydl_opts['postprocessors']
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                print(f"Downloading audio from: {url}")
                ydl.download([url])
                print("Audio download completed successfully!")
                return True
        except Exception as e:
            print(f"Error downloading audio: {str(e)}")
            return False

def main():
    # Example usage
    scraper = MediaScraper()
    
    # Get URL from user
    url = input("Enter the YouTube video or Instagram reel URL: ")
    
    # Get media information
    print("\nGetting media information...")
    info = scraper.get_media_info(url)
    if info:
        print("\nMedia Information:")
        for key, value in info.items():
            if value is not None:  # Only print non-None values
                print(f"{key}: {value}")
    
    # Ask user for file type
    while True:
        file_type = input("\nWhat would you like to download? (video/audio): ").lower()
        if file_type in ['video', 'audio']:
            break
        print("Invalid input! Please enter 'video' or 'audio'")
    
    # Download based on user selection
    if file_type == 'video':
        print("\nDownloading video...")
        scraper.download_video(url)
    else:
        print("\nDownloading audio...")
        scraper.download_audio(url)

if __name__ == "__main__":
    main()
