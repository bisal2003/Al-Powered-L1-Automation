# import os
# import wandb
# from .models import get_llm
# from pinecone import Pinecone , ServerlessSpec
# from dotenv import load_dotenv
# from langchain.chains import RetrievalQA
# from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_pinecone import PineconeVectorStore
# from langchain_huggingface import HuggingFaceEmbeddings


# # Load environment variables
# load_dotenv()

# # Initialize wandb
# wandb.init(project="rag-pipeline", name="llm-invocations", mode="online")

# # Initialize Pinecone vector store
# def get_retriever():
#     index_name = 'call-agent-ai-2' # Load from env
#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-mpnet-base-v2",
        
#     )
#     docsearch = PineconeVectorStore.from_existing_index(
#         index_name=index_name,
#         embedding=embeddings
#     )
#     return docsearch.as_retriever(search_kwargs={'k': 2})

# llm1=get_llm()

# # # Initialize Groq LLM
# # def get_llm():
# #     return ChatGroq(
# #         model_name="llama-3.3-70b-versatile",
# #         temperature=0.9,
# #         api_key=os.getenv("GROQ_API_KEY"),
# #         max_tokens=512
# #     )

# # # Initialize Gemini LLM
# # def gemini_llm():
# #     os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
# #     return ChatGoogleGenerativeAI(
# #         model="gemini-1.5-flash",
# #         temperature=0.7,
# #         max_tokens=512,
# #         max_retries=2,
# #     )

# # Create the Retrieval Augmented Generation (RAG) chain
# def create_rag_chain(retriever, llm):
#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True
#     )
# # Function to invoke LLM and log to wandb & terminal
# def get_llm(llm1, query):
#     response = llm1.invoke(query)  # Directly hit LLM

#     # Convert response to string
#     response_text = str(response.content)  # Extracts text from AIMessage

#     # Log activity in wandb
#     wandb.log({
#         "query": query,
#         "response": response_text
#     })

#     # Print activity in terminal
#     print("\n===== WandB Activity Logged =====")
#     print(f"Query: {query}")
#     print(f"Response: {response_text}")
#     print("================================\n")

#     return response_text

# # Function to invoke LLM and log to wandb & terminal
# def run_query(rag_chain, query):
#     response = rag_chain.invoke(query)

#     # Log activity in wandb
#     wandb.log({
#         "query": query,
#         "response": response["result"],
#         "sources": [doc.metadata for doc in response["source_documents"]]
#     })

#     # Print activity in terminal
#     print("\n===== WandB Activity Logged =====")
#     print(f"Query: {query}")
#     print(f"Response: {response['result']}")
#     print(f"Sources: {[doc.metadata for doc in response['source_documents']]}")
#     print("================================\n")

#     return response["result"]

# # Example Usage
# if __name__ == "__main__":
#     retriever = get_retriever()
#     gemini_model = gemini_llm()
#     rag_chain = create_rag_chain(retriever, gemini_model)

#     query = "sell a product?"
#     result = get_llm(gemini_model, query)
#     print("Gemini Response:", result)