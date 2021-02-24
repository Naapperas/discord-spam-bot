from discord.ext import commands
import discord
import os
from pretty_help import PrettyHelp

TOKEN = str(os.environ['TOKEN'])

intents = discord.Intents.default()
intents.members = True

# 2
bot = commands.Bot(command_prefix='$', help_command=PrettyHelp(), intents=intents)

extensions = ["home_cinema", "spam_bot"]

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
        spam_cog = bot.get_cog("Spam_Bot")
        cinema_cog = bot.get_cog("Home_Cinema")

        if(spam_type == "movie"):
            if not cinema_cog:
                await ctx.send("ERROR")
                return
            await cinema_cog.stop(ctx, the_guild)
        elif(spam_type in {"emote", "spam"}):
            if not spam_cog:
                await ctx.send("ERROR")
                return
            await spam_cog.stop(ctx, the_guild, spam_type)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('pong xd: {0}s'.format(round(bot.latency, 1)))

@bot.event
async def on_command_error(ctx, error):
    print("ERROR", error, type(error))
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command doesn't currently exist!")
    #elif isinstance(error, commands.errors.CommandNotFound):
        #await ctx.send("You do not have permissions to use that command: try asking a server mod/admin")

@bot.command(name="bruh", hidden=True)
async def bruh(ctx):
    guild: discord.Guild = ctx.guild

    print(guild.members)
    
if __name__ == "__main__":
    for extension in extensions:
        bot.load_extension("cogs." + extension)

    bot.run(TOKEN)


