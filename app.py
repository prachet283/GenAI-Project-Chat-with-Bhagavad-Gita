from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv

# Load environment variables (API keys etc.)
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow frontend requests

# ---------- Load Data & Build RAG ----------
# Document Loader
loader = PyPDFLoader("data/Bhagavad-gita-As-It-Is-English.pdf")
docs = loader.load()

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# Embeddings
embedding = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

#Vector Store
vector_store = FAISS.from_documents(chunks, embedding)

# Retriever
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Prompt template
prompt = PromptTemplate(
    template = """
    You are Lord Krishna, offering divine counsel based ONLY on the teachings of the Bhagavad Gita. 
    You speak with clarity, wisdom, and compassion, as you did to Arjuna on the battlefield of Kurukshetra.
    You must only draw from the Bhagavad Gita and always conclude your guidance with the relevant verse references.
    If the Bhagavad Gita does not provide enough information, respond with:
    "The Bhagavad Gita does not answer that directly."

    Previous conversation:
    {history}

    Context (Bhagavad Gita passages):
    {content}

    Question: {question}

    Answer as Lord Krishna, followed by verse references.
    """,
    input_variables=["history", "content", "question"]
)

# LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)

# Format docs
def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

# Parallel retriever chain
parallel_chain = RunnableParallel({
    "content": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough(),
})

# Parser
parser = StrOutputParser()

# Memory
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Main chain
def run_chain(user_input):
    messages = memory.load_memory_variables({}).get("history", [])

    # Build readable history string
    history = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            history += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"Krishna: {msg.content}\n"

    retrieved = parallel_chain.invoke(user_input)
    full_input = {
        "history": history,
        "content": retrieved["content"],
        "question": user_input,
    }

    response = (prompt | model | parser).invoke(full_input)

    # Save to memory
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(response)

    return response

# ---------- Flask Routes ----------
@app.route("/")
def home():
    return render_template("index.html")  # your frontend

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = run_chain(user_input)
    return jsonify({"reply": response})

# Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
