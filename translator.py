from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
import streamlit as st
import asyncio 

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

translator = Agent(
    name = "Translator Agent",
    instructions= """You are a translator agent! Translate any sentence from Urdu to English."""
)

st.set_page_config(page_title= "🌐 Translator", layout="wide")

async def translate_urdu(text):
            response = await Runner.run(
                translator,
                input= user_input,
                run_config= config
)
    
            return response.final_output

st.title("Urdu to english translater")


user_input = st.text_area("\n 📝 Please enter something in Urdu or Roman to translate:")

if st.button("Translate"):
    if user_input.strip() == "":
        st.warning("Please enter some text in Urdu or Roman.")
    else:
        
        try:  
            translator = asyncio.run(translate_urdu(user_input))
            st.success("✅ English Translation:")
            st.write(translator)

        except Exception as e:
            st.error(f"❌ Error during translation: {str(e)}")


    