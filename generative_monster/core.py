import os
import json
import random

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
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict, HumanMessage

from generative_monster.interface.twitter import TwitterInterface
from generative_monster.generator.openjourney import OpenJourneyGenerator
from generative_monster.prompts import PROMPT_SUFFIXES

from settings import (
    AGENT_DESCRIPTION,
    HASHTAGS,
    TEMPERATURE
)


class Monster:

    def __init__(self):
        pass


    def create(self):
        # Inspiration
        print("-- Memory and inspiration")
        text = self.find_inspiration()
        print("Generated description:", text)
        if len(text) > 200:
            text = text[:190] + "..."
            print("Warning: It was too long! Shortening:", text)
        
        # Appending hashtags
        tweet_content = text + "\n\n" + HASHTAGS
        print("Tweet content:", tweet_content)

        # Deciding on style
        print("--- Style")
        available_styles = list(PROMPT_SUFFIXES.keys())
        selected_style = random.choice(available_styles)
        print("Selected style:", selected_style)

        # Prompt creation
        print("--- Prompt creation")
        prompt = self.create_prompt(text, style=selected_style)
        print("Final prompt:", prompt)

        # Image generation
        print("-- Image generation")
        image_path = self.generate(prompt)
        print("Generated image:", image_path)
        
        # Communication
        print("-- Communication")
        response = self.publish(tweet_content, [image_path])
        print("Tweet:", response)


    def create_from_prompt(self, initial_prompt, style):
        # Generate image from prompt straight
        prompt = self.create_prompt(initial_prompt, style)
        print("\tPrompt:", prompt)
        image_path = self.generate(prompt)
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

        llm = ChatOpenAI(temperature=TEMPERATURE)
        conversation = ConversationChain(
            memory=memory,
            prompt=prompt,
            llm=llm,
            verbose=False
        )

        gen_prompt = conversation.predict(
            input="Describe a painting in a short phrase, maximum of 10 words, about a topic of your choice. Limit the your answer to 100 characters. Do not quote.")
        
        # gen_text = conversation.predict(
        #     input="Write a tweet about your latest painting to share with your followers. Limit the answer to maximum 100 characters."
        # )

        # Save to memory
        with open("memory.json", "w") as f:
            memory_dict = messages_to_dict(memory.chat_memory.messages)
            json.dump(memory_dict, f)

        return gen_prompt.strip()


    def create_prompt(self, text, style="acrylic"):
        suffix = PROMPT_SUFFIXES[style]["suffix"]
        prompt = text + suffix
        return prompt


    def generate(self, prompt):
        gen = OpenJourneyGenerator()
        image_path = gen.generate(prompt)
        return image_path


    def publish(self, text, image_paths):
        ti = TwitterInterface()
        res = ti.tweet_with_images(text, image_paths)
        return res
