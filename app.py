import discord,os
from discord.ext.commands.errors import CommandInvokeError, CommandNotFound
from simplejson.errors import JSONDecodeError
import cricbotlib as cb
from discord.ext import commands, tasks

num_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
botid = os.environ.get('BOT_ID') #798505180076965891
arrows_emojis=['⬆️', '⬇️', '➡️', '⬅️', '🔄']
ids_con={}
curr_teams=[]
plids=[]
prctid=0
refresh_time=7

class command_formats:
    schedule = '`schedule [live/upcoming/ended]`'
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
    lastovers = '`lastovers [match number in schedule]`'
    fantasy_insight = '`fi [match number in schedule]`'
    
def string_padder(string):
    return string+('.'*(14-len(string)))

def string_padder2(string):
    return string+('　'*(3-int(len(string)/2)))

def null_normalizer(arg):
    if arg=='': return '0'
    else: return arg

#embedders
def invite_embed():
    embed = discord.Embed(title='cricbot Invite',
                          url='https://discord.com/api/oauth2/authorize?client_id=830809161599025202&permissions=10304&scope=bot',
                          description='Invite cricbot on your server.', color=0x03f8fc)
    return embed

def source_embed():
    source_code = 'https://github.com/0x0is1/project-redesigned-adventure'
    embed = discord.Embed(title='cricbot Source code',
                          url=source_code,
                          description='Visit cricbot source code.', color=0x03f8fc)
    return embed

def help_embed():
    embed = discord.Embed(title="Cricbot-2.0", color=0x03f8fc)
    embed.add_field(
    name="Description:", value="Get real time score and other infos related to cricket on you server instantly.", inline=False)
    embed.add_field(name="Commands:\n", value="_",inline=False)
    embed.add_field(name="Schedule:", value=command_formats.schedule, inline=False)
    embed.add_field(name="Score:", value=command_formats.score, inline=False)
    embed.add_field(name="Scorecard: ", value=command_formats.scorecard, inline=False)
    embed.add_field(name="Heatmap(Pitch): ", value=command_formats.heatmap, inline=False)
    embed.add_field(name="Shots: ", value=command_formats.shots, inline=False)
    embed.add_field(name="Playercard: ", value=command_formats.playercard, inline=False)
    embed.add_field(name="Againstcard: ", value=command_formats.player_againstcard, inline=False)
    embed.add_field(name="Partnership: ", value=command_formats.partnership, inline=False)
    embed.add_field(name="Lastover: ", value=command_formats.lastovers, inline=False)
    embed.add_field(name="Team: ", value=command_formats.team, inline=False)
    embed.add_field(name="Fallofwicket: ", value=command_formats.fallofwicket, inline=False)
    embed.add_field(name="Leaderboard: ", value=command_formats.leaderboard, inline=False)
    embed.add_field(name="Powerplay: ", value=command_formats.powerplay, inline=False)
    embed.add_field(name="Current partnership: ", value=command_formats.partnership_current, inline=False)
    embed.add_field(name="Fantasy Insight: ", value=command_formats.fantasy_insight, inline=False)
    embed.add_field(name="Invite: ", value="`invite`")
    embed.add_field(name="Source: ", value="`source`")
    embed.add_field(name="Credits: ", value="`credits`")
    embed.add_field(name="Join: ", value="Join development server `join`", )
    return embed

def schedule_embed(limit, raw_data, channel_id):
    schedule = cb.schedule(limit,raw_data)[-5:]
    embed = discord.Embed(title='Schedule', color=0x03f8fc)
    global ids_con
    a=[]
    a.append('tadped01312021199821')
    for i in range(limit):
        try:
            k=schedule[i]
        except (IndexError,KeyError):
            break
        embed.add_field(name='{0}. {1}'.format(str(i+1),k[4]), value='{0} vs {1}\n**Date**: {5} | **Time**: {2}  |  **Venue**: {3}\n*{4}*'.format(
            k[0], k[1], k[5], k[8], k[6], k[7]), inline=False)
        a.append(k[9])
    ids_con[channel_id] = a
    return embed

