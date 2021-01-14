from discord.ext import commands
import discord
import os
from pretty_help import PrettyHelp
from cogs.home_cinema import scripts, scripts_running
from cogs.spam_bot import spamming_emotes, spamming_messages

TOKEN = str(os.environ['TOKEN'])

# 2
bot = commands.Bot(command_prefix='$', help_command=PrettyHelp())

extensions = ["HomeCinema", "SpamBot"]

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="clear", help="clears the last 'n' messages, defaulting to 100", hidden=True)
async def clear(ctx, the_limit=100):
    print("running: clear")
    the_message: discord.Message = ctx.message

    if(the_message):
        await the_message.delete()

    the_channel = ctx.channel

    the_commands = list(map(lambda x: bot.command_prefix + x.name, bot.commands))

    if(the_channel):
        async for message in the_channel.history(limit=the_limit):
            if message.author.name == "Spam Bot" or message.content in the_commands:
                await message.delete()
            else:
                for command in the_commands:
                    if(message.content.startswith(command)):
                        await message.delete()
                        break

@bot.command(name="stop", help="Stops the bot from reading the movie script or spamming emotes, defaults to movies")
async def stop(ctx, spam_type="movie"):
    print("running: stop")
    the_guild = ctx.guild

    if(the_guild):
        if(spam_type == "movie"):
            if(the_guild not in scripts_running or not scripts_running[the_guild]):
                await ctx.send("What are you trying to stop, you dumbf*uck?")
            else:
                if(scripts_running[the_guild]):
                    scripts[the_guild].clear()
                    await ctx.send("Stoping movie script playback")
                    scripts_running[the_guild] = False
                    del scripts[the_guild]
        elif(spam_type == "emote"):
            if(the_guild not in spamming_emotes or not spamming_emotes[the_guild]):
                await ctx.send("What are you trying to stop, you dumbf*uck?")
            else:
                if(spamming_emotes[the_guild]):
                    await ctx.send("Stoping emote spam playback")
                    spamming_emotes[the_guild] = False
        elif(spam_type == "spam"):
            if(the_guild not in spamming_messages or not spamming_messages[the_guild]):
                await ctx.send("What are you trying to stop, you dumbf*uck?")
            else:
                if(spamming_messages[the_guild]):
                    await ctx.send("Stoping message spam")
                    spamming_messages[the_guild] = False


@bot.event
async def on_command_error(ctx, error):
    print("ERROR", error, type(error))
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command doesn't currently exist!")
    #elif isinstance(error, commands.errors.CommandNotFound):
        #await ctx.send("You do not have permissions to use that command: try asking a server mod/admin")

if __name__ == "__main__":
    for extension in extensions:
        bot.load_extension("cogs." + extension)

    bot.run(TOKEN)
