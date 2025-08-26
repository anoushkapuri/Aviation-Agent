##This is the file where the PDF processor is defined. 
# It uses OpenAI embeddings to process the PDFs.

import PyPDF2
from typing import List, Dict, Optional, Any
import os
import logging
import pickle
import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
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
        self.cache_dir = os.path.join(os.path.dirname(__file__), "vector_cache")
        self.setup_logging()
        
        # Create default PDF directory if it doesn't exist
        if not os.path.exists(self.default_pdf_dir):
            os.makedirs(self.default_pdf_dir)
            self.logger.info(f"Created default PDF directory at: {self.default_pdf_dir}")
            
        # Create cache directory if it doesn't exist
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            self.logger.info(f"Created vector cache directory at: {self.cache_dir}")
    
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
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash for a file based on its path and modification time."""
        stat = os.stat(file_path)
        # Include file path, size, and modification time in hash
        hash_string = f"{file_path}_{stat.st_size}_{stat.st_mtime}"
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def _get_directory_hash(self, directory_path: str) -> str:
        """Generate hash for all PDF files in a directory."""
        pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
        pdf_files.sort()  # Ensure consistent ordering
        
        combined_hash = ""
        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory_path, pdf_file)
            if os.path.exists(pdf_path):
                combined_hash += self._get_file_hash(pdf_path)
        
        return hashlib.md5(combined_hash.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get the cache file path for a given cache key."""
        return os.path.join(self.cache_dir, f"{cache_key}.pkl")
    
    def _save_vector_store_to_cache(self, vector_store: FAISS, cache_key: str) -> bool:
        """Save vector store to cache directory using FAISS native format."""
        try:
            cache_path = os.path.join(self.cache_dir, cache_key)
            vector_store.save_local(cache_path)
            self.logger.info(f"Vector store cached at: {cache_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to cache vector store: {str(e)}")
            return False
    
    def _load_vector_store_from_cache(self, cache_key: str) -> Optional[FAISS]:
        """Load vector store from cache directory using FAISS native format."""
        try:
            cache_path = os.path.join(self.cache_dir, cache_key)
            if not os.path.exists(cache_path):
                return None
                
            vector_store = FAISS.load_local(cache_path, self.embeddings, allow_dangerous_deserialization=True)
            self.logger.info(f"Vector store loaded from cache: {cache_path}")
            return vector_store
        except Exception as e:
            self.logger.error(f"Failed to load vector store from cache: {str(e)}")
            return None
    
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
        """Process PDF and create vector store with caching."""
        if pdf_path is None:
            # If no specific PDF is provided, process all PDFs in the default directory
            return self.process_directory(self.default_pdf_dir)
            
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return None
        
        # Generate cache key based on file hash
        cache_key = f"single_pdf_{self._get_file_hash(pdf_path)}"
        
        # Try to load from cache first
        cached_vector_store = self._load_vector_store_from_cache(cache_key)
        if cached_vector_store is not None:
            self.processed_files.append(pdf_path)
            self.logger.info(f"Loaded from cache: {pdf_path}")
            return cached_vector_store
        
        # If not in cache, process the PDF
        self.logger.info(f"Processing PDF (not in cache): {pdf_path}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if text is None:
            return None
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create vector store using OpenAI embeddings
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        self.processed_files.append(pdf_path)
        
        # Cache the vector store for future use
        self._save_vector_store_to_cache(vector_store, cache_key)
        self.logger.info(f"Successfully processed and cached: {pdf_path}")
        
        return vector_store
    
    def process_directory(self, directory_path: str = None) -> Optional[FAISS]:
        """Process all PDFs in a directory and combine into one vector store with caching."""
        if directory_path is None:
            directory_path = self.default_pdf_dir
            
        if not self.validate_directory(directory_path):
            return None
        
        # Generate cache key based on directory contents hash
        cache_key = f"directory_{self._get_directory_hash(directory_path)}"
        
        # Try to load from cache first
        cached_vector_store = self._load_vector_store_from_cache(cache_key)
        if cached_vector_store is not None:
            # Update processed files list for tracking
            for filename in os.listdir(directory_path):
                if filename.endswith('.pdf'):
                    pdf_path = os.path.join(directory_path, filename)
                    if os.path.exists(pdf_path):
                        self.processed_files.append(pdf_path)
            self.logger.info(f"Loaded directory from cache: {directory_path}")
            return cached_vector_store
        
        # If not in cache, process all PDFs
        self.logger.info(f"Processing directory (not in cache): {directory_path}")
        
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
            
        # Create combined vector store using OpenAI embeddings
        vector_store = FAISS.from_texts(all_chunks, self.embeddings)
        
        # Cache the vector store for future use
        self._save_vector_store_to_cache(vector_store, cache_key)
        self.logger.info(f"Processing complete. Successfully processed {processed_count} PDFs, {failed_count} failed. Cached for future use.")
        
        return vector_store
    
    def get_processed_files(self) -> List[str]:
        """Get list of successfully processed PDF files."""
        return self.processed_files
        
    def get_default_pdf_directory(self) -> str:
        """Get the path to the default PDF directory."""
        return self.default_pdf_dir
    
    def clear_cache(self) -> bool:
        """Clear all cached vector stores."""
        try:
            import shutil
            if os.path.exists(self.cache_dir):
                for item in os.listdir(self.cache_dir):
                    item_path = os.path.join(self.cache_dir, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        self.logger.info(f"Removed cache directory: {item}")
                    elif item.endswith(('.pkl', '.faiss', '.index')):
                        os.remove(item_path)
                        self.logger.info(f"Removed cache file: {item}")
            self.logger.info("Cache cleared successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about cached files."""
        cache_info = {
            "cache_directory": self.cache_dir,
            "cached_stores": [],
            "total_cache_size": 0
        }
        
        if os.path.exists(self.cache_dir):
            for item in os.listdir(self.cache_dir):
                item_path = os.path.join(self.cache_dir, item)
                if os.path.isdir(item_path):
                    # Calculate directory size
                    dir_size = 0
                    for dirpath, dirnames, filenames in os.walk(item_path):
                        for filename in filenames:
                            filepath = os.path.join(dirpath, filename)
                            dir_size += os.path.getsize(filepath)
                    
                    cache_info["cached_stores"].append({
                        "store_name": item,
                        "size_bytes": dir_size,
                        "size_mb": round(dir_size / (1024 * 1024), 2)
                    })
                    cache_info["total_cache_size"] += dir_size
        
        cache_info["total_cache_size_mb"] = round(cache_info["total_cache_size"] / (1024 * 1024), 2)
        return cache_info 