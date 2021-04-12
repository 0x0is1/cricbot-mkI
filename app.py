import discord,os
from discord.ext.commands.errors import CommandInvokeError, CommandNotFound
from simplejson import JSONDecodeError
import cricbotlib as cb
from discord.ext import commands

num_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '➡️']
botid = os.environ.get('BOT_ID') #798505180076965891
arrows_emojis=['⬆️', '⬇️', '➡️', '⬅️', '🔄']
ids_con=[]
curr_teams=[]
plids=[]
prctid=0

class command_formats:
    schedule = '`schedule [t20/odi/test]`'
    team = '`team [match number in schedule]`'
    partnership = '`partneship [match number in schedule]`'
    partnership_current = '`pc [match number in schedule]`'
    score = '`score [match number in schedule]`'
    scorecard = '`scorecard [match number in schedule]`'
    playercard = '`playercard [match number in schedule]`'
    player_againstcard = '`againstcard [match number in schedule]`'
    shots = '`shots [match number in schedule]`'
    heatmap = '`heatmap [match number in schedule]`'
    leaderboard = '`leaderboard [t20/odi/test] [bat/bowl/allrounder]`'
    fallofwicket = '`fallofwicket [match number in schedule]`'
    powerplay = '`powerplay [match number in schedule]`'
    lastovers = 'lastovers [match number in schedule]'

def string_padder(string):
    return string+('.'*(18-len(string)))

def null_normalizer(arg):
    if arg=='': return '0'
    else: return arg

#embedders
def invite_embed():
    embed = discord.Embed(title='cricbot Invite',
                          url='https://discord.com/api/oauth2/authorize?client_id=830809161599025202&permissions=10304&scope=bot',
                          description='Invite cricbot on your server.')
    return embed

def source_embed():
    source_code = 'https://github.com/0x0is1/project-redesigned-adventure'
    embed = discord.Embed(title='cricbot Source code',
                          url=source_code,
                          description='Visit cricbot source code.')
    return embed

def help_embed():
    embed = discord.Embed(title="Cricbot-2.0", color=0x03f8fc)
    embed.add_field(
    name="Description:", value="Get real time score and other infos related to cricket on you server instantly.", inline=False)
    embed.add_field(name="Commands:\n", value="_",)
    embed.add_field(name="Schedule:", value=command_formats.score, )
    embed.add_field(name="Score:", value=command_formats.schedule, )
    embed.add_field(name="Scorecard: ", value=command_formats.scorecard, )
    embed.add_field(name="Heatmap(Pitch): ", value=command_formats.heatmap, )
    embed.add_field(name="Shots: ", value=command_formats.shots, )
    embed.add_field(name="Playercard: ", value=command_formats.playercard, )
    embed.add_field(name="Againstcard: ", value=command_formats.player_againstcard, )
    embed.add_field(name="Partnership: ", value=command_formats.partnership, )
    embed.add_field(name="Lastover: ", value=command_formats.lastovers, )
    embed.add_field(name="Team: ", value=command_formats.team, )
    embed.add_field(name="Fallofwicket: ", value=command_formats.fallofwicket, )
    embed.add_field(name="Leaderboard: ", value=command_formats.leaderboard, )
    embed.add_field(name="Powerplay: ", value=command_formats.powerplay, )
    embed.add_field(name="Current partnership: ", value=command_formats.partnership_current, )
    embed.add_field(name="Invite: ", value="`invite`", )
    embed.add_field(name="Source: ", value="`source`", )
    embed.add_field(name="Credits: ", value="`credits`", )
    return embed

