import streamlit as st
from app.api import send_url_to_scraping_module, send_question_to_qa_module

# Set page title and layout
st.set_page_config(page_title="Scraping & Q&A Interface", layout="wide")

# Title of the application
st.title("Web Scraping and Q&A System")

# URL Input Section
st.header("Submit URL for Scraping")
url = st.text_input("Enter the URL to scrape")

if st.button("Submit URL"):
    if url:
        with st.spinner('Scraping content...'):
            result = send_url_to_scraping_module(url)
        if result['status'] == 'success':
            st.success("Scraping completed successfully!")
            st.text_area("Scraped Text:", result['scraped_text'], height=200)
        else:
            st.error(f"Failed to scrape the URL: {result['error']}")
    else:
        st.warning("Please enter a valid URL.")

# Question Input Section
st.header("Ask a Question")
question = st.text_input("Enter your question")

if st.button("Submit Question"):
    if question:
        with st.spinner('Fetching answer...'):
            answer = send_question_to_qa_module(question)
        if answer['status'] == 'success':
            st.success("Answer fetched successfully!")
            st.text_area("Answer:", answer['answer'], height=100)
        else:
            st.error(f"Failed to fetch the answer: {answer['error']}")
    else:
        st.warning("Please enter a valid question.")
