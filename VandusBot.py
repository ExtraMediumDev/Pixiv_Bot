import sys
import discord
import time
import pixivapi
import pathlib
import os
import shutil
from discord.ext import commands
from pixivapi import *

loading = False

#something that i apparently have to set to True idk?
intents = discord.Intents.default()
intents.members = True

#bot object thingy idk how objects and classes work shut up
bot = commands.Bot(command_prefix='//',intents=intents)
prefix = '//'

#initiating Pixiv client object whatever
client = pixivapi.Client()
client.login('user_akuy5453', 'uslw121405')

#tells me the bot is ready when it is ready
@bot.event
async def on_ready():
    print("Bot is online!")

#when a reaction is added to a message, nothing happens
@bot.event
async def on_reaction_add(reaction, user):
    pass

#path for image folder
p = pathlib.Path('search')

#remembers the searches for each user so that you can use the //next command
searching = {}
 

#when a message is sent, runs the code below
@bot.event
async def on_message(message):
    global loading
    content = message.content
    username = message.author.name
    author_mention = '<@{}>'.format(message.author.id)
    user_id = message.author.id
    guild_id = message.guild.id
    snd = message.channel

    #if a user mentions the bot, it tells the user the prefix
    if content == '<@!798937352499101717>': await message.channel.send('> Prefix is `//`')
    




    if content.startswith(prefix):
        raw_content = content.split(prefix)
        check_command = 0
        deleting = False
    
        command = raw_content[1]
        words = command.split(' ')
        search_term = ''
        i = 0
        for word in words:
            if i > 0: search_term = search_term + word + ' '
            i += 1
        search_term = search_term[:-1]

        #if the search command is used, it will send the result(s).
        if words[0] == 'search':
            check_command = 1
            if loading == False:
                loading = True
                try:
                    name = os.listdir('search')
                    if len(name) > 0: shutil.rmtree('search')


                    results = client.search_illustrations(search_term, offset = 0)
                    searching[user_id] = (0, search_term)
                    image_obj = results['illustrations']

                    await message.delete()
                    loading_msg = await snd.send('```loading...```')

                    image_obj[0].download(p, filename = 'search_results')
                    name = os.listdir('search')
                    multi = False
                    if name[0] == 'search_results': multi = True
                    if multi == True:
                        name = os.listdir('search\search_results')
                        for i in range(len(name)):
                
                            f = discord.File('search\search_results\{}'.format(name[i]))
                            await snd.send(file = f)
                            if i == 0: await loading_msg.delete()

                        shutil.rmtree('search\search_results')
                    else:
                        name = os.listdir('search')[0]


                        f = discord.File('search\{}'.format(name))
                        await snd.send(file = f)
                        await loading_msg.delete()
                        os.remove('search\{}'.format(name))
                except Exception as e:
                    try: await loading_msg.delete()
                    except: pass
                    await message.channel.send('> ❌ No results found.')
                loading = False
            else:
                await message.channel.send('> ❌ No request spamming! Or at least wait until the current process is finished')

        #if the user uses the //next command it will send the next pagae of results
        if command == 'next':
            check_command = 1
            if user_id in searching:
                if loading == False:
                    loading = True
                    try:
                        name = os.listdir('search')
                        if len(name) > 0: shutil.rmtree('search')
                        a,b = searching[user_id]
                        searching[user_id] = a + 1 , b
                        results = client.search_illustrations(b, offset = a + 1)
                        image_obj = results['illustrations']

                        await message.delete()
                        loading_msg = await snd.send('```loading...```')

                        image_obj[0].download(p, filename = 'search_results')
                        name = os.listdir('search')
                        multi = False
                        if name[0] == 'search_results': multi = True
                        if multi == True:
                            name = os.listdir('search\search_results')
                            for i in range(len(name)):
                    
                                f = discord.File('search\search_results\{}'.format(name[i]))
                                await snd.send(file = f)
                                if i == 0: await loading_msg.delete()

                            shutil.rmtree('search\search_results')
                        else:
                            name = os.listdir('search')[0]


                            f = discord.File('search\{}'.format(name))
                            await snd.send(file = f)
                            await loading_msg.delete()
                            os.remove('search\{}'.format(name))
                    except:
                        try: await loading_msg.delete()
                        except: pass
                        await message.channel.send('> ❌ No results found (or something else happened).')
                    loading = False
                else:
                    await message.channel.send('> ❌ No request spamming! Or at least wait until the current process is finished')
            else:
                await message.delete()
                await message.channel.send('> ❌ You currently have no ongoing searches.')
        
        #sends a cool embed of a help message
        if command == 'help':
            check_command = 1

            embedVar = discord.Embed(title="List of Commands (more coming soon!)", description="If you beg me and peer pressure me they will come sooner", color=0x00ff00)
            embedVar.add_field(name="//search xxx", value="xxx can be anything just don't try to search nsfw", inline=False)
            embedVar.add_field(name="//next", value="If you already used //search command, you can use this to send the next page of results.", inline=False)

            f = discord.File('Yoy!.png', filename = 'Yoy!.png')
            embedVar.set_thumbnail(url = 'attachment://Yoy!.png')
            await message.channel.send(embed=embedVar, file = f)

        #replies with owo
        if command == 'uwu':
            check_command = 1

            await message.delete()
            await message.channel.send('owo')

        #if the command is invalid it sends error message
        if check_command == 0:
            if deleting == False: await message.delete()
            await message.channel.send('> ❌ You ({}) have typed in an invalid command. Get good.'.format(author_mention))

    
    
#runs the bot
bot.run('TOKEN_HERE')
