# import sys
# #print(sys.path)
# import streamlit as st
# import time
# import base64
# import os
# from prompt_processing import response_generator, extract_tasks, get_libraries


# language_versions = {
#     "Python": ["3.12", "3.11", "3.10", "3.9", "3.8", "3.7", "2.7"],
#     "JavaScript": ["ES2023", "ES2022", "ES2021", "ES2020", "ES2019", "ES2018", "ES6"],
# }

# # Set page config to wide layout
# st.set_page_config(layout="wide")

# def set_bg_from_local(image_file):
#     with open(image_file, "rb") as f:
#         img_data = f.read()
#     b64_encoded = base64.b64encode(img_data).decode()
#     style = f"""
#         <style>
#         .stApp {{
#             background-image: url(data:image/png;base64,{b64_encoded});
#             background-size: 100vw;
#             background-position: center center;
#             background-repeat: no-repeat;
#             background-attachment: fixed;
#         }}
#         .stApp::before {{
#             content: "";
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             background-color: rgba(0, 0, 0, 0.4);  # Dark overlay
#             z-index: -1;
#         }}
#         .stApp > div {{
#             color: white;  # Set text color to white for better visibility
#         }}
#         .stChatMessage {{
#             background-color: rgba(0, 0, 0, 0.6);  # Opaque background for chat messages
#             padding: 10px;
#             border-radius: 5px;
#             margin-bottom: 10px;
#         }}
#         </style>
#     """
#     st.markdown(style, unsafe_allow_html=True)

# # Usage
# set_bg_from_local('bg.png')

# st.title("PackIt - `requirements.txt` solved.")

# # Initialize session state
# if 'initial_input_submitted' not in st.session_state:
#     st.session_state.initial_input_submitted = False
# if 'language' not in st.session_state:
#     st.session_state.language = "Python"
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# # In the initial input section
# if not st.session_state.initial_input_submitted:
#     with st.expander("Welcome! Please provide some information to get started", expanded=True):
#         st.write("Welcome to PackIt!")
        
#         st.session_state.language = st.selectbox(
#             "Select Language",
#             list(language_versions.keys())
#         )
        
#         st.session_state.version = st.selectbox(
#             "Select Version",
#             language_versions[st.session_state.language]
#         )
        
#         product_spec = st.text_area("Enter Product Specification", key="product_spec_input", placeholder="Hit ⌘+Enter to submit")
        
#         if product_spec and product_spec != st.session_state.get('previous_product_spec', ''):
#             st.session_state.initial_input_submitted = True
#             st.session_state.previous_product_spec = product_spec
#             st.experimental_rerun()

#         if st.button("Submit"):
#             st.session_state.initial_input_submitted = True
#             st.experimental_rerun()

# # After the form is submitted, store the product spec in session state
# if st.session_state.initial_input_submitted and 'product_spec' not in st.session_state:
#     st.session_state.product_spec = st.session_state.previous_product_spec

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(f'<div class="stChatMessage">{message["content"]}</div>', unsafe_allow_html=True)

# # If initial input has been submitted, show the chat interface
# if st.session_state.initial_input_submitted:
#     # Display initial response
#     if len(st.session_state.messages) == 0:
#         initial_prompt = f"You are an AI assistant helping with software development. The user is working on a project with the following specification: '{st.session_state.product_spec}'. They are using {st.session_state.language} version {st.session_state.version}. Provide a helpful response to get started."
#         st.session_state.messages.append({"role": "system", "content": initial_prompt})
#         with st.chat_message("assistant"):
#             response = st.write(get_libraries(st.session_state.previous_product_spec, st.session_state.language, st.session_state.version))
#         st.session_state.messages.append({"role": "assistant", "content": response})

#     # Accept user input
#     if prompt := st.chat_input("Ask a follow-up question about the library data or provide additional context to the assistant."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(f'<div class="stChatMessage">{prompt}</div>', unsafe_allow_html=True)
        
#         with st.chat_message("assistant"):
#             response = st.write_stream(response_generator(st.session_state.messages))
        
#         st.session_state.messages.append({"role": "assistant", "content": response})
#####################


import streamlit as st
import time
import base64
import os
from prompt_processing import response_generator, extract_tasks, get_libraries

language_versions = {
    "Python": ["3.12", "3.11", "3.10", "3.9", "3.8", "3.7", "2.7"],
    "JavaScript": ["ES2023", "ES2022", "ES2021", "ES2020", "ES2019", "ES2018", "ES6"],
}

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
        .stChatMessage {{
            background-color: rgba(0, 0, 0, 0.6);  # Opaque background for chat messages
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
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
    with st.expander("Please provide some information on your project to get started", expanded=True):
        st.write("Welcome to PackIt!")
        
        st.session_state.language = st.selectbox(
            "Select Language",
            list(language_versions.keys())
        )
        
        st.session_state.version = st.selectbox(
            "Select Version",
            language_versions[st.session_state.language]
        )
        
        product_spec = st.text_area("Enter Project Specification", key="product_spec_input", placeholder="Hit ⌘+Enter to submit")
        
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
        st.markdown(f'<div class="stChatMessage">{message["content"]}</div>', unsafe_allow_html=True)

# If initial input has been submitted, show the chat interface
if st.session_state.initial_input_submitted:
    # Display initial response
    if len(st.session_state.messages) == 0:
        initial_prompt = f"You are an AI assistant helping with software development. The user is working on a project with the following specification: '{st.session_state.product_spec}'. They are using {st.session_state.language} version {st.session_state.version}. Provide a helpful response to get started."
        st.session_state.messages.append({"role": "system", "content": initial_prompt})
        with st.spinner('"Loading brilliance... Just a byte-sized delay!"'):
            with st.chat_message("assistant"):
                response = st.write(get_libraries(st.session_state.previous_product_spec, st.session_state.language, st.session_state.version))
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Accept user input
    if prompt := st.chat_input("Ask a follow-up question about the library data or provide additional context to the assistant."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div class="stChatMessage">{prompt}</div>', unsafe_allow_html=True)
        
        with st.spinner('"Loading brilliance... Just a byte-sized delay!"'):
            with st.chat_message("assistant"):
                response = st.write_stream(response_generator(st.session_state.messages))
        
        st.session_state.messages.append({"role": "assistant", "content": response})


#TO DO (placeholder)
def generate_requirements_txt(specification, language, version):
    # Generate the content of requirements.txt based on the session data
    return f"# Generated for {language} {version}\n# Spec: {specification}\nnumpy==1.18.5\npandas==1.2.0"

# Place this in the appropriate part of your Streamlit app where the button should appear
if st.button("Generate and Download requirements.txt"):
    specification = st.session_state.product_spec  # Assuming you store product spec in session_state
    language = st.session_state.language
    version = st.session_state.version

    requirements_content = generate_requirements_txt(specification, language, version)
    
    # Use Streamlit's built-in function to provide a download button
    st.download_button(
        label="Download requirements.txt",
        data=requirements_content,
        file_name="requirements.txt",
        mime="text/plain"
    )