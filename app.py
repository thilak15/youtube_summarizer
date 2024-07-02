import streamlit as st
from utils.youtube_downloader import download_youtube_video
from utils.audio_extractor import extract_audio_text
from utils.summarizer import summarize_text
import os

# Enhance the UI
st.set_page_config(page_title="YouTube Video Summarizer", layout="wide")
st.title("🎥 YouTube Video Summarizer")
st.markdown("""
    This app summarizes YouTube videos. Enter the URL of a YouTube video to get a concise summary of its content.
    """)

st.sidebar.header("About")
st.sidebar.markdown("""
    **YouTube Video Summarizer** allows you to generate concise summaries of YouTube videos. 
    Enter a YouTube video URL and get a summarized version of the content.
    Currently, it only supports English language videos with a single speaker.
    """)

video_url = st.text_input("Enter YouTube Video URL:", "")
summarize_button = st.button("Summarize Video")

if summarize_button and video_url:
    try:
        with st.spinner("Downloading video..."):
            video_path = download_youtube_video(video_url)
        
        with st.spinner("Extracting audio text..."):
            audio_text = extract_audio_text(video_path)
        
        with st.spinner("Generating summary..."):
            summary = summarize_text(audio_text)
        
        st.success("Summary generated successfully!")
        
        # Display pre-processed and post-processed text
        st.subheader("Pre-processed Text:")
        st.text_area("Transcript of the video:", audio_text, height=200)
        
        st.subheader("Post-processed Text (Summary):")
        st.text_area("Summary of the video:", summary, height=200)
        
        # Option to download the summary
        st.download_button(
            label="Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain",
        )
    except ValueError as ve:
        st.error(f"Value Error: {ve}")
    except Exception as e:
        st.error(f"Error: {e}")
