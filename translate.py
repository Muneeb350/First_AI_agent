from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os


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

while True:
    user_input = input("\n 📝 Please enter something in Urdu to translate:\n>")


    response = Runner.run_sync(
        translator,
        input= user_input,
        run_config= config
)
    
    print("Translation Result:", response.final_output)


    again = input ("\n 🔁 Do you want to translate something else? (yes/no):\n>")
    if again not in ["yes", "y"]:
        print("👋 Goodbye! Have a great day!")
        break