import discord,os
from simplejson import JSONDecodeError
from numpy import str_
import cricbotlib as cb
from discord.ext import commands

num_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '➡️']
botid = os.environ.get('BOT_ID') #798505180076965891
arrows_emojis=['⬆️', '⬇️', '➡️', '⬅️', '🔄']
ids_con=[]
curr_teams=[]
plids=[]
prctid=0

def string_padder(string):
    return string+('.'*(18-len(string)))

def null_normalizer(arg):
    if arg=='': return '0'
    else: return arg

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
        if len(embed) < 5900:
            embed.add_field(name='{0} Team:{1} Point:{2}'.format(i[0],i[1],i[2]), value='+'+i[3], inline=False)
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



bot=commands.Bot(command_prefix='.')

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
        if 'SFG' == sess_args[0]:
            await message.remove_reaction(str(num_emojis[1]), await bot.fetch_user(botid))
            await message.remove_reaction(str(num_emojis[2]), await bot.fetch_user(botid))
            m_id = ids_con[int(sess_args[1])]
            data=cb.fetch(cb.urlprov(m_id, 1, 'batsman', num_emojis.index(str(reaction)), '', ''))
            f=cb.shotsfig_bt(int(sess_args[4]), data)
            file = discord.File(fp=f, filename='img{}.png'.format(m_id))
            nm = await channel.send(file=file, content='sessionid:SFGL-{0}-{1}-{2}-{3}'.format(sess_args[1],sess_args[2],sess_args[3], sess_args[4]))
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

        if 'SFGL' == sess_args[0]:
            m_id = ids_con[int(sess_args[1])]
            data = cb.fetch(cb.urlprov(m_id, 1, 'batsman', 1, '', ''))
            if str(reaction) == arrows_emojis[2]:
                curr_plindex = int(sess_args[4])+1
            if str(reaction) == arrows_emojis[3]:
                curr_plindex = int(sess_args[4])-1
            if curr_plindex <0:
                curr_plindex=0
            try:
                f=cb.shotsfig_bt(curr_plindex, data)
                file = discord.File(fp=f, filename='img{}.png'.format(m_id))
                content='sessionid:SFGL-{0}-{1}-{2}-{3}'.format(sess_args[1], sess_args[2], sess_args[3], str(curr_plindex))
            except IndexError: pass
            nm=await channel.send(file=file, content=content)
            await message.delete()
            await nm.add_reaction(arrows_emojis[3])
            await nm.add_reaction(arrows_emojis[2])

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
                string += '\nsessionid:PACR-{0}-{1}-{2}-{3}\n```'.format(sess_args[1], sess_args[2], str(curr_plindex), str_(player_type))
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
    await ctx.send(embed=leaderboard_embed(match_format, dtype))

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
    
auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
