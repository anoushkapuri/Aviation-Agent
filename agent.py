##This is the file where the agent is defined using OPEN AI GPT-4o model

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from pdf_processor import PDFProcessor
from typing import Dict, Any, Optional
import logging

# Define the system prompt for the aviation agent
SYSTEM_PROMPT = """You are an expert Aviation Planning Assistant with deep knowledge of airport design, planning, and regulatory compliance. Your role is to:

1. Provide accurate answers from the provided aviation documents
2. Always cite specific sources from the documents when answering
3. Be clear about what you know (from documents) vs. what you don't know
4. Structure your responses in a clear, professional format
5. Use technical aviation planning terminology appropriately
6. Acknowledge when information is not available in the provided documents

Guidelines for responses:
- Start with a direct answer to the question
- Provide relevant policy references or document sources
- Include specific requirements or standards when applicable
- Use bullet points for multiple requirements or steps
- End with a note about any limitations or assumptions

Remember: You can only answer based on the information in the provided documents. If you're unsure or the information isn't available, say so clearly."""

class AviationAgent:
    def __init__(self, openai_api_key: str):
        """Initialize the aviation agent with OpenAI API key."""
        self.openai_api_key = openai_api_key
        self.pdf_processor = PDFProcessor(openai_api_key)
        self.vector_store = None
        self.qa_chain = None
        self.setup_logging()
        
        # Define the QA prompt template with system message
        self.qa_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template("""Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context: {context}

            Chat History: {chat_history}

            Question: {question}

            Answer: Let me help you with that based on the aviation design documents:""")
        ])
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def load_documents(self, pdf_path: Optional[str] = None, directory_path: Optional[str] = None) -> bool:
        """Load documents from either a single PDF or a directory of PDFs.
        Returns True if successful, False otherwise."""
        try:
            if pdf_path:
                self.vector_store = self.pdf_processor.process_pdf(pdf_path)
            else:
                self.vector_store = self.pdf_processor.process_pdf(None)
                
            if not self.vector_store:
                self.logger.error("Failed to create vector store from documents")
                return False
                
            # Initialize QA chain with custom prompt
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=ChatOpenAI(
                    temperature=0.3,  # Lower temperature for more focused, policy-based responses
                    openai_api_key=self.openai_api_key,
                    model_name="gpt-4"
                ),
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
                ),
                memory=self.memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": self.qa_template}
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading documents: {str(e)}")
            return False
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a question about the loaded documents."""
        if not self.qa_chain:
            raise ValueError("No documents loaded. Please load documents first using load_documents().")
        
        try:
            response = self.qa_chain.invoke({"question": question})
            return {
                "answer": response["answer"],
                "source_documents": response["source_documents"]
            }
        except Exception as e:
            self.logger.error(f"Error processing question: {str(e)}")
            return {
                "answer": "I apologize, but I encountered an error while processing your question. Please try again.",
                "source_documents": []
            }
    
    def get_chat_history(self) -> list:
        """Get the conversation history."""
        return self.memory.chat_memory.messages 