#!/usr/bin/env python
# coding: utf-8

# # Part 0

# In[2]:


# !pip install -r requirements.txt


# In[13]:


# Data handling 
import pandas as pd 
import json

# Database stuff
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DataFrameLoader
from langchain_openai import OpenAIEmbeddings

# Model
from sentence_transformers import SentenceTransformer


# # Part 1: Preprocessing

# In[14]:


# Load in data
with open('package_info.json', 'r') as json_file:
    data = json.load(json_file)

df = pd.DataFrame(data)
df = df[['name', 'key_features', 'description']]
df['key_features'] = df['key_features'].apply(lambda x: ', '.join(map(str, x)))
df['all_info'] = df.apply(lambda row: str(row.to_dict()), axis=1)


# # Part 2: Populate VectorDB

# In[15]:


# Model name
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Create model class
class Model():
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, text):
        embeddings = self.model.encode(text, convert_to_numpy=True).tolist()
        return embeddings
    
    def embed_query(self, text):
        text = text.lower().strip()
        embeddings = self.model.encode(text, convert_to_numpy=True).tolist()
        return embeddings


# In[16]:


# Create the data loader
loader = DataFrameLoader(df, page_content_column="all_info")
data = loader.load()
db_size = len(data)
print(db_size)


# In[18]:


model = Model(model_name)
# Populate vector database #
# vectorstore = vectorstore = Chroma.from_documents(documents=data, embedding=model, persist_directory="db")
# vectorstore.persist()

# Import local save of vector database #
# vectorstore = Chroma(persist_directory="database", embedding_function=model)


# # Part 3: RAG

# In[19]:


# Load in search algs
# sim_search = vectorstore.similarity_search_with_relevance_scores
# mmr_search = vectorstore.max_marginal_relevance_search


# In[20]:


def produce_dict(doc):
    return {'Name': doc.metadata['name'], 'Description': doc.metadata['description'], 'Key Features': doc.metadata['key_features']}


def search(queries, n, sim_search, mmr_search):
    if (n > db_size):
        print(f"Error: n is too large, there are only {db_size} documents in the database.")
        return None
    
    if not isinstance(queries, list):
        print("Error: Input must be a list of strings.")
        return None
    
    fetch_k = max(int(db_size/10), n)
    
    sim_results = []
    mmr_results = []
    positions = {}
    packages = {}
    
    
    for query in queries:
        sim_packages = sim_search(query=query, k=n)
        mmr_packages = mmr_search(query=query, k=min(fetch_k, n), fetch_k=fetch_k, alpha=0.5)
        
        sim_names = [p[0].metadata['name'] for p in sim_packages]
        mmr_names = [p.metadata['name'] for p in mmr_packages]
        
        num_sim = len(sim_names)
        num_mmr = len(mmr_names)
        
        sim_results.append(sim_names)
        mmr_results.append(mmr_names)
        
        for p in sim_packages:
            name = p[0].metadata['name']
            if name in positions:
                continue
            packages[name] = produce_dict(p[0])
            positions[name] = 0
        
        for p in mmr_packages:
            name = p.metadata['name']
            if name in positions: 
                continue
            packages[name] = produce_dict(p)
            positions[name] = 0
           
     
    all = [key for key in positions]
    for iter in range(len(sim_results)):
        names_left = all.copy()
        for ind, name in enumerate(sim_results[iter]):
            positions[name] += ind+1
            names_left.remove(name)   
        
        for name in names_left:
            positions[name] += num_sim+1
        
        names_left = all.copy()
        for ind, name in enumerate(mmr_results[iter]):
            positions[name] += ind+1
            names_left.remove(name)   
        
        for name in names_left:
            positions[name] += num_mmr+1        
            
    for key in positions:
        packages[key]['Average Position'] = positions[key]/(2*len(queries))
        
    packages = dict(sorted(packages.items(), key=lambda item: item[1]['Average Position']))
     
    return [packages[key] for key in packages]


# In[22]:


def retrieve(queries, n):
    # Import local save of vector database #
    vectorstore = Chroma(persist_directory="db", embedding_function=model)
    
    # Load in search algs
    sim_search = vectorstore.similarity_search_with_relevance_scores
    mmr_search = vectorstore.max_marginal_relevance_search
    
    # Retrieve
    return search(queries, n, sim_search, mmr_search)


# In[ ]:




