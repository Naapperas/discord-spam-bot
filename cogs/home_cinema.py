from discord.ext import commands
from os import listdir
from os.path import isfile, join
import time

scripts_path = "../movie_scripts"

movie_scripts = [f for f in listdir(scripts_path) if isfile(join(scripts_path, f))]

scripts = {} # a dictionary holding the script beng played back in every guild

scripts_running = {} # dictionary holding every guild 'registered' for script playback

class HomeCinema(commands.Cog, name="HomeCinema"):

    the_bot = None

    def __init__(self, bot):
        self.the_bot = bot
        
    @the_bot.command(name='read_movie', help="Starts writing the movie script, line by line")
    async def read_movie(self, ctx, movie_name: str):
        print("running: read_movie")
        the_guild = ctx.guild

        if(the_guild): # check if guild has been passed in the context
            if(the_guild not in scripts_running or not scripts_running[the_guild]): # if we are not 'registeres' for potential playback of scripts or aren't playing anything, mark us as so 
                scripts_running[the_guild] = True
            else:
                if(scripts_running[the_guild]): # already 'registered', check if we are playing anything 
                    await ctx.send(f"***Already writing movie script {ctx.author.mention}!***")
                    return

        print("Not currently writing movie in guild, attempting to do so!")

        if(movie_name == ""):
            await ctx.send("You need to provide a movie to display!!")
            scripts_running[the_guild] = False
            return

        movie = (movie_name + ".txt")

        if(movie not in movie_scripts):
            await ctx.send("You need to provide an existing movie to display!!")
            scripts_running[the_guild] = False
            return

        print("Valid movie name given")

        await ctx.message.delete()

        movie_file = open(scripts_path + movie, "r")

        script = []

        num_lines_read = 0
        for line in movie_file:
            num_lines_read += 1
            script.append(line)

        print("Read", num_lines_read, "lines")

        print("Finished reading movie file!")

        if(the_guild):
            if(the_guild not in scripts):
                scripts[the_guild] = script

        print("Putting movie in scripts dict, beginning to write lines")

        if(len(script) > 0):
            if(the_guild):
                for line in scripts[the_guild]:
                    if(len(line) > 0):
                        await ctx.send(line)
                        time.sleep(1)
        else:
            print("No movie read!!!!")
                
        print("Finnished writing movie!")
                
        scripts_running[the_guild] = False

    @the_bot.command(name="speak_movie", help="NOT WORKING-Joins a voice channel and starts reading the given movie")
    async def speak_movie(self, ctx, movie_name: str):
        print("running: speak_movie")
        if(True):
            await ctx.send("NOT CURRENTLY WORKING")
            return

        the_guild = ctx.guild

        if(the_guild):
            if(the_guild not in scripts_running.keys):
                scripts_running[the_guild] = True
            else:
                if(scripts_running[the_guild]):
                    await ctx.send(f"***Already writing movie script {ctx.author.mention}!***")
                    return

        if(movie_name == ""):
            await ctx.send("You need to provide a movie to speak!!")
            return

        connected = ctx.author.voice

        if not connected:
            await ctx.send("You need to be connected in a voice channel to use this command!")
            return

        vc = await connected.channel.connect()

        movie = (movie_name + ".txt")

        if(movie not in movie_scripts):
            await ctx.send("You need to provide an existing movie to speak!!")
            return

        await ctx.message.delete()

        movie_file = open("movie_scripts/" + movie, "r")

        script = []

        for line in movie_file:
            script.append(line)

        for line in script:
            await ctx.send(line)
            time.sleep(1)

        await vc.disconnect()


            