def score_embed(raw_data, match_index):
    score_string=''
    i=0
    while True:
        try:
            s=cb.miniscore(i,raw_data)
            score_string += '{0} {1}-{2} ({3})\n'.format(s[7],s[4],s[5],s[6])
            i+=1
        except Exception:
            break
    score_string+='**Status**: ***{0}***\n'.format(s[9])
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='**Score**', value=score_string, inline=False)
    embed.set_footer(text='sessionid:MSC-{0}'.format(match_index))
    return embed


def partnership_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get partnership details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.set_footer(text='sessionid:PEF-{0}-{1}-{2}'.format(match_index,team_ids[0],team_ids[1]))
    return embed

def partnership_embed(raw_data, inning_id):
    embed= discord.Embed(title='Partnership', color=0x03f8fc)
    f=cb.partnership(int(inning_id)-1, raw_data)
    file = discord.File(fp=f, filename='img{}.png'.format(inning_id))
    f.close()
    embed.set_image(url='attachment://img{}.png'.format(inning_id))
    return embed, file

def team_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.set_footer(text='sessionid:TEF-{0}-{1}-{2}'.format(match_index,team_ids[0],team_ids[1]))
    return embed
def team_embed(raw_data,team_id):
    team_name = raw_data['Teams'][team_id]['Name_Full']
    embed = discord.Embed(title='Team', color=0x03f8fc)
    team_data=cb.team_pl(team_id, raw_data)
    string=''
    for i in team_data:
       string+='**'+str(i[0])+str(i[1])+str(i[2])+'**\n'
    embed.add_field(name=team_name, value=string, inline=False)
    return embed

def leaderboard_embed(mf, dtype, count):
    data=cb.fetch(cb.urlprov('', 2, '', 0, mf, dtype))
    rawlb=cb.leaderboard(data, count)[-10:]
    embed = discord.Embed(title='Leaderboard [{0}] [{1}]'.format(mf,dtype), color=0x03f8fc)
    for i in rawlb:
        embed.add_field(name='{0}. {1} Team: {2} Point: {3}'.format(i[0],i[1],i[2],i[3]), value='+'+i[4], inline=False)
    return embed

