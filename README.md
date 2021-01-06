# Party Parrot Discord Bot

A Discord bot to display party parrots on command. It also
will insert party parrots where appropriate. Party or die.
Uses the [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
library to implement the bot. Invite link is 
[here](https://discord.com/api/oauth2/authorize?client_id=796102321322328126&permissions=52224&scope=bot).

Party parrots retrieved from the 
[Cult of the Party Parrot](https://cultofthepartyparrot.com/).
The bot scrapes the site for the name and url of the party parrot
on start and embeds the GIF's in the message.

## Commands

Command prefix is set as "%"

- **%parrot parrotname**: Displays a parrot on command containing the name "parrotname"
- **%list**: Lists parrots

## Deployment

Steps to deploy on Ubuntu:

1. Pull the source code `git pull origin master`
2. Kill the current process running (it's the shell process running `runbot.sh`)
3. Restart the process in the background `nohup ./scripts/runbot.sh &`
4. Ensure the process is running with `ps ax | grep runbot.sh`
