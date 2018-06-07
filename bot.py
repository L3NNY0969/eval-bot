import discord
import os
import io
import traceback
import sys
import time
import datetime
import asyncio
import random
import aiohttp
import pip
import random
import textwrap
from contextlib import redirect_stdout
from discord.ext import commands
import json
bot = commands.Bot(command_prefix=commands.when_mentioned_or('-'), owner_id=411683912729755649)
bot.remove_command("help")


def cleanup_code(content):
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')


@bot.event
async def on_ready():
    print('Bot is online, and ready to ROLL!')
    await bot.change_presence(game=discord.Game(name="with L3NNY's Dank Hangout."))
    
    
@bot.command()
async def help(ctx):
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Commands')
    em.description = "I am a bot for evaluating python code."
    em.add_field(name='eval', value='Runs Python code. Great for testing. Also the main purpose of this bot.')
    em.add_field(name='ping', value='Returns my websocket latency.')
    await ctx.send(embed=em)
    
    
@bot.command()
async def ping(ctx):
    """Returns bot latency"""
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Pong! Latency:')
    em.description = f"{bot.latency * 1000:.4f} ms"
    await ctx.send(embed=em)
    
    
@bot.command(name='eval')
async def _eval(ctx, *, body: str):
    if "bot.ws.token" in body or "os.environ.get('TOKEN')" in body or 'os.environ.get("TOKEN")' in body:
        return await ctx.send("No token for you.")
    lol = bot.get_channel(454048592974577664)
    await lol.send(f"**{ctx.message.author.name}** has run the code: \n\n```{body}```")        
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')
