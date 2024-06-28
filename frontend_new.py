import streamlit as st
import time
import base64
import os
from prompt_processing import followup_generator, extract_tasks, get_libraries

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
# set_bg_from_local('bg.png')

st.title("PackIt - `requirements.txt` solved.")

# Initialize session state
if 'initial_input_submitted' not in st.session_state:
    st.session_state.initial_input_submitted = False
if 'language' not in st.session_state:
    st.session_state.language = "Python"
if 'messages' not in st.session_state:

    st.session_state.messages = []
if 'version' not in st.session_state:
    st.session_state.version = None
if 'previous_product_spec' not in st.session_state:
    st.session_state.previous_product_spec = None



def stream_data(sentence):
    for word in sentence.split(" "):
        yield word + " "
        time.sleep(0.09)

def create_form():
    pass


if not st.session_state.initial_input_submitted:
    st.chat_message("assistant").write_stream(stream_data("""Welcome! Please provide some information to get started!"""))
    st.chat_message("assistant").write_stream(stream_data("Select Language"))
    st.session_state.language = st.selectbox(
        "",
        list(language_versions.keys())
    )
    st.chat_message("assistant").write_stream(stream_data("Select Version"))
    st.session_state.version = st.selectbox(
        "",
        language_versions[st.session_state.language]
    )
    product_spec = st.text_area("Enter Product Specification", key="product_spec_input", placeholder="Hit ⌘+Enter to submit")

    if product_spec and product_spec != st.session_state.get('previous_product_spec', ''):
        st.session_state.initial_input_submitted = True
        st.session_state.previous_product_spec = product_spec
        #st.experimental_rerun()


    submitButton = st.button(label = "Submit", on_click = submit_test, args=[])
    # if st.button("Submit"):
    #     st.session_state.initial_input_submitted = True
    #     st.experimental_rerun()


# if st.session_state.initial_input_submitted:
#     user_prompt = "I would like to create a project with the description {}, in the {} language with version {}".format( st.session_state.previous_product_spec, st.session_state.language, st.session_state.version)
#
#     st.session_state.product_spec = st.session_state.previous_product_spec
#     st.chat_message("user").write_stream(stream_data(user_prompt))
#
#     st.chat_message("assistant").write_stream(stream_data("Certainly!!!!"))
#
# #
# # In the initial input section
# if not st.session_state.initial_input_submitted:
#     with st.expander("Welcome! Please provide some information to get started", expanded=True):
#         st.write("Welcome to PackIt!")
#
#         st.session_state.language = st.selectbox(
#             "Select Language",
#             list(language_versions.keys())
#         )
#
#         st.session_state.version = st.selectbox(
#             "Select Version",
#             language_versions[st.session_state.language]
#         )
#
#         product_spec = st.text_area("Enter Product Specification", key="product_spec_input", placeholder="Hit ⌘+Enter to submit")
#
#         if product_spec and product_spec != st.session_state.get('previous_product_spec', ''):
#             st.session_state.initial_input_submitted = True
#             st.session_state.previous_product_spec = product_spec
#             st.experimental_rerun()
#
#         if st.button("Submit"):
#             st.session_state.initial_input_submitted = True
#             st.experimental_rerun()

# After the form is submitted, store the product spec in session state
# if st.session_state.initial_input_submitted and 'product_spec' not in st.session_state:
#     st.session_state.product_spec = st.session_state.previous_product_spec
#
# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(f'<div class="stChatMessage">{message["content"]}</div>', unsafe_allow_html=True)
#
# # If initial input has been submitted, show the chat interface
# if st.session_state.initial_input_submitted:
#     # Display initial response
#     if len(st.session_state.messages) == 0:
#         initial_prompt = f"You are an AI assistant helping with software development. The user is working on a project with the following specification: '{st.session_state.product_spec}'. They are using {st.session_state.language} version {st.session_state.version}. Provide a helpful response to get started."
#         st.session_state.messages.append({"role": "system", "content": initial_prompt})
#         with st.chat_message("assistant"):
#             response = st.write(get_libraries(st.session_state.previous_product_spec, st.session_state.language, st.session_state.version))
#         st.session_state.messages.append({"role": "assistant", "content": response})
#
#     # Accept user input
#     if prompt := st.chat_input("What else would you like to know?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(f'<div class="stChatMessage">{prompt}</div>', unsafe_allow_html=True)
#
#         with st.chat_message("assistant"):
#             response = st.write(response_generator(st.session_state.messages))
#
#         st.session_state.messages.append({"role": "assistant", "content": response})





#
# # In the initial input section
# if not st.session_state.initial_input_submitted:
#     with st.expander("Welcome! Please provide some information to get started", expanded=True):
#         st.write("Welcome to PackIt!")
#
#         st.session_state.language = st.selectbox(
#             "Select Language",
#             list(language_versions.keys())
#         )
#
#         st.session_state.version = st.selectbox(
#             "Select Version",
#             language_versions[st.session_state.language]
#         )
#
#         product_spec = st.text_area("Enter Product Specification", key="product_spec_input", placeholder="Hit ⌘+Enter to submit")
#
#         if product_spec and product_spec != st.session_state.get('previous_product_spec', ''):
#             st.session_state.initial_input_submitted = True
#             st.session_state.previous_product_spec = product_spec
#             st.experimental_rerun()
#
#         if st.button("Submit"):
#             st.session_state.initial_input_submitted = True
#             st.experimental_rerun()
#
# # After the form is submitted, store the product spec in session state
# if st.session_state.initial_input_submitted and 'product_spec' not in st.session_state:
#     st.session_state.product_spec = st.session_state.previous_product_spec
#
# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(f'<div class="stChatMessage">{message["content"]}</div>', unsafe_allow_html=True)
#
# # If initial input has been submitted, show the chat interface
# if st.session_state.initial_input_submitted:
#     # Display initial response
#     if len(st.session_state.messages) == 0:
#         initial_prompt = f"You are an AI assistant helping with software development. The user is working on a project with the following specification: '{st.session_state.product_spec}'. They are using {st.session_state.language} version {st.session_state.version}. Provide a helpful response to get started."
#         st.session_state.messages.append({"role": "system", "content": initial_prompt})
#         with st.chat_message("assistant"):
#             response = st.write(get_libraries(st.session_state.previous_product_spec, st.session_state.language, st.session_state.version))
#         st.session_state.messages.append({"role": "assistant", "content": response})
#
#     # Accept user input
#     if prompt := st.chat_input("Ask a follow-up question about the library data or provide additional context to the assistant."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(f'<div class="stChatMessage">{prompt}</div>', unsafe_allow_html=True)
#
#         with st.chat_message("assistant"):
#             response = st.write_stream(response_generator(st.session_state.messages))
#
#         st.session_state.messages.append({"role": "assistant", "content": response})
