import streamlit as st
import time
import base64
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter

from prompt_processing import response_generator, extract_tasks, create_embeddings_and_store, query_vectordb

# Set page config to wide layout
st.set_page_config(layout="wide")

def set_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: 100vw;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.4);  # Dark overlay
            z-index: -1;
        }}
        .stApp > div {{
            color: white;  # Set text color to white for better visibility
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Usage
set_bg_from_local('bg.png')

st.title("PackIt - `requirements.txt` solved.")

# Initialize session state
if 'initial_input_submitted' not in st.session_state:
    st.session_state.initial_input_submitted = False
if 'language' not in st.session_state:
    st.session_state.language = "Python"
if 'messages' not in st.session_state:
    st.session_state.messages = []

# In the initial input section
if not st.session_state.initial_input_submitted:
    with st.expander("Welcome! Please provide some information to get started", expanded=True):
        st.write("Welcome to PackIt!")
        
        st.session_state.language = st.selectbox(
            "Select Language",
            list(language_versions.keys())
        )
        
        st.session_state.version = st.selectbox(
            "Select Version",
            language_versions[st.session_state.language]
        )
        
        product_spec = st.text_area("Enter Product Specification", key="product_spec_input", placeholder="Hit ⌘+Enter to submit")
        
        if product_spec and product_spec != st.session_state.get('previous_product_spec', ''):
            st.session_state.initial_input_submitted = True
            st.session_state.previous_product_spec = product_spec
            st.experimental_rerun()

        if st.button("Submit"):
            st.session_state.initial_input_submitted = True
            st.experimental_rerun()

# After the form is submitted, store the product spec in session state
if st.session_state.initial_input_submitted and 'product_spec' not in st.session_state:
    st.session_state.product_spec = st.session_state.previous_product_spec

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# If initial input has been submitted, show the chat interface
if st.session_state.initial_input_submitted:
    # Display initial response
    if len(st.session_state.messages) == 0:
        # todo -> not sure why this is here        
        # initial_prompt = f"You are an AI assistant helping with software development. The user is working on a project with the following specification: '{st.session_state.product_spec}'. They are using {st.session_state.language} version {st.session_state.version}. Provide a helpful response to get started."
        st.session_state.messages.append({"role": "system", "content": initial_prompt})
        with st.chat_message("assistant"):
            response = st.write_stream(extract_tasks(st.session_state.previous_product_spec))
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Accept user input
    if prompt := st.chat_input("What else would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(st.session_state.messages))
        
        st.session_state.messages.append({"role": "assistant", "content": response})
