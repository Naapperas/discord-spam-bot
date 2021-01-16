from discord.ext import commands

class Exams(commands.Cog):
    """ WORK IN PROGRESS """

    the_bot = None

    def __init__(self, bot):
        self.the_bot = bot




def setup(bot):
    bot.add_cog(Exams(bot))