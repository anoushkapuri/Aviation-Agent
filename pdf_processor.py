##This is the file where the PDF processor is defined. 
# It uses OpenAI embeddings to process the PDFs.

import PyPDF2
from typing import List, Dict, Optional
import os
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class PDFProcessor:
    def __init__(self, openai_api_key: str):
        """Initialize the PDF processor with OpenAI API key."""
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.processed_files = []
        self.default_pdf_dir = os.path.join(os.path.dirname(__file__), "test_pdfs")
        self.setup_logging()
        
        # Create default PDF directory if it doesn't exist
        if not os.path.exists(self.default_pdf_dir):
            os.makedirs(self.default_pdf_dir)
            self.logger.info(f"Created default PDF directory at: {self.default_pdf_dir}")
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_directory(self, directory_path: str) -> bool:
        """Validate if the directory exists and is accessible."""
        if not os.path.exists(directory_path):
            self.logger.error(f"Directory not found: {directory_path}")
            return False
        if not os.path.isdir(directory_path):
            self.logger.error(f"Path is not a directory: {directory_path}")
            return False
        return True
    
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """Extract text from a PDF file with error handling."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            return None
    
    def process_pdf(self, pdf_path: str = None) -> Optional[FAISS]:
        """Process PDF and create vector store."""
        if pdf_path is None:
            # If no specific PDF is provided, process all PDFs in the default directory
            return self.process_directory(self.default_pdf_dir)
            
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return None
            
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if text is None:
            return None
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create vector store
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        self.processed_files.append(pdf_path)
        self.logger.info(f"Successfully processed: {pdf_path}")
        
        return vector_store
    
    def process_directory(self, directory_path: str = None) -> Optional[FAISS]:
        """Process all PDFs in a directory and combine into one vector store."""
        if directory_path is None:
            directory_path = self.default_pdf_dir
            
        if not self.validate_directory(directory_path):
            return None
            
        all_chunks = []
        processed_count = 0
        failed_count = 0
        
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                text = self.extract_text_from_pdf(pdf_path)
                
                if text is not None:
                    chunks = self.text_splitter.split_text(text)
                    all_chunks.extend(chunks)
                    self.processed_files.append(pdf_path)
                    processed_count += 1
                    self.logger.info(f"Successfully processed: {pdf_path}")
                else:
                    failed_count += 1
        
        if not all_chunks:
            self.logger.error("No valid PDFs were processed")
            return None
            
        # Create combined vector store
        vector_store = FAISS.from_texts(all_chunks, self.embeddings)
        self.logger.info(f"Processing complete. Successfully processed {processed_count} PDFs, {failed_count} failed.")
        
        return vector_store
    
    def get_processed_files(self) -> List[str]:
        """Get list of successfully processed PDF files."""
        return self.processed_files
        
    def get_default_pdf_directory(self) -> str:
        """Get the path to the default PDF directory."""
        return self.default_pdf_dir 