# Generative Monster

![](https://pbs.twimg.com/media/FvnwKZ_XwAIXmW0?format=jpg&name=small)

Fully autonomous generative/AI artist.

It uses ChatGPT (through LangChain) to choose a topic of its interest, then
describes it as a OpenJourney prompt, generating a new image every day and
sharing it at [@generativemnstr](https://twitter.com/generativemnstr).

More models to be added in the future.

# Installing

## Locally

First of all, create a `.env` file with the following env vars set:

```
# Twitter
TWITTER_CONSUMER_KEY = ...
TWITTER_CONSUMER_SECRET = ...
TWITTER_BEARER_TOKEN = ...
TWITTER_ACCESS_TOKEN = ...
TWITTER_ACCESS_TOKEN_SECRET= ...

# Hugging Face
HUGGINGFACE_API_TOKEN = ...

# OpenAI
OPENAI_API_KEY = ...
```

Create a Python virtual env and install the dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install .
```

# Running

Run the full creation chain: inspiration, prompt engineering, image generation
and communication:

```
python generative_monster/cli.py create
```

Useful to debug, run only prompt engineering and image generation:

```
python generative_monster/cli.py create-from-prompt "some prompt" "some style"
```

Note that the styles are the ones supported in `generative_monster/prompts.py`.