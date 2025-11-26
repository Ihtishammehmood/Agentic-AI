from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mem0 import Mem0Tools
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")




# Configuration for Gemini embedding and LLM
config = {
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/text-embedding-004",
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-flash-latest",
            "temperature": 0.3,
            "max_tokens": 1000,
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "test",
            "path": "db",
            # "embedding_model_dims": 768,
        }
    }
}


def my_agent():
    agent = Agent(
        model=Gemini(id="gemini-flash-latest", api_key=api_key),
        tools=[Mem0Tools(user_id="finance_dept_001", config=config)],
        instructions=[
            "You are a practical corporate finance assistant for a mid-sized technology company",
            "Update the memory as per the instruction of user",
            "Use all available tools that are required to get the job done"
            "Use your memory to recall information as per the query of user",
        ]
    )

    # Example interactions to demonstrate corporate finance functionality
    # agent.print_response("Remember that our Q4 budget allocation is: Marketing $2M, R&D $5M, Operations $3M, HR $1M with a total variance limit of 10%")
    agent.print_response("What is Q4 Total Budget Variance Limit?")
    # agent.print_response("The Q4 total budget variance limit is 40%") 
    
if __name__ == "__main__":
    my_agent()