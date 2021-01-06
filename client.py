import discord
import string
from utils import Parrot, get_parrots_from_site
from nltk.corpus import stopwords
from discord.ext import commands

# Set up some globals
CHARACTER_LIMIT = 2000
english_stopwords = stopwords.words('english')

# Initialize the bot
description = '''🦜 A bot to send party parrots. Party or die. 🦜'''
bot = commands.Bot(command_prefix='%', description=description)
bot.parrot_list = []


def find_parrot(parrot: str) -> Parrot:
    """
    Helper function to find the parrot object in the bot's parrot list
    """

    query = parrot.lower().replace(' ', '')

    # Search for exact mathces
    for p in bot.parrot_list:
        if query == p.id:
            return p
    
    # Search for substrings
    for p in bot.parrot_list:
        if query in p.id:
            return p

    return None

@bot.event
async def on_ready():
    """
    Initializes the bot's parrot list and does other initializion stuff
    """

    print(f'Logged in as {bot.user.name} with id {bot.user.id}')

    # Load the parrots from the site
    bot.parrot_list = get_parrots_from_site()
    print('Parrots loaded.')

    # Set the status
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, 
        name="parrot beats 🦜"
    ))

    print('Bot ready 👍🦜')
    
@bot.event
async def on_message(message):
    """
    Sets up the on message listener. Sends a party parrot if any of the words
    in the message match words in the party parrots. If the message begins with
    the prefix, then go to the command dispatcher.
    """

    # Don't send to ourselves
    if message.author.id == bot.user.id:
        return

    # Check for the command prefix
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    # Set to lowercase, remove punctuation
    cleaned_message = message.content.lower()
    cleaned_message = cleaned_message.translate(str.maketrans('', '', string.punctuation))

    # Iterate through all words in the message
    for word in cleaned_message.split():
        # Don't consider words with 2 or fewer characters or stop words
        if (len(word) <= 2) or (word in english_stopwords):
            continue

        # Attempt to find a parrot
        parrot_obj = find_parrot(word)
        if parrot_obj:
            # Send the first parrot found
            embed = discord.Embed()
            embed.set_image(url=parrot_obj.url)
            await message.channel.send(embed=embed)
            return

class PartyParrotCommands(commands.Cog):
    """
    Party parrot commands
    """

    description = "Party or die"

    @commands.command(name='parrot')
    async def parrot(ctx, *args):
        """
        Display a party parrot of your choosing
        """
        parrot_name = ' '.join(args)
        print(f'Received request for party parrot {parrot_name}')

        # Find the parrot object in the bot list
        parrot_obj = find_parrot(parrot_name)
        if not parrot_obj:
            print(f'Parrot {parrot_name} not found')
            await ctx.send(f'parrot {parrot_name} not found :(')
            return

        # Embed the parrot gif url
        embed = discord.Embed()
        embed.set_image(url=parrot_obj.url)
        await ctx.send(embed=embed)

    @commands.command(name='list')
    async def list_parrots(ctx, *args):
        """
        Lists all available party parrots
        """

        print('Listing parrots')
        parrots_str = 'Gaze upon all parrots of which I am cognizant:\n'
        old_parrots_str = parrots_str
        for i, parrot in enumerate(bot.parrot_list):
            parrots_str += f'{i+1}. {parrot.name}\n'

            # Send message if the parrot string is too long
            if len(parrots_str) > CHARACTER_LIMIT:
                await ctx.send(old_parrots_str)
                parrots_str = f'{i+1}. {parrot.name}\n'

            old_parrots_str = parrots_str

        # Send the remaining parrots
        await ctx.send(parrots_str)

bot.add_cog(PartyParrotCommands())