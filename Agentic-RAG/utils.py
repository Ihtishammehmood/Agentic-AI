from agno.agent import Agent
from agno.models.google import Gemini
from agno.embedder.google import GeminiEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.sql import SQLTools
from agno.document.chunking.document import DocumentChunking
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.storage.agent.sqlite import SqliteAgentStorage
from dotenv import load_dotenv
import os
import shutil

db_file_path = "assets/Chinook.db"
db_url = f"sqlite:///{os.path.abspath(db_file_path)}"

load_dotenv()


def reset_data_folder():
    """Clears the data folder and recreates it"""
    data_dir = "data"
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir, exist_ok=True)


def save_uploaded_files(uploaded_files):
    """Saves uploaded files to data folder"""
    reset_data_folder()
    for file in uploaded_files:
        with open(os.path.join("data", file.name), "wb") as f:
            f.write(file.getbuffer())


def initialize_agent():
    """Initializes the RAG agent with current documents"""
    return Agent(
        model=Gemini(id="gemini-2.0-flash"),
        knowledge=PDFKnowledgeBase(
            path="data/",
            vector_db=LanceDb(
                table_name="documents",
                uri="tmp/lancedb",
                search_type=SearchType.hybrid,
                embedder=GeminiEmbedder(),
            ),
            chunking_strategy=DocumentChunking(chunk_size=1500, overlap=150)
        ),
        show_tool_calls=True,
        search_knowledge=True,
        markdown=True,
        tools=[DuckDuckGoTools(),
               CalculatorTools(
            add=True,
            subtract=True,
            multiply=True,
            divide=True,
            exponentiate=True,
            factorial=True,
            is_prime=True,
            square_root=True,
        ),
            YFinanceTools(stock_price=True, analyst_recommendations=True,
                          stock_fundamentals=True),
            SQLTools(db_url=db_url)
               ],
        instructions=[
            "Answer the user's questions to the best of your ability.",
            "Use tools based on your reasoning and the user's questions.",
            "If you are not able to use one tool to answer the question, use another tool.",
        ],
        storage=SqliteAgentStorage(table_name="agent_sessions",
                                   db_file="agent_storage/data.db"),
        add_history_to_messages=True,
        num_history_responses=3

    )