def shotsfig_embed_f(raw_data: dict):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    embed.add_field(name='Select the Inning:', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    return embed

def shotsfig_embed(curr_plindex, data):
    f=cb.shotsfig_bt(curr_plindex, data)
    embed = discord.Embed(title='Shots playerwise', color=0x03f8fc)
    file = discord.File(fp=f[1], filename='img{}.png'.format(curr_plindex))
    embed.add_field(name='Name:', value=f[0], inline=False)
    embed.set_image(url='attachment://img{}.png'.format(curr_plindex))
    return embed, file

def heatfig_embed_f(raw_data: dict, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    embed.add_field(name='Select the Inning:', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.set_footer(text='sessionid:HFG-{0}-{1}'.format(
        match_index, str(0)))
    return embed

def fow_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get Fall of wicket details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.set_footer(text='sessionid:FOW-{0}-{1}-{2}'.format(match_index,team_ids[0],team_ids[1]))
    return embed

def fow_embed(raw_data, inning_id):
    embed = discord.Embed(title='Fall of wicket')
    f=cb.fow(int(inning_id)-1, raw_data)
    file = discord.File(fp=f, filename='img{}.png'.format(inning_id))
    embed.set_image(url='attachment://img{}.png'.format(inning_id))
    return embed, file

def powerplay_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='React the team no. to get Partnership details', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.set_footer(text='sessionid:PSP-{0}-{1}-{2}'.format(match_index,team_ids[0],team_ids[1]))
    return embed

def powerplay_embed(raw_data, inning_id):
    data= cb.powerplay(inning_id, raw_data)
    embed = discord.Embed(title='Powerplays', color=0x03f8fc)
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
    embed.set_footer(text='sessionid:PRC-{0}-{1}-{2}-{3}'.format(
        match_index, team_ids[0], team_ids[1], str(0)))
    return embed

def playercard_embed(raw_data, player_id, team_id):
    data_bt = cb.playercard(team_id, player_id, raw_data, 0)
    data_bl = cb.playercard(team_id, player_id, raw_data, 1)    
    embed = discord.Embed(title='Player Info', color=0x03f8fc)
    embed.add_field(name='Name:', value=data_bt[0], inline=True)
    embed.add_field(name='Total Matches:', value=data_bt[1], inline=True)
    embed.add_field(
        name='BATTING', value='+=============+', inline=False)
    for i in range(0, len(data_bt[2])):
        val = data_bt[3][i]
        if val == '':
            val='NaN'
        embed.add_field(name=data_bt[2][i], value=val, inline=True)
    embed.add_field(
        name='BOWLING', value='+=============+', inline=False)
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
    embed.set_footer(text='sessionid:SCR-{0}'.format(match_index))
    return embed

def scorecard_embed(raw_data, inning_id):
    data=cb.scorecard(inning_id, raw_data)
    data_bt = data[0]
    data_bl = data[1]
    vt = "```css\n[Name]       [Runs] [Balls] [4s]  [6s]  [D]    [S.R]\n"
    for i in range(0, len(data_bt)):
        k = data_bt[i]
        vt = vt+'{}{:03n}    {:03n}     {:02n}    {:02n}    {:02n}    {}\n'.format(string_padder(k[0]), int(null_normalizer(k[1])), int(null_normalizer(k[2])), int(null_normalizer(k[3])), int(null_normalizer(k[4])), int(null_normalizer(k[5])), float(null_normalizer(k[6])))
    vt+='\n```'
    vb = '```css\n[Name]       [Runs] [Overs] [M] [W]  [NB] [WD] [D] [E.R]\n'
    for i in range(0, len(data_bl)):
        k = data_bl[i]
        vb += '{}{:03n}   {:4.1f}    {:02n}   {:02n}   {:02n}   {:02n}   {:02n}  {}\n'.format(
            string_padder(k[0]), int(null_normalizer(k[1])), float(null_normalizer(k[2])), int(null_normalizer(k[3])), int(null_normalizer(k[4])), int(null_normalizer(k[5])), int(null_normalizer(k[6])), int(null_normalizer(k[7])), float(null_normalizer(k[8])))
    vb+='\n```'
    embed= discord.Embed(title='Scorecard {0} vs {1}'.format(data[2], data[3]), color=0x03f8fc)
    embed.add_field(name='BATTING [{}]'.format(data[2]), value=vt, inline=False)
    embed.add_field(name='BOWLING [{}]'.format(data[3]), value=vb, inline=False)
    return embed

def player_againstcard_embed_f(raw_data, n):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(
        s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0], s[1], s[3]), inline=False)
    if n == 0:
        embed.add_field(name='Select the inning:', value='1. {0}\n2. {1}'.format(
            teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    else:
        embed.add_field(name='Select player type:', value='1. {0}\n2. {1}'.format('Batsmen', 'Bowlers'), inline=False)
    return embed

def player_againstcard_embed(player_index, raw_data, is_batsman):
    embed = discord.Embed(title='PLAYER PERFORMANCE', color=0x03f8fc)
    data = cb.player_againstcard(player_index, raw_data, is_batsman)
    heading = '```css\n'
    if is_batsman:
        table_indices = '\n[Name]       [Runs] [Balls] [4s]  [6s]  [D]    [S.R]\n'
    else:
        table_indices = '\n[Name]       [Runs] [Balls] [4s]  [6s]  [D]    [E.R]\n'
    nm = '{} performance against:\n'.format(data[0])
    string=''
    for k in data[1]:
        string += '{}{:03n}    {:03n}     {:02n}    {:02n}    {:02n}    {}\n'.format(string_padder(k[0]), int(null_normalizer(k[1])), int(null_normalizer(k[2])), int(null_normalizer(k[3])), int(null_normalizer(k[4])), int(null_normalizer(k[5])), float(null_normalizer(k[6])))
    string+='\n```'
    embed.add_field(name=nm, value=heading+table_indices+ string)
    return embed

def lastover_embed_f(raw_data, match_index):
    s = cb.miniscore(0, raw_data)
    teams = raw_data['Teams']
    team_ids = list(teams)
    embed = discord.Embed(title=s[2], color=0x03f8fc)
    embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
    embed.add_field(name='Select the inning:', value='1. {0}\n2. {1}'.format(
        teams[team_ids[0]]['Name_Full'], teams[team_ids[1]]['Name_Full']), inline=False)
    embed.set_footer(text='sessionid:LO-{0}'.format(match_index))
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
    embed.set_footer(text='sessionid:PPC-{0}'.format(match_index), inline=True)
    return embed

def pshipc_embed(raw_data, inning_id):
    data = cb.curr_partnership(raw_data, inning_id)
    embed = discord.Embed(title='Current Partnership', color=0x03f8fc)
    embed.add_field(name='For Inning {0}:'.format(data[0]), value='**Runs**: {0} **Balls**: {1}\n**Partners**:\n**{2}:**\n*Runs*: {3} *Balls*: {4}\n**{5}:**\n*Runs*: {6} *Balls*: {7}'.format(
        data[0], data[1], data[2], data[3], data[4],data[5], data[6], data[7] 
    ), inline=True)
    return embed

def fantasy_insight_embed(raw_data, fantasy_type):
    fe = {'d11':'Dream11', 'my11':'MyTeam11'}
    embed = discord.Embed(title='Team Prediction: {0}'.format(fe[fantasy_type]), color=0x03f8fc)
    data= cb.fantasy_insight(raw_data, fantasy_type)
    file = discord.File(fp=data, filename='img{}.png'.format(fantasy_type))
    embed.set_image(url='attachment://img{}.png'.format(fantasy_type))
    return file, embed

def state_selector():
    embed= discord.Embed(title='Election May 2021', color=0x03f8fc)
    embed.add_field(name='React to Select State:', value='1. Assam\n2. Kerala\n3. Pudducherry\n4. Tamil Nadu\n5. West Bengal', inline=False)
    embed.set_footer(text='sessionid:ESEL')
    return embed

def election_embed(state_index):
    string=''
    states=['Assam', 'Kerala', 'Pudducherry', 'Tamil Nadu', 'West Bengal']
    embed = discord.Embed(title='{0} Election Result May 2021'.format(states[state_index-1]), color=0x03f8fc)
    data = cb.election_result(state_index)
    for i in data:
        string+='{}{:03n}　　{:03n}　　{:03n}\n'.format(string_padder2(i[0]), int(i[1]), int(i[2]), int(i[3]))
    embed.add_field(name='Party     Won     Leading     Total', value=string, inline=False)
    embed.set_footer(text='sessionid:ELREF-{0}'.format(state_index))
    return embed

bot=commands.Bot(command_prefix='.')
bot.remove_command('help')

@tasks.loop(seconds=refresh_time)
async def status_changer():
    cshtype = 1
    url = 'https://cricket.yahoo.net/sifeeds/multisport/?methodtype=3&client=24&sport=1&league=0&timezone=0530&language=en&gamestate='+str(cshtype)
    sh = cb.schedule(40, cb.fetch(url))
    t,preid = '', ''
    for i in sh:
        if 'ICC World Test Championship Final' in i[4]:
            preid = i[9]
            break
    if preid == '':
        preid = sh[0][9]
    url = 'https://cricket.yahoo.net/sifeeds/cricket/live/json/' + preid + '.json'
    data = cb.fetch(url)
    c=0
    while True:
        try: 
            s=cb.miniscore(c,data)
            c+=1
        except IndexError:break
        except KeyError: 
            s=''
            break
    try:
        score = '{0}-{1} ({2})'.format(s[4], s[5], s[6])
        t = '{0} vs {1}'.format(s[7], s[8])
        string = '{0} | {1}'.format(t, score)
    except IndexError: string = ''
    await bot.change_presence(activity=discord.Game(name=string))

#events
@bot.event
async def on_ready():
    status_changer.start()
    print('bot is online.')

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if not user.bot and message.author == bot.user:
        global ids_con, botid
        channel = message.channel
        channel_id = channel.id
        msg=await channel.fetch_message(message.id)
        try:
            session_id=str(msg.embeds[0].footer.text).split('sessionid:')[1].split('`')[0]
            await message.remove_reaction(reaction, user)
        except IndexError:pass
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
            e=schedule_embed(curr_count, cb.fetch(url), channel_id)            
            e.set_footer(text='sessionid:SCD-{0}-{1}'.format(str(cshtype), str(curr_count)))
            await message.edit(embed=e)

        if 'TEF' in sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            e=team_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')),sess_args[num_emojis.index(str(reaction))+1])
            e.set_footer(text='sessionid:TEF-{0}-{1}-{2}'.format(sess_args[1],sess_args[2],sess_args[3]))
            await message.edit(embed=e)
        if 'PEF' in sess_args[0]:
            inning_index=num_emojis.index(str(reaction))
            m_id = ids_con[channel_id][int(sess_args[1])]
            url=cb.urlprov(m_id, 0, '', 0, '', '')
            d=partnership_embed(cb.fetch(url), inning_index)
            await channel.send(embed=d[0], file=d[1])
        
        if 'MSC' in sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            await message.edit(embed=score_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')), sess_args[1]))
        if 'SFG' == sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            inning_id=num_emojis.index(str(reaction))
            url=cb.urlprov(m_id, 1, 'batsman', inning_id, '', '')
            curr_plindex=int(sess_args[2])
            data=cb.fetch(url)
            file = shotsfig_embed(curr_plindex, data)
            content='sessionid:SFGL-{0}-{1}-{2}'.format(sess_args[1],(str(curr_plindex)),inning_id)
            embed = file[0]
            embed.set_footer(text=content)
            await message.delete()
            nm = await channel.send(embed=embed, file=file[1])
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'SFGL' == sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            inning_id = int(sess_args[3])
            curr_plindex= int(sess_args[2])
            url=cb.urlprov(m_id, 1, 'batsman', inning_id, '', '')
            data = cb.fetch(url)
            if str(reaction) == arrows_emojis[2]:
                curr_plindex += 1
            if str(reaction) == arrows_emojis[3]:
                curr_plindex -= 1
            if curr_plindex <0:
                curr_plindex=0
            content='sessionid:SFGL-{0}-{1}-{2}'.format(sess_args[1],str(curr_plindex), str(inning_id))
            try:
                f = shotsfig_embed(curr_plindex, data)
                embed = f[0]
                embed.set_footer(text=content)
                nm=await channel.send(file=f[1], embed=embed)
            except (IndexError,UnboundLocalError,JSONDecodeError): pass
            await message.delete()
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'HFG' == sess_args[0]:
            embed = discord.Embed(title='Heatmap', color=0x03f8fc)
            m_id = ids_con[channel_id][int(sess_args[1])]
            url=cb.urlprov(m_id, 1, 'bowler', num_emojis.index(str(reaction)), '', '')
            data=cb.fetch(url)
            f=cb.shotsfig_bl(int(sess_args[2]), data)
            file = discord.File(fp=f[1], filename='img{}.png'.format(m_id))
            embed.add_field(name='Name:', value=f[0], inline=False)
            embed.set_image(url='attachment://img{}.png'.format(m_id))
            embed.set_footer(text='sessionid:HFGL-{0}-{1}-{2}'.format(
                sess_args[1],sess_args[2], num_emojis.index(str(reaction))))
            nm = await channel.send(file=file, embed=embed)
            await message.delete()
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'HFGL' == sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
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
                embed = discord.Embed(title='Heatmap', color=0x03f8fc)
                f=cb.shotsfig_bl(curr_plindex, data)
                file = discord.File(fp=f[1], filename='img{}.png'.format(m_id))
                embed.add_field(name='Name:', value=f[0], inline=False)
                embed.set_image(url='attachment://img{}.png'.format(m_id))
                embed.set_footer(text='sessionid:HFGL-{0}-{1}-{2}'.format(
                    sess_args[1], str(curr_plindex), sess_args[3]))
                if file != None:
                    nm=await channel.send(file=file, embed=embed)
                else: raise IndexError
            except IndexError:pass
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
            e.set_footer(text='sessionid:LB-{}-{}-{}'.format(mf,dtype, curr_count))
            await message.edit(embed=e)

        if 'FOW' in sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            f=fow_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')), num_emojis.index(str(reaction)))
            await channel.send(file=f[1], embed=f[0])

        if 'PSP' in sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            e=powerplay_embed(cb.fetch(cb.urlprov(m_id, 0, '', 0, '', '')), num_emojis.index(str(reaction)))
            e.set_footer(text='sessionid:PSP-{0}-{1}-{2}'.format(sess_args[1],sess_args[2],sess_args[3]))
            await message.edit(embed=e)
        if 'PRC' == sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            global plids, prctid
            plids.clear()
            m_id = ids_con[channel_id][int(sess_args[1])]
            data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
            teams = list(data['Teams'])
            team_id = num_emojis.index(str(reaction))
            prctid = team_id
            plids = list(data['Teams'][teams[team_id-1]]['Players'])
            player_id = plids[int(sess_args[4])]
            e = playercard_embed(data, player_id, teams[team_id-1])
            e.set_footer(text='sessionid:PRCI={0}={1}={2}={3}'.format(
                sess_args[1],sess_args[2],sess_args[3], sess_args[4]))
            await message.edit(embed=e)
            await message.add_reaction(arrows_emojis[3])
            await message.add_reaction(arrows_emojis[2])
        
        #split pattern changed as spliting and parsing '-' to string to int 
        #results into considering the minus as hyphen;
        # '=' replace here '-' to avoid this bug.
        sess_args=session_id.split('=')
        if 'PRCI' in sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
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
                e.set_footer(text='sessionid:PRCI={0}={1}={2}={3}'.format(
                    sess_args[1], sess_args[2], sess_args[3], str(curr_plindex)))
            except IndexError: pass
            await message.edit(embed=e)
        #resetting splition back to normal '-'
        sess_args = session_id.split('-')
        if 'SCR' == sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[channel_id][int(sess_args[1])]
            url = cb.urlprov(m_id, 0, '', 0, '', '')
            raw_data = cb.fetch(url)
            try:
                in_id = num_emojis.index(str(reaction))
            except ValueError:
                in_id = sess_args[2]
            sessid='sessionid:SCR-{0}-{1}'.format(sess_args[1], in_id)
            embed=scorecard_embed(raw_data, int(in_id)-1)
            embed.set_footer(text=sessid)
            await message.edit(embed=embed)
            await message.add_reaction(arrows_emojis[4])

        if 'PAC' == sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
            e = player_againstcard_embed_f(data, 1)
            e.set_footer(text='sessionid:PACF-{0}-{1}-{2}'.format(sess_args[1], num_emojis.index(str(reaction)), str(0)))
            await message.edit(embed=e)
            
        if 'PACF' in sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            inning_index = int(sess_args[2])
            a = ['batsman', 'bowler']
            b = [True, False]
            player_type = num_emojis.index(str(reaction))-1
            curr_plindex = int(sess_args[3])
            url = cb.urlprov(m_id, 1, a[player_type], inning_index, '', '')
            try:data = cb.fetch(url)
            except JSONDecodeError: pass
            try:
                embed = player_againstcard_embed(curr_plindex, data, b[player_type])
                embed.set_footer(text='sessionid:PACR-{0}-{1}-{2}-{3}'.format(
                    sess_args[1], sess_args[2], str(curr_plindex), str(player_type)))
            except IndexError: pass
            nm=await channel.send(embed=embed)
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'PACR' in sess_args[0]:
            m_id = ids_con[channel_id][int(sess_args[1])]
            inning_index = int(sess_args[2])
            a = ['batsman', 'bowler']
            b = [True, False]
            player_type = int(sess_args[4])
            curr_plindex = int(sess_args[3])
            url = cb.urlprov(m_id, 1, a[player_type], inning_index, '', '')
            try:data = cb.fetch(url)
            except JSONDecodeError: pass
    
            if str(reaction) == arrows_emojis[2]:
                curr_plindex = int(sess_args[3])+1
            if str(reaction) == arrows_emojis[3]:
                curr_plindex = int(sess_args[3])-1
            if curr_plindex <0:
                curr_plindex=0
            try:
                embed = player_againstcard_embed(curr_plindex, data, b[player_type])
                embed.set_footer(text='sessionid:PACR-{0}-{1}-{2}-{3}'.format(sess_args[1], sess_args[2], str(curr_plindex), str(player_type)))
            except IndexError: pass
            await message.edit(embed=embed)

        if 'LO' in sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[channel_id][int(sess_args[1])]
            inning_index = num_emojis.index(str(reaction))
            url = cb.urlprov(m_id, 0, '', inning_index, '', '')
            raw_data = cb.fetch(url)
            e=lastover_embed(raw_data, inning_index-1)
            await message.edit(embed=e)

        if 'PPC' in sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[channel_id][int(sess_args[1])]
            inning_index = num_emojis.index(str(reaction))
            url = cb.urlprov(m_id, 0, '', inning_index, '', '')
            raw_data = cb.fetch(url)
            e=pshipc_embed(raw_data, inning_index-1)
            await message.edit(embed=e)

        if 'FI' in sess_args[0]:
            d={1:'d11', 2:'my11'}
            m_id = ids_con[channel_id][int(sess_args[1])]
            ftype = d[num_emojis.index(str(reaction))]
            url='https://cricket.yahoo.net/sifeeds/cricket/live/json/{}_fantasy_picks.json'.format(m_id)
            data= cb.fetch(url)
            c=fantasy_insight_embed(data, ftype)
            embed=c[1]
            embed.set_footer(text='sessionid:FI-{0}-{1}'.format(str(sess_args[1]), ftype))
            await message.delete()
            msg=await channel.send(file=c[0], embed=embed)
            await msg.add_reaction(num_emojis[1])
            await msg.add_reaction(num_emojis[2])
    
        if 'ESEL' in sess_args[0]:
            await message.edit(embed=election_embed(num_emojis.index(str(reaction))))
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[3]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[4]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[5]), await bot.fetch_user(botid))
            await message.add_reaction(arrows_emojis[4])

        if 'ELREF' in sess_args[0]:
            await message.edit(embed=election_embed(int(sess_args[1])))
            
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('`Unknown command` \n Please use right command to operate. `help` for commands details.')
    if isinstance(error, CommandInvokeError):
        return

#commands
@bot.command(aliases=['sh', 'sd'])
async def schedule(ctx, shtype='live'):
    channel_id = ctx.message.channel.id
    cshtype = {'ended': 4, 'upcoming': 2, 'live': 1, 'all': 3}[shtype]
    url = 'https://cricket.yahoo.net/sifeeds/multisport/?methodtype=3&client=24&sport=1&league=0&timezone=0530&language=en&gamestate='+str(cshtype)
    e=schedule_embed(5, cb.fetch(url), channel_id)
    e.set_footer(text='sessionid:SCD-{0}-{1}'.format(str(cshtype), str(5)))
    message=await ctx.send(embed=e)
    await message.add_reaction(arrows_emojis[0])
    await message.add_reaction(arrows_emojis[1])

@bot.command(aliases=['sc', 'ms', 'miniscore'])
async def score(ctx, match_index: int):
    channel_id = ctx.message.channel.id
    global ids_con
    m_id = ids_con[channel_id][match_index]
    msg=await ctx.send(embed=score_embed(cb.fetch(cb.urlprov(m_id,0,'',0,'','')), match_index))
    await msg.add_reaction('🔄')

@bot.command(aliases=['tm'])
async def team(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con,curr_teams
    m_id = ids_con[channel_id][match_index]
    raw_data=cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message=await ctx.send(embed=team_embed_f(raw_data,match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['lb', 'ldb'])
async def leaderboard(ctx, match_format='odi', dtype='bat'):
    e=leaderboard_embed(match_format, dtype, 10)
    e.set_footer(text='sessionid:LB-{}-{}-{}'.format(match_format,dtype, str(10)))
    message=await ctx.send(embed=e)
    await message.add_reaction(arrows_emojis[0])
    await message.add_reaction(arrows_emojis[1])

@bot.command(aliases=['prship','ps','pship'])
async def partnership(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con,curr_teams
    m_id = ids_con[channel_id][match_index]
    raw_data=cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message=await ctx.send(embed=partnership_embed_f(raw_data,match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['shot', 'st', 'sts'])
async def shots(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    e=shotsfig_embed_f(raw_data)
    e.set_footer(text='sessionid:SFG-{0}-{1}'.format(match_index, str(1)))
    message = await ctx.send(embed=e)
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['hmp', 'heat', 'pitch'])
async def heatmap(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message = await ctx.send(embed=heatfig_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])


@bot.command(aliases=['fow', 'fall', 'wicketfall'])
async def fallofwicket(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message = await ctx.send(embed=fow_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['pow', 'pp', 'powerp', 'power'])
async def powerplay(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    raw_data = cb.fetch(cb.urlprov(m_id, 0, '', 0, '', ''))
    message = await ctx.send(embed=powerplay_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['trumpcard', 'prc', 'player-info'])
async def playercard(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    message = await ctx.send(embed=playercard_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['scr', 'scoreboard', 'sbd'])
async def scorecard(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    message=await ctx.send(embed=scorecard_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['agcard', 'acard', 'ac'])
async def againstcard(ctx, match_index: int):
    channel_id = ctx.message.channel.id    
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    e=player_againstcard_embed_f(raw_data, 0)
    e.set_footer(text='sessionid:PAC-{0}'.format(match_index))
    message=await ctx.send(embed=e)
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['lsover', 'lo'])
async def lastovers(ctx, match_index: int):
    channel_id = ctx.message.channel.id
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
    raw_data = cb.fetch(url)
    message=await ctx.send(embed=lastover_embed_f(raw_data, match_index))
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])

@bot.command(aliases=['pc', 'pshipc', 'pshipcurr'])
async def partnership_current(ctx, match_index: int):
    channel_id = ctx.message.channel.id
    global ids_con, curr_teams
    m_id = ids_con[channel_id][match_index]
    url = cb.urlprov(m_id, 0, '', 0, '', '')
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

@bot.command(aliases=['fantasy', 'insight', 'fi', 'finsight', 'dream11'])
async def fantasy_insight(ctx, match_index: int):
    channel_id = ctx.message.channel.id
    global ids_con
    m_id = ids_con[channel_id][match_index]
    url='https://cricket.yahoo.net/sifeeds/cricket/live/json/{}_fantasy_picks.json'.format(m_id)
    raw_data = cb.fetch(url)
    c=fantasy_insight_embed(raw_data, 'd11')
    embed=c[1]
    embed.set_footer(text='sessionid:FI-{0}-{1}'.format(str(match_index), 'd11'))
    message=await ctx.message.channel.send(file=c[0], embed=embed)
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])


@bot.command()
async def election(ctx):
    message=await ctx.send(embed=state_selector())
    await message.add_reaction(num_emojis[1])
    await message.add_reaction(num_emojis[2])
    await message.add_reaction(num_emojis[3])
    await message.add_reaction(num_emojis[4])
    await message.add_reaction(num_emojis[5])

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

@fantasy_insight.error
async def fantasy_insight_error(ctx, error):
    print(error)
    await ctx.send('Invalid command! use {}'.format(command_formats.fantasy_insight))

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