def schedule_embed(limit, raw_data):
    schedule = cb.schedule(limit,raw_data)[-5:]
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
        embed.add_field(name='**Score**', value='{0} {1}-{2} ({3})\n{4} {5}-{6} ({7})\n**Status**: ***{8}***'.format(s[7],s[4],s[5],s[6],s0[7],s0[4],s0[5],s0[6], s0[9]), inline=False)
    except Exception: 
        s=cb.miniscore(0, raw_data)
        embed = discord.Embed(title=s[2], color=0x03f8fc)
        embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
        embed.add_field(name='**Score**', value='{0} {1}-{2} ({3})\n**Status**: ***{4}***'.format(s[7],s[4],s[5],s[6], s[9]), inline=False)
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

def leaderboard_embed(mf, dtype, count):
    data=cb.fetch(cb.urlprov('', 2, '', 0, mf, dtype))
    rawlb=cb.leaderboard(data, count)[-10:]
    embed = discord.Embed(title='Leaderboard [{0}] [{1}]'.format(mf,dtype), color=0x03f8fc)
    for i in rawlb:
        embed.add_field(name='{0}. {1} Team: {2} Point: {3}'.format(i[0],i[1],i[2],i[3]), value='+'+i[4], inline=False)
    return embed

def shotsfig_embed_f(raw_data: dict, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    embed.add_field(name='Select the Inning:', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:SFG-{0}-{1}-{2}-{3}`'.format(
        match_index, team_ids[0], team_ids[1], str(1)), inline=True)
    return embed

def heatfig_embed_f(raw_data: dict, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    embed.add_field(name='Select the Inning:', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:HFG-{0}-{1}`'.format(
        match_index, str(0)), inline=True)
    return embed

def fow_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get Fall of wicket details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:FOW-{0}-{1}-{2}`'.format(match_index,team_ids[0],team_ids[1]), inline=True)
    return embed

def fow_embed(raw_data, inning_id):
    f=cb.fow(int(inning_id)-1, raw_data)
    file = discord.File(fp=f, filename='img{}.png'.format(inning_id))
    f.close()
    return file

def powerplay_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get Partnership details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:PSP-{0}-{1}-{2}`'.format(match_index,team_ids[0],team_ids[1]), inline=True)
    return embed

def powerplay_embed(raw_data, inning_id):
    data= cb.powerplay(inning_id, raw_data)
    embed = discord.Embed(title='Powerplays')
    for i in data:
        embed.add_field(name='{0}\nOvers   Run   Wicket'.format(i[0]), value="{:02n}-{:02n}   {:03n}   {:02n}".format(
            int(i[1].split('-')[0]), int(i[1].split('-')[1]), int(i[2]), int(i[3])))
    return embed

def playercard_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    embed.add_field(name='React the team ID to get Players details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:PRC-{0}-{1}-{2}-{3}`'.format(
        match_index, team_ids[0], team_ids[1], str(0)), inline=True)
    return embed

def playercard_embed(raw_data, player_id, team_id):
    data_bt = cb.playercard(team_id, player_id, raw_data, 0)
    data_bl = cb.playercard(team_id, player_id, raw_data, 1)    
    embed = discord.Embed(title='Player Info')
    embed.add_field(name='Name:', value=data_bt[0], inline=True)
    embed.add_field(name='Total Matches:', value=data_bt[1], inline=True)
    embed.add_field(
        name='BATTING', value='+=============++=============+', inline=False)
    for i in range(0, len(data_bt[2])):
        val = data_bt[3][i]
        if val == '':
            val='NaN'
        embed.add_field(name=data_bt[2][i], value=val, inline=True)
    embed.add_field(
        name='BOWLING', value='+=============++=============+', inline=False)
    for i in range(0, len(data_bl[2])):
        val = data_bl[3][i]
        if val == '':
            val = 'NaN'
        embed.add_field(name=data_bl[2][i], value=val, inline=True)
    return embed

