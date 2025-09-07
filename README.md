# 🌿 Bhagavad Gita Conversational RAG Chatbot 🙏  

> _"Whenever dharma declines and the purpose of life is forgotten, I manifest myself on earth."_ — **Bhagavad Gita**

This project is a **GenAI RAG-based chatbot** that lets you talk to **Lord Krishna** himself 🌸.  
It uses **LangChain**, **FAISS**, and **HuggingFace Inference API** to provide **life guidance** from the **Bhagavad Gita**, with direct verse references.  

The UI has a divine Krishna essence 🎨 — with peacock feather watermark 🪶 — so the experience feels like a **spiritual conversation** rather than just a Q&A bot.  

---

## ✨ Features
- 📖 **Reference from Bhagavad Gita** (PDF source)  
- 🧠 **Conversational Memory** → Krishna remembers your past questions in the session  
- 🔎 **RAG (Retrieval-Augmented Generation)** → Accurate answers grounded in scripture  
- 🎨 **Aesthetic UI** with peacock feather watermark  
- ⚡ **Flask Backend + HTML/CSS/JS Frontend**  
- 🌐 **Deployable on Render/Heroku/Docker**  

---

## 🛠️ Tech Stack
- **Backend** → Flask + LangChain + HuggingFace API  
- **Frontend** → HTML, CSS, JS (chat-style interface)  
- **Vector DB** → FAISS (local)  
- **PDF Loader** → LangChain PyPDFLoader  
- **Memory** → ConversationBufferMemory  

---

## 📂 Project Structure
```bash
📁 BhagavadGita-Chatbot
 │── app.py # Flask backend (RAG + Memory)
 │── requirements.txt # Dependencies
 │── .env # HuggingFace API Key
 │── /templates
 │ └── index.html # Chat UI
 │── /static
 │ ├── style.css # Styling
 │ └── script.js # Frontend logic
 │── Bhagavad-gita-As-It-Is-English.pdf # Knowledge source
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/your-username/BhagavadGita-Chatbot.git
cd BhagavadGita-Chatbot
```
2️⃣ Create Virtual Environment (recommended)
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Add Environment Variables
Create a .env file:
```bash
HUGGINGFACEHUB_API_TOKEN=your_api_key_here
```
5️⃣ Run the App
```bash
python app.py
```
Visit 👉 http://127.0.0.1:8080/ in your browser.

Deployment with Docker (Optional)
```bash
docker build -t gita-chatbot .
docker run -d -p 5000:5000 --env-file .env gita-chatbot
```

Future Enhancements
- Voice-enabled chat with Krishna
- Support for additional languages (Hindi, Sanskrit, Marathi)
- Rich mobile experience (PWA)
- Persistent session storage for multi-user environments

Acknowledgments
- Bhagavad Gita — timeless source of divine wisdom
- LangChain — elegant RAG implementation
- HuggingFace — for inference APIs
- GitHub & Render — for deployment support
