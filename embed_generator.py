import discord,os
import cricbotlib as cb
from discord.ext import commands

num_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

ids_con=[]
curr_teams=[]

#embedders
def schedule_embed(limit, raw_data):
    schedule = cb.schedule(limit,raw_data)
    embed = discord.Embed(title='Schedule', color=0x03f8fc)
    global ids_con
    ids_con.clear()
    ids_con.append('tadped01312021199821')
    for i in range(limit):
        try:
            k=schedule[i]
        except (IndexError,KeyError):
            break
        embed.add_field(name='{0}. {1}'.format(str(i+1),k[4]), value='{0} vs {1}\n**Date**: {2}  |  **Venue**: {3}\n*{4}*'.format(
            k[0], k[1], k[5], k[8], k[6]), inline=False)
        ids_con.append(k[9])
    return embed

def score_embed(raw_data, match_index):
    try: 
        s0=cb.miniscore(0,raw_data)
        s=cb.miniscore(1,raw_data)
        embed = discord.Embed(title=s[2], color=0x03f8fc)
        embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
        embed.add_field(name='**Score**', value='{0} {1}-{2} ({3})\n{4} {5}-{6} ({7})'.format(s[7],s[4],s[5],s[6],s0[7],s0[4],s0[5],s0[6]), inline=False)
    except Exception: 
        s=cb.miniscore(0, raw_data)
        embed = discord.Embed(title=s[2], color=0x03f8fc)
        embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
        embed.add_field(name='**Score**', value='{0} {1}-{2} ({3})'.format(s[7],s[4],s[5],s[6]), inline=False)
    embed.add_field(name='_', value='`sessionid:MSC-{0}`'.format(match_index), inline=True)
    return embed

def team_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:TEF-{0}-{1}-{2}`'.format(match_index,team_ids[0],team_ids[1]), inline=True)
    return embed

def partnership_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get partnership details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:PEF-{0}-{1}-{2}`'.format(match_index,team_ids[0],team_ids[1]), inline=True)
    return embed

def partnership_embed(raw_data, inning_id):
    f=cb.partnership(int(inning_id)-1, raw_data)
    file = discord.File(fp=f, filename='img{}.png'.format(inning_id))
    f.close()
    return file

def team_embed(raw_data,team_id):
    team_name = raw_data['Teams'][team_id]['Name_Full']
    embed = discord.Embed(title=team_name, color=0x03f8fc)
    team_data=cb.team_pl(team_id, raw_data)
    for i in team_data:
       embed.add_field(name=i[0], value=i[1]+i[2]+i[3], inline=False)
    return embed

def leaderboard_embed(mf,dtype):
    rawlb=cb.leaderboard(cb.fetch(cb.urlprov('', 2, '', 0, mf, dtype)))
    embed = discord.Embed(title='Leaderboard {0} {1}'.format(mf,dtype), color=0x03f8fc)
    embed.add_field(name='-',value='(Name) (Team Name) (Points) (Against)',inline=False)
    for i in rawlb:
        embed.add_field(name='{0} Team:{1} Point:{2}'.format(i[0],i[1],i[2]), value='+'+i[3], inline=False)
    return embed

bot=commands.Bot(command_prefix='.')

#events
@bot.event
async def on_ready():
    print('bot is running.')

@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        global ids_con
        message = reaction.message
        channel = message.channel
        msg=await channel.fetch_message(message.id)
        session_id=str(msg.embeds[0].fields[-1].value).split('sessionid:')[1].split('`')[0]
        await message.remove_reaction(reaction, user)
        sess_args=session_id.split('-')
        if 'TEF' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            e=team_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')),sess_args[num_emojis.index(str(reaction))+1])
            e.add_field(name='_', value='`sessionid:TEF-{0}-{1}-{2}`'.format(sess_args[1],sess_args[2],sess_args[3]), inline=True)
            await message.edit(embed=e)
        if 'PEF' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            await channel.send(file=partnership_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')), num_emojis.index(str(reaction))))
        if 'MSC' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            await message.edit(embed=score_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')), sess_args[1]))


#commands
@bot.command(aliases=['sh', 'sd'])
async def schedule(ctx, count=5, shtype='live'):
    cshtype = {'ended': 4, 'upcoming': 2, 'live': 1, 'all': 3}[shtype]
    url = 'https://cricket.yahoo.net/sifeeds/multisport/?methodtype=3&client=24&sport=1&league=0&timezone=0530&language=en&gamestate='+str(cshtype)
    await ctx.send(embed=schedule_embed(count, cb.fetch(url)))

@bot.command(aliases=['sc', 'ms', 'miniscore'])
async def score(ctx, match_index: int):
    global ids_con
    m_id = ids_con[match_index]
    msg=await ctx.send(embed=score_embed(cb.fetch(cb.urlprov(m_id,0,'',0,'','')), match_index))
    await msg.add_reaction('🔄')

@bot.command(aliases=['tm'])
async def team(ctx, match_index: int):
    global ids_con,curr_teams
    m_id = ids_con[match_index]
    raw_data=cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message=await ctx.send(embed=team_embed_f(raw_data,match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['lb', 'ldb'])
async def leaderboard(ctx, match_format='odi', dtype='bat'):
    await ctx.send(embed=partnership_embed_f(match_format, dtype))

@bot.command(aliases=['prship','ps','pship'])
async def partnership(ctx, match_index: int):
    global ids_con,curr_teams
    m_id = ids_con[match_index]
    raw_data=cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message=await ctx.send(embed=partnership_embed_f(raw_data,match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])


auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
