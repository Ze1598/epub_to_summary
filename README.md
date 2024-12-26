# Summarise books in EPUB format using Google Gemini [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://epub-to-summary.streamlit.app/)


* This web app takes your uploaded EPUB book, converts it to the Markdown format, and then submits it to Google Gemini for summarisation
* User-uploaded files within the web app are only kept during summarisation. All intermediary files generated are deleted upon completion, including deletion of files Gemini-side

The summary includes:
 - Chapters and a two-sentence description for each chapter
 - Key concepts and definitions provided by the author
 - Chapter summaries included within the book, if any
 - Overall summary included within the book, if any
 - Any tools, recipes, processes, or systems discussed 
 - Existing ideas, concepts, theories, or laws discussed