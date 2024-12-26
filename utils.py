import os
import google.generativeai as genai
import streamlit as st

def summarise_markdown(file_path, display_name, gemini_model="gemini-1.5-pro"):
    # Authenticate into the API
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=GEMINI_KEY)

    # Upload markdown file separately
    markdown_file = genai.upload_file(path = file_path, display_name = display_name, mime_type = "text/markdown")

    # And 
    model = genai.GenerativeModel(gemini_model)
    prompt ="""
    For the book attached, I want you to retrieve the following information:
    - Chapters and a two-sentence description for each chapter
    - Key concepts and definition provided by the author
    - If there are chapter summaries included within the book, include them as part of your response verbatim
    - If there is a summary for the book at the end, typically in the last chapter, include it as part of your response verbatim
    - If the book describes any tools, recipes, processes, or systems, then include their details as part of your response
    - If the book references existing ideas, concepts, theories, or laws, then include their names as part of your response

    Do not consult external sources for this response. Respond based purely on the file attached.
    """
    result = model.generate_content(
        [markdown_file, "\n\n", prompt]
    )

    return result.text