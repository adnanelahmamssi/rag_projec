from sklearn.metrics import precision_score, recall_score, f1_score
import re
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextRelevance
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import SentenceTransformerEmbeddings
from datasets import Dataset
import os
from dotenv import load_dotenv

load_dotenv()

class Evaluator:
    @staticmethod
    def evaluate_retrieval(retrieved_docs, relevant_docs):
        """Evaluate retrieval performance."""
        # Simple binary relevance
        retrieved_set = set(doc.page_content[:100] for doc in retrieved_docs)
        relevant_set = set(relevant_docs)

        true_positives = len(retrieved_set & relevant_set)
        precision = true_positives / len(retrieved_set) if retrieved_set else 0
        recall = true_positives / len(relevant_set) if relevant_set else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }

    @staticmethod
    def evaluate_generation(response, ground_truth):
        """Simple evaluation of generated response."""
        # Basic checks: length, keyword overlap
        response_words = set(re.findall(r'\b\w+\b', response.lower()))
        truth_words = set(re.findall(r'\b\w+\b', ground_truth.lower()))
        overlap = len(response_words & truth_words)
        total = len(response_words | truth_words)
        jaccard = overlap / total if total else 0

        return {
            "response_length": len(response),
            "jaccard_similarity": jaccard
        }

    @staticmethod
    def evaluate_with_ragas(question, answer, contexts, ground_truth):
        """Evaluate using RAGAS framework."""
        # Set env for RAGAS
        os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")
        
        data = {
            "question": [question],
            "answer": [answer],
            "contexts": [[ctx[:500] for ctx in contexts]],  # Truncate each context to 500 chars
            "ground_truth": [ground_truth]
        }
        dataset = Dataset.from_dict(data)
        
        # Set up embeddings
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Evaluate with selected metrics
        result = evaluate(
            dataset=dataset,
            metrics=[Faithfulness(), AnswerRelevancy(), ContextRelevance()],
            llm=ChatOpenAI(
                model_name="llama-3.1-8b-instant",
                openai_api_key=os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1"
            ),
            embeddings=embeddings
        )
        
        return result