import os
import csv
import re
import urllib
import requests
import ssl
from time import sleep
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from get_text import *
from get_embeddings import *
from get_llm_reply import *

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
from flask import Flask, render_template, jsonify, request


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

system_prompt = """You are a medical assistant Q&A bot. You are here to answer questions based on the context given.
You are prohibited from using prior knowledge and you can only use the context given. If you need
more information, please ask the user."""

ai_prompt = """
Hello! I’m here to assist you with any questions you have based on the provided PUBMED articles.
"""


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    user_prompt = msg
    print("User Input: ", user_prompt)

    query1 = "Heart transplant"
    year_from = "2008"
    year_to = "2022"
    search_url = format_query(query1, year_from, year_to)
    url = fetch_url(search_url)
    filename = f"{query1}.txt"
    webpage_text = download_webpage(url)
    if webpage_text:
        save_text_to_file(webpage_text, filename)

    docs = get_webpage_chunks(query1)
    vectordb = generate_chromadb_embeddings(docs)

    llm_reply = qa_conversational_chain(vectordb, system_prompt, user_prompt, ai_prompt)
    print("Response:", llm_reply)

    return str(llm_reply)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 5000, debug= True)