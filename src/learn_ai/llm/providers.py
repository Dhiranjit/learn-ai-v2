import os 
from dotenv import load_dotenv
load_dotenv()


PROVIDERS = {
    "groq": {
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1"    
    },
    "nvidia": {
        "api_key": os.getenv("NVIDIA_API_KEY"),
        "base_url": "https://integrate.api.nvidia.com/v1"    
    }
}