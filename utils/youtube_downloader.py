from pytube import YouTube

def download_youtube_video(url, output_path='temp_audio.mp4'):
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Error downloading video: {e}")
