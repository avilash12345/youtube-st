import streamlit as st
from pytubefix import YouTube
import os
from pathlib import Path

# Get system Downloads folder
downloads_path = str(Path.home() / "Downloads")

st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.title("📥 YouTube Video/Audio Downloader")

url = st.text_input("🔗 Enter YouTube URL")

download_type = st.radio("📁 Download as:", ("Video", "Audio"))

# Initialize
streams = []
resolutions = []

if url:
    try:
        yt = YouTube(url)
        st.success(f"🎬 Title: {yt.title}")

        if download_type == "Video":
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            resolutions = [stream.resolution for stream in streams]
        else:
            streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
            resolutions = [stream.abr for stream in streams]

        selected_quality = st.selectbox("🎚️ Select quality:", resolutions)

        if st.button("⬇️ Download"):
            stream = next((s for s in streams if (s.resolution if download_type == "Video" else s.abr) == selected_quality), None)
            if stream:
                st.info("Downloading...")
                file_path = stream.download(output_path=downloads_path)
                st.success(f"✅ Downloaded to: {file_path}")
                with open(file_path, "rb") as file:
                    st.download_button(label="📂 Save File", data=file, file_name=os.path.basename(file_path))
            else:
                st.error("❌ Stream not found for selected quality.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
