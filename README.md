# CALL.E: AI-Powered L1 Customer Care Automation

<p align="center">
  <img src="https://github.com/user-attachments/assets/b506abe4-acbd-4d1d-8673-48b530ba6417" alt="CALL.E Logo" width="200"/>
</p>

<p align="center">
  <strong>Built by Ninja Developers</strong><br>
  An intelligent, self-learning customer support engine designed to automate and elevate Level 1 customer interactions.
</p>

---

## 🎯 The Problem

Traditional customer care is struggling. Businesses face missed engagement opportunities, skilled agents are bogged down by repetitive tasks, disconnected bots create frustrating experiences, and high costs make advanced AI solutions inaccessible for many.

## ✨ Our Solution

**CALL.E** is a real-time, self-learning support engine that provides a seamless, 24/7 support experience across chat and voice. Our closed-loop system ensures context is never lost, conversations resume seamlessly after interruptions, and your team is free to focus on high-impact issues.

It features two core components:
- **`CALL.X`**: Manages all incoming customer support queries with persistent memory.
- **`CALL.O`**: Handles automated outgoing follow-ups, re-engagement, and bulk calling campaigns.

## 🚀 Key Features

- **Seamless Two-Way Communication**: A fully integrated system where `CALL.X` handles incoming queries and `CALL.O` manages proactive, automated follow-ups. If a query is unresolved, `CALL.O` automatically re-engages the customer once a solution is available.

- **Dynamic AI Agents**: Select a context-specific agent type (e.g., Sales, Medical, Support). The AI instantly adjusts its tone, vocabulary, and script to match the domain, ensuring professional and effective interactions.

- **Real-Time Multilingual Support**: The AI can detect a user's language and switch to it in real-time during a call, using a sophisticated translation engine to ensure natural, fluent conversation.

- **Scalable Bulk Calling**: Launch mass outreach campaigns to thousands of contacts simultaneously. Our distributed architecture ensures every call is handled in parallel without delays.

## 🛠️ Tech Stack

| Category                  | Technologies                                                              |
| ------------------------- | ------------------------------------------------------------------------- |
| **Frontend**              | React, TypeScript, Vite, Tailwind CSS                                     |
| **Backend**               | Node.js, Express.js, Python, FastAPI                                      |
| **AI & Machine Learning** | PyTorch, Transformers (BART), Amazon Nova, OpenCV, AWS Rekognition        |
| **Database**              | MySQL, Redis                                                              |
| **APIs & Integrations**   | Twilio                                                                    |
| **Cloud & DevOps**        | AWS (S3, EC2), Docker                                                     |

## 🏗️ Architecture


*(Replace the link above with a link to your hosted architecture diagram image)*

## 📂 Project Structure

```
.
├── backend
│   ├── src
│   │   ├── chains.py
│   │   ├── models.py
│   │   ├── prompts.py
│   │   ├── speech_to_text.py
│   │   ├── stages.py
│   │   ├── text_to_speech.py
│   │   ├── tools.py
│   │   └── vector_store.py
│   ├── vector_store/knowledge_base
│   │   ├── index.faiss
│   │   └── index.pkl
│   ├── app.py
│   ├── main.py
│   ├── requirements.txt
│   └── twilio_call.py
├── frontend
│   ├── public/
│   ├── src/
│   ├── .gitignore
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Getting Started

### Prerequisites
- Node.js and npm
- Python and pip
- An account with Twilio and AWS
- Git

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/cyfuture.git
    cd cyfuture
    ```

2.  **Setup the Backend:**
    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *Create a `.env` file and add your environment variables (API keys for Twilio, AWS, etc.).*

3.  **Setup the Frontend:**
    ```sh
    cd ../frontend
    npm install
    ```
    *Create a `.env` file if needed for frontend variables.*

### Running the Application

1.  **Start the Backend Server:**
    ```sh
    # From the 'backend' directory
    uvicorn app:app --reload
    ```

2.  **Start the Frontend Development Server:**
    ```sh
    # From the 'frontend' directory
    npm run dev
    ```

The application should now be running on `http://localhost:5173`.

## 🏆 The Team: Ninja Developers

- Samir Kumar
- Bisal Prasad
- Subrata Lodh
- Kaushik Bhowmick
- Chinmoy Dutta

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for
