"""
Interactive chat interface for StarBot
"""
from starbot.data.ingestion import DataIngestion
from starbot.models.config import ModelConfig
from starbot.models.retrieval import RetrievalQA

def main():
    print("=" * 50)
    print("Welcome to StarBot!")
    print("A chatbot that answers questions about Star College Durban")
    print("=" * 50)
    
    # Initialize components
    print("\nInitializing StarBot...")
    data_ingestion = DataIngestion()
    model_config = ModelConfig()
    
    # Load data from Star College Durban website
    print("Ingesting data from Star College Durban website...")
    docs = data_ingestion.ingest_website('https://starcollegedurban.co.za/')
    print(f"Ingested {len(docs)} document chunks")
    
    # Create vector store
    vector_store = data_ingestion.create_vector_store(docs, 'star-college')
    print("Vector store created successfully")
    
    # Initialize QA system with streaming for better user experience
    qa_system = RetrievalQA(
        vector_store=vector_store, 
        llm=model_config.get_llm(streaming=True)
    )
    print("QA system initialized")
    
    print("\nStarBot is ready! Type 'exit' to quit.")
    
    # Chat loop
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "q"]:
            print("\nThank you for chatting with StarBot. Goodbye!")
            break
            
        print("\nStarBot: ", end="")
        answer = qa_system.answer_question(user_input)
        print()  # Add a newline after the streaming response

if __name__ == "__main__":
    main()
