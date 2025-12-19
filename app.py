import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag.retriever import Retriever
from rag.indexer import Indexer
from rag.data_loader import DataLoader

st.title("RAG System - AI Knowledge Base")

# Initialize components
@st.cache_resource
def load_system():
    try:
        retriever = Retriever()
        return retriever
    except Exception as e:
        st.error(f"Failed to load the system: {str(e)}. Please ensure the vector database exists (run `python build_index.py`) and your OPENAI_API_KEY is set in .env.")
        return None

retriever = load_system()

if retriever:
    st.sidebar.header("System Status")
    st.sidebar.success("RAG System Loaded Successfully")

    # Query interface
    st.header("Ask Questions")
    query = st.text_input("Enter your question about AI and machine learning:")

    if st.button("Get Answer"):
        if query:
            with st.spinner("Generating answer..."):
                try:
                    answer = retriever.query(query)
                    st.success("Answer generated!")
                    st.write("**Question:**", query)
                    st.write("**Answer:**", answer)
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
        else:
            st.warning("Please enter a question.")

    # Evaluation section
    st.header("System Evaluation")
    eval_query = st.text_input("Enter a question for evaluation (optional):", key="eval_query")
    if st.button("Run RAGAS Evaluation"):
        if eval_query:
            from rag.evaluator import Evaluator
            evaluator = Evaluator()

            # Use entered query
            question = eval_query
            answer = retriever.query(question)
            contexts = [doc.page_content[:500] for doc in retriever.vectorstore.similarity_search(question, k=3)]
            # For demo, use a simple ground truth or skip
            ground_truth = "Sample ground truth for evaluation."

            ragas_results = evaluator.evaluate_with_ragas(question, answer, contexts, ground_truth)
            st.write("RAGAS Evaluation Results:")
            st.json(ragas_results.scores)
        else:
            st.warning("Please enter a question for evaluation.")

    # Document Viewer
    st.header("Scraped Documents")
    import os
    doc_dir = "data/documents"
    if os.path.exists(doc_dir):
        pdf_files = [f for f in os.listdir(doc_dir) if f.endswith('.pdf')]
        if pdf_files:
            st.write("Downloaded PDFs:")
            for pdf in pdf_files:
                st.write(f"- {pdf}")
            # Links
            links_file = os.path.join(doc_dir, "scraped_links.txt")
            if os.path.exists(links_file):
                st.write("Links to original sources:")
                with open(links_file, 'r') as f:
                    for line in f:
                        st.markdown(f"- [{line.strip()}]({line.strip()})")
        else:
            st.write("No PDFs found. Run scraping first.")
    else:
        st.write("Documents directory not found.")