import os
from dotenv import load_dotenv
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
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("openai_api_key")
openai_api_version = os.getenv("openai_api_version")
openai_api_base = os.getenv("openai_api_base")
deployment_name = os.getenv("openai_api_key")

def qa_conversational_chain(vectordb, system_prompt, user_prompt, ai_prompt):
    llm = AzureChatOpenAI(
        openai_api_key = openai_api_key,
        openai_api_version = openai_api_version,
        openai_api_base = openai_api_base,
        deployment_name = deployment_name,
        temperature=0.2
    )

    ret = vectordb.as_retriever(search_kwargs={"k": 3})
    qa = ConversationalRetrievalChain.from_llm(llm, ret)

    chat_history = [
        SystemMessage(content = system_prompt),
        HumanMessage(content = "Do you know about depression?"),
        AIMessage(content = ai_prompt)
    ]

    prompt = "Please anwser the question first. If you don't have the answer, please refer the user to specific articles related to the question."
    # question = "List the  types of depression."
    final_prompt = user_prompt + " " + prompt

    llm_reply = qa.invoke({"question": final_prompt, "chat_history" : chat_history})["answer"]

    return llm_reply