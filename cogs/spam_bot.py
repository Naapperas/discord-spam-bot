from discord.ext import commands
import discord
import time
import random
import os
import psycopg2
from psycopg2 import Error

class Spam_Bot(commands.Cog):
    """
    The name says it all
    """

    emotes = ["kekw", "pepega", "sadge", "peepohappy", "monkaW", "ELIMINAR",
          "pufavo", "pogchamp", "weirdchamp", "homies", "FeelsStrongMan",
          "5head", "bruh", "caragomeu", "ehehe", "mds", "facho", "caos", "zeapogar", 
          "poggies", "angryNPC", "wat", "stop", "cringe", "maskwojak", "monkaHmm", "PepeRage",
          "spitcereal", "stonks", "stinks", "pepefudido", "pain", "ban", "mods", "poogers", "thonk",
          "suicide", "knuckles", "FeelsAmazingMan"]

    spamming_emotes = {}

    spamming_messages = {}

    the_bot = None

    def __init__(self, bot):
        self.the_bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="register_emote", hidden=True)
    async def register_emote(self, ctx, emote_name):
        print("Registering emote")
        await ctx.send("Teste")
        time.sleep(1)
        async for message in ctx.channel.history(limit=2):
            await message.delete()

        DATABASE_URL = os.environ['DATABASE_URL']

        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            print(conn)
            
            cursor = conn.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(conn.get_dsn_parameters(), "\n")
            # Executing a SQL query
            cursor.execute("SELECT version();")
            # Fetch result
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")
            cursor.execute("SELECT current_database();")
            # Fetch result
            record = cursor.fetchone()
            print("Current database - ", record, "\n")
        except (Exception, Error) as error:
            print(error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("PostegreSQL connections closed!")


    @commands.command(name="fuckyou", help="fuck you")
    async def fuck_you(self, ctx):
        print("running: fuckyou")
        await ctx.send("thats why")


    @commands.command(name="yomamasofat", help="lol")
    async def yomamasofat(self, ctx, member: discord.Member=None):
        print("running: yomamasofat")
        await ctx.send("lol, no u" + ((" " + ctx.message.author.mention) if member else ""))


    @commands.command(name="poke", help="Be an annoying prick, poke a member >:)")
    async def poke(self, ctx, member: discord.Member):
        print("running: poke")
    
        the_message = ctx.message

        await ctx.send(member.mention)

        if(the_message):
            await the_message.delete()


    @commands.command(name="spam_message", help="Spams the given message.")
    async def spam_message(self, ctx, *args):
        print("running:spam_message")

        spam_amount = -1
        spam_message = " ".join(args)

        try:
            spam_amount = int(args[-1])
            spam_message = " ".join(args[:len(args) - 1])
        except:
            print("No amount given, default to '-1'")

        the_guild = ctx.guild

        if(the_guild):
            if(the_guild not in self.spamming_messages or not self.spamming_messages[the_guild]):
                self.spamming_messages[the_guild] = True
            else:
                if(self.pamming_messages[the_guild]):
                    await ctx.send(f"***Already spamming message {ctx.author.mention}!***")
                    return

        if(len(spam_message) <= 0):
            await ctx.send("You must provide a message to spam")

        await ctx.message.delete()

        if(the_guild):
            if(spam_amount < 0):
                while self.spamming_messages[the_guild]:
                    await ctx.send(spam_message)
            else:
                for _ in range(spam_amount):
                    await ctx.send(spam_message)
                self.spamming_messages[the_guild] = False


    @commands.command(name="spam_emote", help="Spams emotes continuously (or a specified number of times) or one particular emote specified by the user")
    async def spam_emote(self, ctx, emote_name: str = "no emote", num_times: int = -1):
        print("running: spam_emote")
        the_message: discord.Message = ctx.message

        if(the_message):
            await the_message.delete()

        the_guild = ctx.guild

        if(the_guild):
            if(the_guild not in self.spamming_emotes or not self.spamming_emotes[the_guild]):
                self.spamming_emotes[the_guild] = True
            else:
                if(self.spamming_emotes[the_guild]):
                    await ctx.send(f"***Already spamming emotes {ctx.author.mention}!***")
                    return

        if(num_times <= -1):
            while self.spamming_emotes[the_guild]:
                emote = emote_name
                if(emote_name == "no emote"):
                    emote = random.choice(self.emotes)
                else:
                    pass

                emoji = discord.utils.get(self.the_bot.emojis, name=emote)
                await ctx.send(str(emoji) if emoji else f"No emote with name {emote} found")
        else:
            for _ in range(num_times):
                emote = emote_name
                if(emote_name == "no emote"):
                    emote = random.choice(self.emotes)
                else:
                    pass

                emoji = discord.utils.get(self.the_bot.emojis, name=emote)
                await ctx.send(str(emoji) if emoji is not None else f"No emote with name {emote} found")
            self.spamming_emotes[the_guild] = False


    async def stop(self, ctx, the_guild, spam_type):
        if(spam_type == "emote"):
            if(the_guild not in self.spamming_emotes or not self.spamming_emotes[the_guild]):
                await ctx.send("What are you trying to stop, you dumbf*uck?")
            else:
                if(self.spamming_emotes[the_guild]):
                    await ctx.send("Stoping emote spam playback")
                    self.spamming_emotes[the_guild] = False
        elif(spam_type == "spam"):
            if(the_guild not in self.spamming_messages or not self.spamming_messages[the_guild]):
                await ctx.send("What are you trying to stop, you dumbf*uck?")
            else:
                if(self.spamming_messages[the_guild]):
                    await ctx.send("Stoping message spam")
                    self.spamming_messages[the_guild] = False


def setup(bot):
    bot.add_cog(Spam_Bot(bot))


                