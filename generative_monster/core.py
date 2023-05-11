import openai
import os
import json
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()

from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict, HumanMessage

from generative_monster.interface.twitter import TwitterInterface
from generative_monster.generator.openjourney import OpenJourneyGenerator
from generative_monster.prompts import PROMPT_SUFFIXES

AGENT_DESCRIPTION = (
    "Pretend you are a digital artist that is also a digital influencer. "
    "You like to engage and interact with your followers. You generate at least one unique digital art "
    "every day and tweet about it."
)


class Monster:

    def __init__(self):
        pass


    def create(self):
        # Inspiration
        print("-- Memory and inspiration")
        initial_prompt, text = self.find_inspiration()
        print("\tTweet:", text, "\n\tInitial prompt:", initial_prompt)
        if len(text) > 200:
            text = text[:190] + "..."
            print("It was too long! Shortening:", text)
        
        # Prompt creation
        print("--- Prompt creation")
        prompt = self.create_prompt(initial_prompt, style="acrylic")
        print("\tFinal prompt:", prompt)

        # Image generation
        print("-- Image generation")
        image_path = self.generate(prompt)
        print("\tImage:", image_path)
        
        # Communication
        print("-- Communication")
        response = self.publish(text, [image_path])
        print("\tTweet:", response)


    def create_from_prompt(self, initial_prompt, style):
        # Generate image from prompt straight
        prompt = m.create_prompt(initial_prompt, style)
        print("\tPrompt:", prompt)
        image_path = m.generate(prompt)
        print("\tImage:", image_path)


    def find_inspiration(self):
        # TODO Search twitter for daily headlines? Movies? TVSeries?

        # Recover memory
        if os.path.exists("memory.json"):
            # Use existing memory
            with open("memory.json", "r") as f:
                memory_dict = json.load(f)
                messages = messages_from_dict(memory_dict)
                memory = ConversationBufferMemory(return_messages=True)
                # Constraint 
                max_messages = 10
                for message in messages[-max_messages:]:
                    if isinstance(message, HumanMessage):
                        memory.chat_memory.add_user_message(message.content)
                    else:
                        memory.chat_memory.add_ai_message(message.content)
        else:
            # Or create new one
            memory = ConversationBufferMemory(return_messages=True)
        memory.load_memory_variables({})

        # Create a prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(AGENT_DESCRIPTION),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        llm = ChatOpenAI(temperature=0)
        conversation = ConversationChain(
            memory=memory,
            prompt=prompt,
            llm=llm,
            verbose=True
        )

        gen_prompt = conversation.predict(
            input="Describe a painting in max 10 words about a topic of your choice. Limit the answer to 100 characters.")
        
        gen_text = conversation.predict(
            input="Write a tweet about your latest painting to share with your followers. Limit the answer to maximum 100 characters."
        )

        # Save to memory
        with open("memory.json", "w") as f:
            memory_dict = messages_to_dict(memory.chat_memory.messages)
            json.dump(memory_dict, f)

        return gen_prompt.strip(), gen_text.strip()


    def create_prompt(self, text, style="acrylic"):
        suffix = PROMPT_SUFFIXES[style]["suffix"]
        prompt = text + suffix
        print("prompt", prompt, len(prompt))
        return prompt


    def generate(self, prompt):
        gen = OpenJourneyGenerator()
        image_path = gen.generate(prompt)
        return image_path


    def publish(self, text, image_paths):
        ti = TwitterInterface()
        res = ti.tweet_with_images(text, image_paths)
        return res

m = Monster()
m.create()