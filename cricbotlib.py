import requests
import base64
import io
import matplotlib.pyplot as mp
import numpy as np
from PIL import Image, ImageDraw
from math import cos, sin, radians


def urlprov(ids: str, urlindex: int, ptype: str, inning_index: int, mformat: str, dtype: str):
    base_url = 'https://cricket.yahoo.net/sifeeds/cricket/live/json/'
    url = {
        0: base_url + ids + '.json',
        1: base_url + ids + '_' + ptype + '_splits_'+str(inning_index)+'.json',
        2: 'https://cricket.yahoo.net/sifeeds/cricket/static/json/iccranking-' + mformat+'-'+dtype+'.json',
    }[urlindex]
    return url

def fetch(url):
    return requests.get(url).json()

def schedule(limit: int, raw_data: dict):
    data = {}
    team_names: str = lambda item_type, match_index, inning_id: raw_data[
        'matches'][match_index]['participants'][inning_id][item_type]
    event_fetch: str = lambda match_index, item_type: raw_data['matches'][match_index][item_type]
    for i in range(limit):
        try:team_names('name', i, 0)
        except(IndexError,KeyError):break
        data[i] = (
            team_names('name', i, 0),
            team_names('name', i, 1),
            team_names('id', i, 0),
            team_names('id', i, 1),
            event_fetch(i, 'series_name'),
            event_fetch(i, 'start_date').split('+')[1],
            event_fetch(i, 'event_sub_status'),
            event_fetch(i, 'start_date'),
            event_fetch(i, 'venue_name'),
            event_fetch(i, 'game_id')
        )
    return data

def miniscore(inning_id: int, data: dict):
    inning = data['Innings'][inning_id]
    teams = data['Teams']
    md = data['Matchdetail']
    return (
        md['Match']['Date'],
        md['Match']['Offset'].replace('+', ''),
        md['Series']['Series_short_display_name'],
        md['Venue']['Name'],
        inning['Total'],
        inning['Wickets'],
        inning['Overs'],
        teams[inning['Battingteam']]['Name_Short'],
        teams[inning['Bowlingteam']]['Name_Short'],
    )

def fetch_team(team_id: str):
    return requests.get('https://cricket.yahoo.net/sifeeds/cricket/static/json/' + str(team_id) + '_team.json').json()


def playercard(team_id: str, player_id: str, raw_data: dict):
    player = raw_data['Teams'][team_id]['Players'][player_id]
    bt = player['Batting']
    bl = player['Bowling']
    return player['Name_Full'], player['Matches'],\
        (bt['Style'], bt['Average'], bt['Strikerate'], bt['Runs']),\
        (bl['Style'], bl['Average'], bl['Economyrate'], bl['Wickets'])


def scorecard(inning_id: int, data: dict):
    btsb,blsb = [],[]
    inning = data['Innings'][inning_id]
    batsmen = inning['Batsmen']
    bowler = inning['Bowlers']
    btteam_id = inning['Battingteam']
    blteam_id = inning['Bowlingteam']
    btplayer = data['Teams'][btteam_id]['Players']
    blplayer = data['Teams'][blteam_id]['Players']
    for i in batsmen:
        btsb.append(
            (
                btplayer[i['Batsman']]['Name_Full'],
                     i['Runs'], i['Balls'], i['Fours'],
                     i['Sixes'], i['Dots'], i['Strikerate'], i['Howout']
            )
        )
    for i in bowler:
        blsb.append(
            (
                blplayer[i['Bowler']]['Name_Full'],
                     i['Overs'], i['Maidens'], i['Wickets'],
                     i['Economyrate'], i['Noballs'], i['Wides'], i['Dots']))
    return btsb, blsb


def team_pl(team_id: str, raw_data: dict):
    players = raw_data['Teams'][team_id]['Players']
    pls = []
    for i in players:
        if players[str(i)]['Confirm_XI']:
            p = ' *(playing)*'
        try:
            players[str(i)]['Iscaptain']
            c = ' *(captain)*'
        except KeyError:
            c = ''
        try:
            players[str(i)]['Iskeeper']
            k = ' *(keeper)*'
        except KeyError:
            k = ''
        pls.append((players[str(i)]['Name_Full'], p, c, k))
    return pls


