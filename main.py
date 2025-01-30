import discord
import os
from openai import AsyncOpenAI

# Load environment variables (store your bot token and API key in a .env file)
from dotenv import load_dotenv
load_dotenv()

# Replace with your Discord bot token and OpenAI API key in the .env file
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Replace with the specific channel ID you want the bot to listen to
TARGET_CHANNEL_ID = 1334319741346643998

# Initialize the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Initialize the OpenAI client
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def ask_openai(question):
    """Send a question to OpenAI's API and return the response."""
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while calling the OpenAI API: {e}"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Only respond in the target channel
    if message.channel.id == TARGET_CHANNEL_ID:
        try:
            # Send the question to OpenAI
            response = await ask_openai(message.content)

            # Send the response back to the channel
            await message.channel.send(response)
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

# Run the bot
client.run(TOKEN)