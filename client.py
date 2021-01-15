import discord
import string
from random import randint
from utils import Parrot, get_parrots_from_site
from nltk.corpus import stopwords
from discord.ext import commands, tasks

# Settings
SEND_PARROT_IN_REGULAR_MESSAGES = False
POSITIVE_MESSAGE_LOOP_HOURS = 46

# Set up some globals
CHARACTER_LIMIT = 2000
english_stopwords = stopwords.words('english')

# Initialize the bot
description = '''🦜 A bot to send party parrots. Party or die. 🦜 '''
bot = commands.Bot(command_prefix='%', description=description)
bot.parrot_list = []



## Utility functions

def find_parrot(parrot: str, search_subtrings=False) -> Parrot:
    """
    Helper function to find the parrot object in the bot's parrot list
    """

    # Search for exact matches on the id
    query_id = parrot.lower().replace(' ', '')
    for p in bot.parrot_list:
        if query_id == p.id:
            return p
    
    # Search for substrings
    query_strings = parrot.lower().split()
    for p in bot.parrot_list:
        # Iterate through each word in the parrot name
        for parrot_name_str in p.name.lower().split():
            if parrot_name_str in query_strings:
                return p
        
        # Iterate through each query string
        for query_str in query_strings:
            if query_str in p.name.lower().split():
                return p

    # Search substrings if specified
    if search_subtrings:
        for p in bot.parrot_list:
            if query_id in p.id:
                return p

    return None

def random_parrot() -> Parrot:
    """Retrives a random parrot for your pleasure

    Returns:
        Parrot: The random parrot object chosen
    """
    # Get a random parrot
    pi = randint(0, len(bot.parrot_list))
    parrot_obj = bot.parrot_list[pi]
    return parrot_obj



## Event listeners

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

    # Check for mentions
    if bot.user.mentioned_in(message):
        await message.channel.send("pls stop bothering me, i am partying")
        return

    # Custom PARTY OR DIE message
    if 'party?' in message.content.lower():
        embed = discord.Embed()
        parrot_obj = next((p for p in bot.parrot_list if p.id == 'partyparrot'), None)
        embed.set_image(url=parrot_obj.url)
        await message.channel.send('PARTY OR DIE!', embed=embed)
        return

    # Do nothing else if regular messages aren't enabled
    if not SEND_PARROT_IN_REGULAR_MESSAGES:
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



## Commands

@bot.command(name='parrot')
async def parrot(ctx, *args):
    """
    Display a party parrot of your choosing
    """
    parrot_name = ' '.join(args)
    print(f'Received request for party parrot {parrot_name}')

    # Find the parrot object in the bot list
    parrot_obj = find_parrot(parrot_name, search_subtrings=True)
    if not parrot_obj:
        print(f'Parrot {parrot_name} not found')
        await ctx.send(f'parrot {parrot_name} not found :(')
        return

    # Embed the parrot gif url
    embed = discord.Embed()
    embed.set_image(url=parrot_obj.url)
    await ctx.send(embed=embed)

@bot.command(name='random')
async def random_parrot_request(ctx, *args):
    """
    Display a random party parrot
    """
    # Get random parrot
    parrot_obj = random_parrot()

    # Embed the parrot gif url
    embed = discord.Embed()
    embed.set_image(url=parrot_obj.url)
    await ctx.send(embed=embed)


@bot.command(name='list')
async def list_parrots(ctx, *args):
    """
    Lists all available party parrots
    """

    print('Listing parrots')
    parrots_str = 'Gaze upon all parrots of which I am cognizant:\n'
    old_parrots_str = parrots_str
    for i, parrot in enumerate(bot.parrot_list):
        parrots_str += f'{i+1}. {parrot.name} ({parrot.id})\n'

        # Send message if the parrot string is too long
        if len(parrots_str) > CHARACTER_LIMIT:
            await ctx.send(old_parrots_str)
            parrots_str = f'{i+1}. {parrot.name} ({parrot.id})\n'

        old_parrots_str = parrots_str

    # Send the remaining parrots
    await ctx.send(parrots_str)



## Background tasks

@tasks.loop(hours=POSITIVE_MESSAGE_LOOP_HOURS)
async def positive_message_loop():
    """
    Set up a loop to send a positive message and a parrot every so often
    """
    # Get the main channel
    channel = bot.get_channel(749428787166314639)

    # Get random parrot
    parrot_obj = random_parrot()

    # Embed the parrot gif url
    embed = discord.Embed()
    embed.set_image(url=parrot_obj.url)

    # Send the message
    msg = 'you all are beautiful and deserve happiness, so here\'s a random parrot to lighten the mood for you:'
    await channel.send(msg, embed=embed)

@positive_message_loop.before_loop
async def wait_for_bot_ready():
    """
    Wait until the bot is ready until we send
    """
    await bot.wait_until_ready()

# Start background tasks
positive_message_loop.start()