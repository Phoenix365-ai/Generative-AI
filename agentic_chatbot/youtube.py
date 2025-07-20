import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for Gemini
PROMPT = """You are a YouTube video summarizer. You will take the transcript text
and provide a concise summary in bullet points within 250 words. Please summarize the following text: """

# Extract video ID from URL
def get_video_id(url):
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return video_id_match.group(1) if video_id_match else None

# Fetch YouTube transcript
def extract_transcript(video_id):
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

# Generate summary using Gemini API
def generate_summary(transcript):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(PROMPT + transcript)
    return response.text


# Streamlit UI
st.title("🎯 YouTube Video Summarizer")
youtube_url = st.text_input("Enter YouTube Video URL:")

if youtube_url:
    video_id = get_video_id(youtube_url)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    else:
        st.error("Invalid YouTube URL!")

if st.button("Get Summary"):
    if not youtube_url:
        st.warning("Please enter a YouTube URL.")
    elif not video_id:
        st.error("Invalid YouTube URL.")
    else:
        with st.spinner("Fetching transcript and generating summary..."):
            transcript = extract_transcript(video_id)
            if transcript:
                summary = generate_summary(transcript)
                st.markdown("## ✨ Detailed Notes:")
                st.write(summary)