import os, sys
from dotenv import load_dotenv
from client import bot

if __name__ == "__main__":
    load_dotenv()

    # Get the token
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("[ERROR] BOT_TOKEN environment variable not set. Add it do the .env file.")
        sys.exit()

    # Start the bot
    bot.run(token)
