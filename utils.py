import os
import google.generativeai as genai
import streamlit as st
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import html2text
import os
import re
from tempfile import NamedTemporaryFile

def gemini_authenticate():
    """Authenticate into the Gemini API"""
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=GEMINI_KEY)
    
    
def clean_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def html_to_markdown(html_content):
    """Convert HTML content to Markdown"""
    # First parse with BeautifulSoup to clean the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize html2text
    h = html2text.HTML2Text()
    h.body_width = 0  # Disable line wrapping
    h.ignore_images = False
    h.ignore_links = False
    h.ignore_tables = False
    
    # Convert to markdown
    markdown = h.handle(str(soup))
    return markdown


def epub_to_markdown(epub_path, output_dir='output'):
    """Convert EPUB file to Markdown"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read EPUB file
    book = epub.read_epub(epub_path)
    
    # Get book title for the main markdown file
    book_title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Untitled'
    book_title = clean_filename(book_title)
    
    # Create main markdown file
    main_markdown_path = os.path.join(output_dir, f'{book_title}.md')
    
    with open(main_markdown_path, 'w', encoding='utf-8') as main_file:
        # Write book title
        main_file.write(f'# {book_title}\n\n')
        
        # Write metadata
        creator = book.get_metadata('DC', 'creator')
        if creator:
            main_file.write(f'Author: {creator[0][0]}\n\n')
        
        # Process each document in the EPUB
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Convert HTML content to markdown
                content = item.get_content().decode('utf-8')
                markdown_content = html_to_markdown(content)
                
                # Write content to main file
                main_file.write(markdown_content)
                main_file.write('\n\n---\n\n')  # Add separator between chapters
    
    return main_markdown_path


def cleanup_gemini_files():
    gemini_authenticate()
    
    file_names = [f.name for f in genai.list_files()]
    print(file_names)

    for f in file_names:
        print(f"Deleting {f}")
        genai.delete_file(f)
        print()


def summarise_markdown(file_path, display_name, gemini_model="gemini-1.5-pro"):
    gemini_authenticate()

    # Upload markdown file separately
    gemini_file = genai.upload_file(path = file_path, display_name = display_name, mime_type = "text/markdown")
    
    gemini_file_name = gemini_file.name

    # And send the prompt
    model = genai.GenerativeModel(gemini_model)
    prompt ="""
    For the book attached, I want you to retrieve the following information:
    - Chapters and a two-sentence description for each chapter
    - Key concepts and definitions provided by the author
    - If there are chapter summaries included within the book, include them as part of your response verbatim
    - If there is a summary for the book at the end, typically in the last chapter, include it as part of your response verbatim
    - If the book describes any tools, recipes, processes, or systems, then include their details as part of your response
    - If the book references existing ideas, concepts, theories, or laws, then include their names as part of your response

    Do not consult external sources for this response. Respond based purely on the file attached.
    """
    result = model.generate_content(
        [gemini_file, "\n\n", prompt]
    )
    
    # Finished with Gemini, clean up artefacts
    genai.delete_file(gemini_file_name)

    return result.text


def manage_epub_to_markdown(uploaded_file):
    """Create a temporary epub file to be converted into markdown"""
    # Create a temporary file
    with NamedTemporaryFile(delete = False, suffix='.epub') as tmp_file:
        # Write the uploaded file content to the temporary file
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # Convert EPUB to Markdown as a persisted file
    md_path = epub_to_markdown(tmp_path)
    md_name = os.path.basename(md_path)

    # Collate all paths and file names to clean up separately    
    info_dict = {
        "epub_path": tmp_path,
        "markdown_path": md_path,
        "markdown_name": md_name
    }

    return info_dict


def cleanup_local_files(file_dict):
    """Cleanup all local files, provided a dict containing file paths"""
    
    paths_to_delete = [file_dict[path] for path in file_dict.keys() if "_path" in path]
    
    for path in paths_to_delete:
        os.unlink(path)