def fow(inning_id: int, raw_data: dict):
    sc = raw_data['Innings'][inning_id]
    fw = sc['FallofWickets']
    team_id = sc['Battingteam']
    team_name = raw_data['Teams'][team_id]['Name_Full']
    score = str(sc['Total'])+'/'+str(sc['Wickets'])+' '+str(sc['Overs'])
    o, s = [], []
    for i in fw:
        o.append(float(i['Overs']))
        s.append(int(i['Score']))
    mp.xticks(np.arange(0, int(o[len(o)-1]+100), step=1))
    mp.yticks(np.arange(0, int(s[len(s)-1]+100), step=10))
    mp.title('Fall of wicket: '+team_name+' ('+score+')', fontsize=14)
    mp.xlabel('Overs', fontsize=14)
    mp.ylabel('Runs', fontsize=14)
    mp.plot(o, s, color='red', marker='o', linewidth=3,
            markerfacecolor='red', markersize=8)
    for i in range(len(o)):
        mp.annotate('('+str(s[i])+'-'+str(o[i])+')', (o[i]+0.1, s[i]-2))
    s.append(int(sc['Total']))
    o.append(float(sc['Overs']))
    mp.plot(o, s, color='blue')
    fig = mp.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    return string


def powerplay(inning_id: int, raw_data: dict):
    pp = raw_data['Innings'][inning_id]['PowerPlayDetails']
    a = []
    for i in pp:
        a.append((i['Name'], i['Overs'], i['Runs'], i['Wickets']))
    return a


def lastovers(inning_id: int, raw_data: dict):
    lsov = raw_data['Innings'][inning_id]['LastOvers']
    a = []
    for i in lsov:
        a.append((i, lsov[i]['Score'], lsov[i]['Wicket'], lsov[i]['Runrate']))
    return a


def partnership(inning_id: int, raw_data: dict):
    sc = raw_data['Innings'][inning_id]
    x, runs, balls = [], [], []
    team_id = sc['Battingteam']
    plr = raw_data['Teams'][team_id]['Players']
    psp = sc['Partnerships']
    team_name = raw_data['Teams'][team_id]['Name_Full']
    score = str(sc['Total'])+'/'+str(sc['Wickets'])+' '+str(sc['Overs'])
    for i in psp:
        b =lambda a:plr[i['Batsmen'][a]['Batsman']]['Name_Full'].split(' ')[-1]
        x.append(b(0)+'\n'+b(1))
        runs.append(int(i['Runs']))
        balls.append(int(i['Balls']))
    x_pos = [i for i, _ in enumerate(x)]
    mp.bar(x_pos, runs, color='blue', width=0.7)
    mp.xlabel("Partners")
    mp.ylabel("Runs")
    mp.title("Partnerships: "+team_name+' '+str(score))
    mp.xticks(x_pos, x, fontsize=7)
    r=sorted(runs)
    mp.yticks(np.arange(0, int(r[len(runs)-1])+10, step=15))
    for i in range(len(runs)):
        mp.annotate(str(runs[i])+' in '+ str(balls[i]), (x_pos[i]-0.3, runs[i]+1), fontsize=8)
    fig = mp.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf


def player_againstcard(player_id: str, raw_data: dict, pltype: int):
    if pltype == 1:
        c = 'Strikerate'
        d = 'Batsmen'
        e = 'Bowler'
        f = 'Batsman'
    else:
        c = 'Economyrate'
        d = 'Bowlers'
        e = 'Batsman'
        f = 'Bowler'
    pl = raw_data[d][player_id]
    ag = pl['Against']
    a = []
    for i in ag:
        k = ag[i]
        a.append((k[e], k['Runs'], k['Balls'],
                  k['Fours'], k['Sixes'], k['Dots'], k[c]))
        return pl[f], a


def get_color(index: str):
    return {'1': 'orange', '2': 'purple', '3': 'pink',
            '4': 'green', '6': 'blue'}[index]


def shotsfig(player_id: str, raw_data: dict):
    shots = raw_data['Batsmen'][player_id]['Shots']
    BATS_POS = (496, 470)
    UNIT_DIS = 110
    distance=lambda k: int(k['Distance'])*UNIT_DIS
    im = Image.open("./field.jpg")
    d = ImageDraw.Draw(im)
    for i in shots:
        X = (distance(i)*cos(radians(int(i['Angle'])+90)))+BATS_POS[0]
        Y = (distance(i)*sin(radians(int(i['Angle'])+90)))+BATS_POS[1]
        d.line([(X, Y), BATS_POS], fill=get_color(i['Runs']), width=4)
        d.text((X, Y), i['Runs'], fill='black')
    buf = io.BytesIO()
    im.save(buf, format='jpeg')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    return string


def leaderboard(raw_data: dict):
    a = []
    r = raw_data['bat-rank']['rank']
    for i in r:
        a.append((i['Player-name'], i['Country'],
                  i['Points'], i['careerbest']))
    return a

#print(shotsfig('3852', fetch('inen02132021199340', 2)))

#print(fow(0, fetch('tadped01312021199821', 1)))

#print(playercard('1989', '4476', fetch('tadped01312021199821', 1)))

#print(scorecard(1, fetch('pedbet02012021199824', 1))[0])

#print(urlprov('tadped01312021199821', 2))
#f=open('schedule.json', 'r')
#shotsfig('7861', json.load(f))

#print(leaderboard(fetch(urlprov('', 2, '', 0, 't20', 'bowl'))))
