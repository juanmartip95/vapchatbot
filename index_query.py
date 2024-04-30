from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.chains import StuffDocumentsChain,LLMChain

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "vaping-chatbot"


llm_name = "gpt-3.5-turbo"
key1= os.environ["OPENAI_API_KEY_NO"]
key = os.environ["OPENAI_API_KEY"]


llm=ChatOpenAI(model_name=llm_name, temperature=0,openai_api_key = key1)
# a purely formal prompt for formatting the docs
prompt = PromptTemplate.from_template("Summarize this content: {context}")
# a purely formal chain for later defining a stuff documents chain to format docs
llm_chain = LLMChain(llm=llm, prompt=prompt)
# define embedding
embeddings = OpenAIEmbeddings(openai_api_key = key)
# load vector database
db = FAISS.load_local("vaping_index",embeddings)
# define retriever, score_threshold is minimum required similarity (0 to 1)
#retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold":0.7})
retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 4,"score_threshold":0.6})
# create a stuff documents chain.
sd = StuffDocumentsChain(llm_chain=llm_chain)

# obtain relevant documents from db
def get_docs(query):
  docs = retriever.get_relevant_documents(query)
  return sd._get_inputs(docs)['context'] 