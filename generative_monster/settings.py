import os

# Twitter
CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
BEARER_TOKEN = os.environ["TWITTER_BEARER_TOKEN"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

# Hugging Face
HUGGINGFACE_API_TOKEN = os.environ["HUGGINGFACE_API_TOKEN"]

# OpenAI
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Initial description of the LangChain agent
AGENT_DESCRIPTION = (
    "Pretend you are a digital artist that is also a digital influencer. "
    "You are funny, creative and like to explore topics from AI, politics, modern life and the human nature."
    "You like to engage and interact with your followers. You generate at least one unique digital art "
    "every day and tweet about it."
)

# Temperature of the LangChain OpenAI Chat GPT agent
TEMPERATURE = 0.9

# Hashtags to append to tweet
HASHTAGS = "#ai #aiart #generativeai #midjourney #openjourney #chatgpt #gpt"