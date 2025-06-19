# from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize Groq LLM
# def get_llm():
#     llm = ChatGroq(
#         model_name="llama-3.3-70b-versatile",
#         temperature=0.9,
#         api_key= os.getenv("GROQ_API_KEY"),
#         max_tokens=512
#     )

#     return llm


# def gemini_llm():

#     os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=0.7,
#         max_tokens=512,
#         max_retries=2,
#     )

#     return llm
import os
import wandb
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Function to initialize Groq LLM and log to wandb
def get_llm():
    # Ensure wandb is initialized before updating config
    # if wandb.run is None:
    #     wandb.init(project="rag-pipeline", name="llm-invocations", mode="online")

    # Initialize Groq LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.9,
        api_key=os.getenv("GROQ_API_KEY"),
        max_tokens=512
    )

    # Log model configuration to wandb
    # wandb.config.update({
    #     "model_name": "llama-3.3-70b-versatile",
    #     "temperature": 0.9,
    #     "max_tokens": 512,
    #     "max_retries": 2
    # })

    print("✅ Gemini LLM initialized and logged to wandb.")
    return llm
