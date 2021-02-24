import discord
import cricbotlib,os
from discord.ext import commands

ids_con=[]


def schedule_embed(limit, raw_data):
    schedule = cricbotlib.schedule(limit,raw_data)
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

def score_embed(raw_data):
    try: 
        s0=cricbotlib.miniscore(0,raw_data)
        s=cricbotlib.miniscore(1,raw_data)
        embed = discord.Embed(title=s[2], color=0x03f8fc)
        embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
        embed.add_field(name='**Score**', value='{0} {1}-{2} ({3})\n{4} {5}-{6} ({7})'.format(s[7],s[4],s[5],s[6],s0[7],s0[4],s0[5],s0[6]), inline=False)
    except Exception: 
        s=cricbotlib.miniscore(0, raw_data)
        embed = discord.Embed(title=s[2], color=0x03f8fc)
        embed.add_field(name='{0} vs {1}'.format(s[7], s[8]), value='**Date**: {0}  **Time**:{1}\n**Venue**: {2}'.format(s[0],s[1],s[3]), inline=False)
        embed.add_field(name='**Score**', value='{0} {1}-{2} ({3})'.format(s[7],s[4],s[5],s[6]), inline=False)
    return embed

bot=commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('bot is running.')
@bot.command()
async def shedule(ctx, count=5, shtype='live'):
    cshtype = {'ended': 4, 'upcoming': 2, 'live': 1, 'all': 3}[shtype]
    url = 'https://cricket.yahoo.net/sifeeds/multisport/?methodtype=3&client=24&sport=1&league=0&timezone=0530&language=en&gamestate='+str(cshtype)
    await ctx.send(embed=schedule_embed(count, cricbotlib.fetch(url)))

@bot.command()
async def score(ctx, match_index: int):
    global ids_con
    m_id = ids_con[match_index]
    await ctx.send(embed=score_embed(cricbotlib.fetch(cricbotlib.urlprov(m_id,0,'',0,'',''))))

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
