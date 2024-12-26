import streamlit as st
from utils import summarise_markdown, manage_epub_to_markdown, cleanup_local_files#, timer
import os

st.set_page_config(
    page_title = "Home"
)

st.write("# 📖 Summarise your EPUB books with Google Gemini")


st.markdown(
    """
    Welcome to the Gemini book summariser. Upload your EPUB book and the app will handle everything for you :)

    Technical notes below:
    * This web app takes your uploaded EPUB book, converts it to the Markdown format, and then submits it to Google Gemini for summarisation
    * GitHub repository available [here](https://github.com/Ze1598/epub_to_summary)
    * Your uploaded files within the web app are only kept during summarisation. All intermediary files generated are deleted upon completion, including deletion of files Gemini-side
"""
)

st.info("For the curious minds, you can read the specific prompt sent to Gemini [here](https://github.com/Ze1598/epub_to_summary/blob/bc6670801816998d09ea290b04cda220e977e7e2/utils.py#L16)")


epub_book = st.file_uploader(
    label="Upload your file here - only one Epub (.epub) file accepted at a time"
    ,type="epub"
)
# epub_book = st.file_uploader(
    # label="Upload your file here - only one Markdown (.md) file accepted at a time"
#     ,type="md"
# )


if epub_book is not None:
    
    # First convert the input EPUB into Markdown
    epub_md_dict = manage_epub_to_markdown(epub_book)
    st.write("🪄 Successfully converted your EPUB to Markdown. Gemini is now on its way with the summary...")

    # Call Gemini to summarise the book
    book_summary = summarise_markdown(
        file_path=epub_md_dict["markdown_path"]
        , display_name=epub_md_dict["markdown_name"]
    )
    st.write("🧠 And here is your book summary, courtesy of Google Gemini")
    st.markdown(book_summary)

    # Delete temporary persisted files (epub upload and markdown conversion)
    cleanup_local_files(epub_md_dict)
    
    st.write("🧹 Successfully deleted all intermediary EPUB and Markdown files generated.")
    st.write("😎 Upload a new file for more summaries")