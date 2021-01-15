# Party Parrot Discord Bot

![github-party-parrot](https://cultofthepartyparrot.com/parrots/hd/githubparrot.gif)

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

First, install all the dependencies with `pip install -r requirements.txt`. Run the server 
with `python run.py`. Simple steps to deploy on Ubuntu in the background:

1. Pull the source code `git pull origin master`
2. Kill the current process running (it's the shell process running `runbot.sh`)
3. Restart the process in the background `nohup ./scripts/runbot.sh &`
4. Ensure the process is running with `ps ax | grep runbot.sh`

A better alternative to the above is to run the bot as a service. Go to 
`/etc/systemd/system` and create a unit file named `party-parrot-bot.service`
that contains the contents:

```ini
[Unit]
Description=party parrot bot

[Service]
User=<your user name>
WorkingDirectory=<absolute_path_to_wherever_the_source_code_is>
ExecStart=<absolute_wherever_source_code_is>/<virtual_env_name>/bin/python <absolute_wherever_source_code_is>/run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable the service with 

```bash
sudo systemctl enable party-parrot-bot
```

And start the service with

```bash
sudo systemctl start party-parrot-bot
```

Monitor the logs with

```bash
sudo journalctl party-parrot-bot
```
