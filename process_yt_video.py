# Function to extract video ID from YouTube URL
import re
import yt_dlp

def get_video_id(youtube_url):
    match = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})", youtube_url)    
    return match.group(0) if match else None

# Function to generate YouTube embed URL
def get_embed_url(youtube_url):
    video_id = get_video_id(youtube_url)
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return None
# Function to download audio 
def download_audio(youtube_url):
    video_id = get_video_id(youtube_url)
    if not video_id:

        return None, None  # Invalid URL

    

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        audio_path = "temp_audio.mp3"  

    return audio_path
