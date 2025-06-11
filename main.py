import streamlit as st
from pytubefix import YouTube

def on_progress(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percentage = (bytes_downloaded / stream.filesize) * 100
    progress_bar.progress(int(percentage))

def download_video(url, resolution):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(resolution=resolution).first()
    stream.download()
    st.success("Video downloaded successfully!")

def download_audio(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download()
    st.success("Audio downloaded successfully!")

st.title("YouTube Downloader")

url = st.text_input("Enter YouTube URL")

if url:
    yt = YouTube(url)
    st.write(f"Title: {yt.title}")
    st.write(f"Author: {yt.author}")
    st.write(f"Length: {yt.length} seconds")

    download_type = st.selectbox("Select download type", ["Video", "Audio"])

    if download_type == "Video":
        resolutions = [stream.resolution for stream in yt.streams.filter(progressive=True)]
        resolution = st.selectbox("Select resolution", resolutions)
        progress_bar = st.progress(0)
        if st.button("Download Video"):
            with st.spinner("Downloading video..."):
                download_video(url, resolution)
    elif download_type == "Audio":
        progress_bar = st.progress(0)
        if st.button("Download Audio"):
            with st.spinner("Downloading audio..."):
                download_audio(url)