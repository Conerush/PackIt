import time
import base64
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings


# Setup LangChain ChatOpenAI
# chat = ChatOpenAI(temperature=0, streaming=True)
# embeddings = OpenAIEmbeddings()

# Load a free model from Hugging Face (e.g., GPT-2)
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create a text generation pipeline
text_generation_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=100,
    temperature=0,
)

# Create a LangChain HuggingFacePipeline object
chat = HuggingFacePipeline(pipeline=text_generation_pipeline)


# Define language-version mapping
language_versions = {
    "Python": ["3.12", "3.11", "3.10", "3.9", "3.8", "3.7", "2.7"],
    "JavaScript": ["ES2023", "ES2022", "ES2021", "ES2020", "ES2019", "ES2018", "ES6"],
}

def extract_tasks(specification):
    if not specification: return None # todo -> handle!!
    extraction_prompt = f"""You are a senior software engineer buildling a project with the following specification:
    <projectSpecification>

    {specification}

    </projectSpecification>

    Seperate each of your tasks ONLY with newlines - do NOT use bullet points or a numbred list
    """
    response = chat([HumanMessage(content=extraction_prompt)])
    return [line.strip() for line in response.content.split('\n') if line.strip()]

def call_jtao_api(specification, language, version):
    tasks = extract_tasks(specification)
    # use ex_jtao_out.json as a placeholder for the API response
    with open('ex_jtao_out.json') as f:
        api_response = json.load(f)
    return api_response

# function for initial product spec api call
def spec_to_libraries(spec, language, version):
    task_extraction_prompt = f"Extract the main tasks and steps involved in the following project specification: '{st.session_state.product_spec}'"


def response_generator(messages):
    try:
        stream = chat.stream(messages)
        for chunk in stream:
            if chunk.content:
                yield chunk.content
    except Exception as e:
        yield f"An error occurred: {str(e)}"

def extract_tasks(specification):
    prompt = f"Extract the main tasks and steps involved in the following project specification: {specification}"
    response = chat([HumanMessage(content=prompt)])
    return response.content

def create_embeddings_and_store(tasks):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(tasks)
    vectorstore = Chroma.from_texts(texts, embeddings)
    return vectorstore

def query_vectordb(vectorstore, query):
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=retriever)
    return qa_chain.run(query)
