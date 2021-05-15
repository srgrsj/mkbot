
try:
    import conf 
except ImportError:
    pass

from requests.models import encode_multipart_formdata
import discord
from discord.ext import commands
import img_handler as imhl
import os
import random

intense = discord.Intents.default()
intense.members = True
client = discord.Client(intents=intense)

bot = commands.Bot(command_prefix = "!")

whitelist = {
    822806350886207538: {825309259578474496: "Bots / zhukov_voice"},
}

def allowed_channel():
    async def predicate(ctx:commands.Context):
        if ctx.guild.id in whitelist:
           if ctx.channel.id in whitelist[ctx.guild.id].keys():
               return True
    

        
        return False 
        


    return commands.check(predicate)





@bot.command(name = "repeat")
@allowed_channel()
async def command_hello(ctx, *args):
    message = " ".join(args)
    msg = f'{message}'
    await ctx.channel.send(msg)


@bot.command(name= "mk")
@allowed_channel()
async def mk(ctx, f1:discord.Member=None, f2:discord.Member=None):
    voice_channel = ctx.author.voice.channel

    if f1 and f2:
        await imhl.vs_create(f1.avatar_url, f2.avatar_url)
        await ctx.channel.send(file=discord.File(os.path.join("./img/result.png")))
    elif f1:
        await imhl.vs_create(f1.avatar_url, bot.user.avatar_url)
        await ctx.channel.send(file=discord.File(os.path.join("./img/result.png")))


@bot.command(name="join")
@allowed_channel()
async def vc_join(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        msg = f"Подключаюсь к {voice_channel.name}"
        await ctx.channel.send(msg)
        await voice_channel.connect()


@bot.command(name="leave")
@allowed_channel()
async def vc_leave(ctx):
    msg = ""
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client != None:
        msg = f"Отключаюсь от {voice_channel.name}"
        await ctx.channel.send(msg)
        await ctx.voice_client.disconnect()


@bot.command(name="ost")
@allowed_channel()
async def vs_ost(ctx):
    msg = f"мм-мммм-мортал к-ккк-кк-кккк-к-к-к-к-комбат("
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await ctx.channel.send(msg)
        await voice_client.play(discord.FFmpegPCMAudio(source="./sound/mk.mp3"))



@bot.command(name="fight")
@allowed_channel()
async def fight(ctx:commands.Context):
    f1 = None
    f2 = bot.user
    voice_channel = ctx.author.voice.channel

    if voice_channel:
        await vc_join(ctx)
        voice_members = voice_channel.members
        voice_members = [m for m in voice_members if m.bot == False]

        if len(voice_members) > 1:
            f1, f2 = [voice_members.pop(random.randint(0, len(voice_members))), voice_members.pop(random.randint(0, len(voice_members)))]
        else:
            f1=ctx.author

        
        await imhl.vs_create(f1.avatar_url, f2.avatar_url)
        await ctx.channel.send(file=discord.File(os.path.join("./img/result.png")))


        voice_client = discord.utils.get(bot.voice_clients, guild = ctx.guild) 
        await voice_client.play(discord.FFmpegPCMAudio(source="./sound/mk.mp3"))


    else:
        await ctx.channel.send("зайдите в войс пжпжпж")









bot.run(os.environ["BOT_TOKEN"])

