from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.chains  import  ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

def get_webpage_chunks(query1):
    with open(f'{query1}.txt', 'r+', encoding="utf-8") as text:
        contents = text.read().split('\n\n\n')    

    docs = [Document(page_content=element) for element in contents]
    return docs

def generate_chromadb_embeddings(docs):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    print("X")
    # embedded_docs = embeddings.embed_documents(docs)
    print("Y")
    vector_store = FAISS.from_documents(docs, embedding=embeddings)
    print("Z")
    vector_store.save_local("faiss_index")
    vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    print("W")
    return vector_db