def scorecard_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    embed.add_field(name='Select the inning', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:SCR-{0}-{1}-{2}`'.format(
        match_index, team_ids[0], team_ids[1]), inline=True)
    return embed

def scorecard_embed(raw_data, inning_id):
    data_bt = cb.scorecard(inning_id, raw_data)[0]
    data_bl = cb.scorecard(inning_id, raw_data)[1]
    vt = "```css\n.BATTING\n+=============++=============+\n[Name]           [Runs] [Balls] [4s]  [6s]  [D]    [S.R]\n"
    for i in range(0, len(data_bt)):
        k = data_bt[i]
        vt = vt+'{}{:03n}    {:03n}     {:02n}    {:02n}    {:02n}    {}\n'.format(string_padder(k[0]), int(null_normalizer(k[1])), int(null_normalizer(k[2])), int(null_normalizer(k[3])), int(null_normalizer(k[4])), int(null_normalizer(k[5])), float(null_normalizer(k[6])))
    
    vb = "\n.BOWLING\n+=============++=============+\n[Name]           [Runs] [Overs] [M] [W]  [NB] [WD] [D] [E.R]\n"
    for i in range(0, len(data_bl)):
        k = data_bl[i]
        vb += '{}{:03n}   {:4.1f}    {:02n}   {:02n}   {:02n}   {:02n}   {:02n}  {}\n'.format(
            string_padder(k[0]), int(null_normalizer(k[1])), float(null_normalizer(k[2])), int(null_normalizer(k[3])), int(null_normalizer(k[4])), int(null_normalizer(k[5])), int(null_normalizer(k[6])), int(null_normalizer(k[7])), float(null_normalizer(k[8])))
    
    n = vt + vb
    return n

def player_againstcard_embed_f(raw_data, match_index, n):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    if n == 0:
        embed.add_field(name='Select the inning:', value='1. {0}\n2. {1}'.format(
            teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
        embed.add_field(name='_', value='`sessionid:PAC-{0}`'.format(match_index), inline=True)
    else:
        embed.add_field(name='Select player type:', value='1. {0}\n2. {1}'.format('Batsmen', 'Bowlers'), inline=False)
    return embed

def player_againstcard_embed(player_index, raw_data, is_batsman):
    data = cb.player_againstcard(player_index, raw_data, is_batsman)
    heading = '```css\n[PLAYER PERFORMANCE]\n'
    if is_batsman:
        table_indices = '\n[Name]           [Runs] [Balls] [4s]  [6s]  [D]    [S.R]\n'
    else:
        table_indices = '\n[Name]           [Runs] [Balls] [4s]  [6s]  [D]    [E.R]\n'
    nm = '.{} - against:\n'.format(data[0])
    string=''
    for k in data[1]:
        string += '{}{:03n}    {:03n}     {:02n}    {:02n}    {:02n}    {}\n'.format(string_padder(k[0]), int(null_normalizer(k[1])), int(null_normalizer(k[2])), int(null_normalizer(k[3])), int(null_normalizer(k[4])), int(null_normalizer(k[5])), float(null_normalizer(k[6])))
    return heading + nm + table_indices + string

def lastover_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='Select the inning:', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:LO-{0}`'.format(match_index), inline=True)
    return embed

def lastover_embed(raw_data, inning_id):
    data = cb.lastovers(inning_id, raw_data)
    embed = discord.Embed(title='Lastovers', color=0x03f8fc)
    for i in data:
        embed.add_field(name='{0}:'.format(i[0]), value='**Score**: {:02n}\n**Wicket**: {:02n}\n**Run Rate**: {}'.format(int(null_normalizer(i[1])), int(null_normalizer(i[2])), float(null_normalizer(i[3]))), inline=True)
    return embed

def pshipc_embed_f(match_index,raw_data):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='Select the inning:', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.add_field(name='_', value='`sessionid:PPC-{0}`'.format(match_index), inline=True)
    return embed

def pshipc_embed(raw_data, inning_id):
    data = cb.curr_partnership(raw_data, inning_id)
    embed = discord.Embed(title='Current Partnership', color=0x03f8fc)
    embed.add_field(name='For Inning {0}:'.format(data[0]), value='**Runs**: {0}**Balls**: {1}\n**Partners**:\n**{2}:**\n*Runs*: {3}*Balls*: {4}\n**{5}:**\n*Runs*: {6}*Balls*: {7}'.format(
        data[0], data[1], data[2], data[3], data[4],data[5], data[6], data[7] 
    ), inline=True)
    return embed

bot=commands.Bot(command_prefix='.')
bot.remove_command('help')

#events
@bot.event
async def on_ready():
    print('bot is online.')

@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        global ids_con, psid, botid
        message = reaction.message
        channel = message.channel
        msg=await channel.fetch_message(message.id)
        try:
            session_id=str(msg.embeds[0].fields[-1].value).split('sessionid:')[1].split('`')[0]
        except Exception:
            session_id = str(msg.content).split('sessionid:')[1].split('\n')[0]
        except IndexError: pass
        await message.remove_reaction(reaction, user)
        sess_args=session_id.split('-')
        if 'SCD' in sess_args[0]:
            cshtype = int(sess_args[1])
            curr_count = int(sess_args[2])
            if str(reaction) == arrows_emojis[1]:
                curr_count+=5
            if str(reaction) == arrows_emojis[0]:
                curr_count-=5
            if curr_count < 5:
                curr_count=5
            url = 'https://cricket.yahoo.net/sifeeds/multisport/?methodtype=3&client=24&sport=1&league=0&timezone=0530&language=en&gamestate='+str(cshtype)
            e=schedule_embed(curr_count, cb.fetch(url))            
            e.add_field(name='_', value='sessionid:SCD-{0}-{1}'.format(str(cshtype), str(curr_count)))
            await message.edit(embed=e)

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
        if 'SFG' == sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[int(sess_args[1])]
            data=cb.fetch(cb.urlprov(m_id, 1, 'batsman', num_emojis.index(str(reaction)), '', ''))
            f=cb.shotsfig_bt(int(sess_args[4]), data)
            file = discord.File(fp=f[1], filename='img{}.png'.format(m_id))
            content='**Name: **{}'.format(f[0])
            content+='\nsessionid:SFGL-{0}-{1}-{2}-{3}-{4}'.format(sess_args[1],sess_args[2],sess_args[3], sess_args[4],num_emojis.index(str(reaction)))
            nm = await channel.send(file=file, content=content)
            await message.delete()
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'SFGL' == sess_args[0]:
            content=''
            m_id = ids_con[int(sess_args[1])]
            data = cb.fetch(cb.urlprov(m_id, 1, 'batsman', sess_args[5], '', ''))
            if str(reaction) == arrows_emojis[2]:
                curr_plindex = int(sess_args[4])+1
            if str(reaction) == arrows_emojis[3]:
                curr_plindex = int(sess_args[4])-1
            if curr_plindex <0:
                curr_plindex=0
            try:
                f=cb.shotsfig_bt(curr_plindex, data)
                content='**Name: **{}'.format(f[0])
                content+='\nsessionid:SFGL-{0}-{1}-{2}-{3}-{4}'.format(sess_args[1], sess_args[2], sess_args[3], str(curr_plindex), sess_args[4])
                file = discord.File(fp=f[1], filename='img{}.png'.format(m_id))
                nm=await channel.send(file=file, content=content)
            except IndexError: pass
            except JSONDecodeError: 
                nm=await channel.send(content=content)
                content+='\nN/A'
            await message.delete()
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'HFG' == sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[int(sess_args[1])]
            url=cb.urlprov(m_id, 1, 'bowler', num_emojis.index(str(reaction)), '', '')
            data=cb.fetch(url)
            f=cb.shotsfig_bl(int(sess_args[2]), data)
            content='**Name: **{}'.format(f[0])
            content+='\nsessionid:HFGL-{0}-{1}-{2}'.format(sess_args[1],sess_args[2], num_emojis.index(str(reaction)))
            file = discord.File(fp=f[1], filename='img{}.png'.format(m_id))
            nm = await channel.send(file=file, content=content)
            await message.delete()
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'HFGL' == sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            url=cb.urlprov(m_id, 1, 'bowler', 1, '', '')
            data = cb.fetch(url)
            content=''
            if str(reaction) == arrows_emojis[2]:
                curr_plindex = int(sess_args[2])+1
            if str(reaction) == arrows_emojis[3]:
                curr_plindex = int(sess_args[2])-1
            if curr_plindex <0:
                curr_plindex=0
            try:
                f=cb.shotsfig_bl(curr_plindex, data)
                content='**Name: **{}'.format(f[0])            
                content+='\nsessionid:HFGL-{0}-{1}-{2}'.format(sess_args[1], str(curr_plindex), sess_args[3])
                file = discord.File(fp=f[1], filename='img{}.png'.format(m_id))
                if file != None:
                    nm=await channel.send(file=file, content=content)
                else: raise IndexError
            except IndexError: 
                content+='\nN/A'
                nm=await channel.send(content=content)
            await message.delete()
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])
        if 'LB' in sess_args[0]:
            curr_count = int(sess_args[3])
            mf=sess_args[1]
            dtype = sess_args[2]
            if str(reaction) == arrows_emojis[1]:
                curr_count+=10
            if str(reaction) == arrows_emojis[0]:
                curr_count-=10
            if curr_count < 10:
                curr_count = 10
            e=leaderboard_embed(mf, dtype, curr_count)
            e.add_field(name='_', value='sessionid:LB-{}-{}-{}'.format(mf,dtype, curr_count))
            await message.edit(embed=e)

        if 'FOW' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            await channel.send(file=fow_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')), num_emojis.index(str(reaction))))
        if 'PSP' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            e=powerplay_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')), num_emojis.index(str(reaction)))
            e.add_field(name='_', value='`sessionid:PSP-{0}-{1}-{2}`'.format(sess_args[1],sess_args[2],sess_args[3]), inline=True)
            await message.edit(embed=e)
        if 'PRC' == sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            global plids, prctid
            plids.clear()
            m_id = ids_con[int(sess_args[1])]
            data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
            teams = list(data['Teams'])
            team_id = num_emojis.index(str(reaction))
            prctid = team_id
            plids = list(data['Teams'][teams[team_id-1]]['Players'])
            player_id = plids[int(sess_args[4])]
            e = playercard_embed(data, player_id, teams[team_id-1])
            e.add_field(name='_', value='`sessionid:PRCI={0}={1}={2}={3}`'.format(sess_args[1],sess_args[2],sess_args[3], sess_args[4]), inline=True)
            await message.edit(embed=e)
            await message.add_reaction(arrows_emojis[3])
            await message.add_reaction(arrows_emojis[2])
        
        #split pattern changed as spliting and parsing '-' to string to int 
        #results into considering the minus as hyphen;
        # '=' replace here '-' to avoid this bug.
        sess_args=session_id.split('=')
        if 'PRCI' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
            teams = list(data['Teams'])
            team_id = prctid
            if str(reaction) == arrows_emojis[2]:
                curr_plindex = int(sess_args[4])+1
            if str(reaction) == arrows_emojis[3]:
                curr_plindex = int(sess_args[4])-1
            if curr_plindex <0:
                curr_plindex=0
            try:
                player_id = plids[curr_plindex]
                e = playercard_embed(data, player_id, teams[team_id-1])
                e.add_field(name='_', value='`sessionid:PRCI={0}={1}={2}={3}`'.format(sess_args[1], sess_args[2], sess_args[3], str(curr_plindex)), inline=True)
            except IndexError: pass
            await message.edit(embed=e)
        #resetting splition back to normal '-'
        sess_args = session_id.split('-')
        if 'SCR' == sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            url = cb.urlprov(m_id, 0, '', 0, '', '')
            raw_data = cb.fetch(url)
            in_id = num_emojis.index(str(reaction))
            string=scorecard_embed(raw_data, int(in_id)-1)
            string = string + 'sessionid:SCRR-{0}-{1}-{2}-{3}\n```'.format(sess_args[1],sess_args[2],sess_args[3], in_id)
            sent_message=await channel.send(string)
            await sent_message.add_reaction(arrows_emojis[4])

        if 'SCRR' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            url = cb.urlprov(m_id, 0, '', 0, '', '')
            raw_data = cb.fetch(url)
            string=scorecard_embed(raw_data, int(sess_args[4])-1)
            string = string + 'sessionid:SCRR-{0}-{1}-{2}-{3}\n```'.format(sess_args[1],sess_args[2],sess_args[3], sess_args[4])
            await message.edit(content=string)
        if 'PAC' == sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
            e = player_againstcard_embed_f(data, sess_args[1], 1)
            e.add_field(name='_', value='`sessionid:PACF-{0}-{1}-{2}`'.format(sess_args[1], num_emojis.index(str(reaction)), str(0)), inline=True)
            await message.edit(embed=e)
            
        if 'PACF' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            inning_index = int(sess_args[2])
            a = ['batsman', 'bowler']
            b = [True, False]
            player_type = num_emojis.index(str(reaction))-1
            curr_plindex = int(sess_args[3])
            url = cb.urlprov(m_id, 1, a[player_type], inning_index, '', '')
            try:data = cb.fetch(url)
            except JSONDecodeError: string='N/A'
            try:
                string = player_againstcard_embed(curr_plindex, data, b[player_type])
                string += '\nsessionid:PACR-{0}-{1}-{2}-{3}\n```'.format(sess_args[1], sess_args[2], str(curr_plindex), str(player_type))
            except IndexError: pass
            nm=await channel.send(content=string)
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'PACR' in sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            inning_index = int(sess_args[2])
            a = ['batsman', 'bowler']
            b = [True, False]
            player_type = int(sess_args[4])
            curr_plindex = int(sess_args[3])
            url = cb.urlprov(m_id, 1, a[player_type], inning_index, '', '')
            try:data = cb.fetch(url)
            except JSONDecodeError: string='N/A'
    
            if str(reaction) == arrows_emojis[2]:
                curr_plindex = int(sess_args[3])+1
            if str(reaction) == arrows_emojis[3]:
                curr_plindex = int(sess_args[3])-1
            if curr_plindex <0:
                curr_plindex=0
            try:
                string = player_againstcard_embed(curr_plindex, data, b[player_type])
                string += '\nsessionid:PACR-{0}-{1}-{2}-{3}\n```'.format(sess_args[1], sess_args[2], str(curr_plindex), str(player_type))
            except IndexError: pass
            await message.edit(content=string)

        if 'LO' in sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[int(sess_args[1])]
            inning_index = num_emojis.index(str(reaction))
            url = cb.urlprov(m_id, 0, '', inning_index, '', '')
            raw_data = cb.fetch(url)
            e=lastover_embed(raw_data, inning_index-1)
            await message.edit(embed=e)

        if 'PPC' in sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[int(sess_args[1])]
            inning_index = num_emojis.index(str(reaction))
            url = cb.urlprov(m_id, 0, '', inning_index, '', '')
            raw_data = cb.fetch(url)
            e=pshipc_embed(raw_data, inning_index-1)
            await message.edit(embed=e)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('`Unknown command` \n Please use right command to operate. `help` for commands details.')
    if isinstance(error, CommandInvokeError):
        return

#commands
@bot.command(aliases=['sh', 'sd'])
async def schedule(ctx, shtype='live'):
    cshtype = {'ended': 4, 'upcoming': 2, 'live': 1, 'all': 3}[shtype]
    url = 'https://cricket.yahoo.net/sifeeds/multisport/?methodtype=3&client=24&sport=1&league=0&timezone=0530&language=en&gamestate='+str(cshtype)
    e=schedule_embed(5, cb.fetch(url))
    e.add_field(name='_', value='sessionid:SCD-{0}-{1}'.format(str(cshtype), str(5)))
    message=await ctx.send(embed=e)
    await message.add_reaction(arrows_emojis[0])
    await message.add_reaction(arrows_emojis[1])

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
    e=leaderboard_embed(match_format, dtype, 10)
    e.add_field(name='_', value='sessionid:LB-{}-{}-{}'.format(match_format,dtype, str(10)))
    message=await ctx.send(embed=e)
    await message.add_reaction(arrows_emojis[0])
    await message.add_reaction(arrows_emojis[1])

@bot.command(aliases=['prship','ps','pship'])
async def partnership(ctx, match_index: int):
    global ids_con,curr_teams
    m_id = ids_con[match_index]
    raw_data=cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message=await ctx.send(embed=partnership_embed_f(raw_data,match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['shot', 'st', 'sts'])
async def shots(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message = await ctx.send(embed=shotsfig_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['hmp', 'heat', 'pitch'])
async def heatmap(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message = await ctx.send(embed=heatfig_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])


@bot.command(aliases=['fow', 'fall', 'wicketfall'])
async def fallofwicket(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message = await ctx.send(embed=fow_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['pow', 'pp', 'powerp', 'power'])
async def powerplay(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message = await ctx.send(embed=powerplay_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['trumpcard', 'prc', 'player-info'])
async def playercard(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    message = await ctx.send(embed=playercard_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['scr', 'scoreboard', 'sbd'])
async def scorecard(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    message=await ctx.send(embed=scorecard_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['agcard', 'acard', 'ac'])
async def againstcard(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    message=await ctx.send(embed=player_againstcard_embed_f(raw_data, match_index, 0))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['lsover', 'lo'])
async def lastovers(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    message=await ctx.send(embed=lastover_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['pc', 'pshipc', 'pshipcurr'])
async def partnership_current(ctx, match_index: int):
    global ids_con, curr_teams
    m_id = ids_con[match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    print(url)
    raw_data = cb.fetch(url)
    message=await ctx.send(embed=pshipc_embed_f(match_index, raw_data))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['hlp', 'h'])
async def help(ctx):
    await ctx.send(embed=help_embed())

@bot.command(aliases=['inv', 'invit'])
async def invite(ctx):
    await ctx.send(embed=invite_embed())

@bot.command(aliases=['jn'])
async def join(ctx):
    link='https://discord.gg/PyzaTzs2cF'
    await ctx.send('Join cricbot development server for any help or feedback/bug report.'+link)

@bot.command(aliases=['source', 'source-code'])
async def code(ctx):
    await ctx.send(embed=source_embed())

@bot.command(aliases=['credit', 'cred', 'creds'])
async def credits(ctx):
    embed = discord.Embed(title="Cricbot-2.0 : Your own cricket bot", color=0x03f8fc)
    embed.add_field(name='API Disclaim: ', value="I don't own cricbot API. it is owned by Yahoo! cricket. This is an unofficial use of this API which is not public.", inline=False)    
    embed.add_field(name='Developed by:', value='0x0is1', inline=False)
    await ctx.send(embed=embed)



#errors

@schedule.error
async def schedule_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.schedule))

@score.error
async def score_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.score))

@team.error
async def team_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.team))

@leaderboard.error
async def leaderboard_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.leaderboard))

@partnership.error
async def partnership_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.partnership))

@shots.error
async def shots_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.shots))

@heatmap.error
async def heatmap_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.heatmap))

@fallofwicket.error
async def fallofwicket_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.fallofwicket))

@playercard.error
async def playercard_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.playercard))

@scorecard.error
async def scorcecard_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.scorecard))

@againstcard.error
async def againstcard_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.player_againstcard))

@lastovers.error
async def lastovers_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.lastovers))

@partnership_current.error
async def partnership_current_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.partnership_current))

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
