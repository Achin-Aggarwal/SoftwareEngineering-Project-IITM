import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.document_loaders.base import Document
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Directory setup
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(current_dir, "dataset")
BDM_dir = os.path.join(dataset_dir, "BDM")
MLP_dir = os.path.join(dataset_dir, 'MLP')
MAD1_dir = os.path.join(dataset_dir, 'MAD1')
MAD2_dir = os.path.join(dataset_dir, 'MAD2')
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db")

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text.strip()

if not os.path.exists(persistent_directory):
    print("Persistent directory does not exist. Initializing vector store...")

    # Check if all required directories exist
    for dir_path in [BDM_dir, MLP_dir, MAD1_dir, MAD2_dir]:
        if not os.path.exists(dir_path):
            raise FileNotFoundError(
                f"The directory {dir_path} does not exist. Please check the path."
            )

    print("-------Starting Extraction-----------")
    documents = []

    # Process all subjects
    subject_dirs = [BDM_dir, MLP_dir, MAD1_dir, MAD2_dir]
    for subject_dir in subject_dirs:
        subject_name = os.path.basename(subject_dir)
        
        # Process weeks
        for week in range(1, 13):
            week_folder = os.path.join(subject_dir, f"Week-{week:02d}")
            if not os.path.exists(week_folder):
                continue
                
            # Process document types
            doc_types = ["Lecture", "Transcript", "Graded Assignment", "Practise Assignment"]
            for doc_type in doc_types:
                doc_folder = os.path.join(week_folder, doc_type)
                if not os.path.exists(doc_folder):
                    continue
                    
                # Process PDF files
                for pdf_file in os.listdir(doc_folder):
                    if not pdf_file.lower().endswith('.pdf'):
                        continue
                        
                    pdf_path = os.path.join(doc_folder, pdf_file)
                    text = extract_text_from_pdf(pdf_path)
                    
                    if text:
                        doc = Document(
                            page_content=text,
                            metadata={
                                "source": pdf_file,
                                "subject": subject_name,
                                "week": 'Week-'+ str(week),
                                "doc_type": doc_type
                            }
                        )
                        documents.append(doc)
                        print(f"Processed: {subject_name} - Week {week} - {doc_type} - {pdf_file}")
    
    print("---------Extraction Completed-------------")

    print("------------Starting to Split--------------")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print("------------Splitting Completed-------------")

    print("----Document Chunks Information-----")
    print(f"Number of document chunks: {len(docs)}")

    print("-----Creating Embeddings-----")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("-----Finished Creating Embeddings-----")

    print("------Creating and persisting vector store----")
    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=persistent_directory
    )
    print("-----Finished Creating and Persisting Vector Store-----")

else:
    print("Vector store already exists. No need to initialize")