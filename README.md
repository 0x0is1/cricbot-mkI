# Cricbot - yahoo! cricket info provider discord bot
### *ATTENTION! We are closing this project due to API shut down by Yahoo! cricket. Please wait for next version of cricbot [(cricbot-mkII)](https://github.com/0x0is1/cricbot-mkII).*
![image](https://user-images.githubusercontent.com/42772562/131855545-1579a7bf-560c-40ae-b2ed-6a3a0f7b40ae.png)

## Description
Cricbot is a discord bot made with [Cricbot API](https://github.com/0x0is1/cricbot-api) developed by [0x0is1](https://github.com/0x0is1) to provide all live data from yahoo! Cricket directly to your discord server.

## Install
You can [invite](https://discord.com/oauth2/authorize?client_id=830809161599025202&permissions=10304&scope=bot) link to call this bot your discord server.

## Host
You can also host this bot by using following processes:

* Download this repository directly or by using git cli i.e-

```css
> git clone https://github.com/0x0is1/cricbot
> cd cricbot
> python3 -m pip install requirements.txt
> export EXPERIMENTAL_BOT_TOKEN='<Your bot token here>'
> python3 app.py
```
* Or you can host it on heroku, the Procfile is already provided.

## Requirements
* Python3.5+
* python-requests (requests)
* discord.py (discord)
* numpy-python
* pillow-python (PIL)

## Compatibilty _(for hosting this bot particularly)_

Any device that can run Python3.5+ including raspberry pi and other OS'es.

## Commands arguments
* `schedule`: [live/upcoming/ended]
* `team`: [match number in schedule]
* `partneship`: [match number in schedule]
* `partnership current`: [match number in schedule]
* `score`: [match number in schedule]
* `scorecard`: [match number in schedule]
* `playercard`: [match number in schedule]
* `againstcard` [match number in schedule]
* `shots`: [match number in schedule]
* `heatmap`: [match number in schedule]
* `leaderboard`: [t20/odi/test] [bat/bowl/allrounder]
* `fall of wicket`: [match number in schedule]
* `powerplay`: [match number in schedule]
* `lastovers`: [match number in schedule]
* `fantasy insight`: [match number in schedule]
    
## Feedback and bug report

Send feedback or bug report to our developers on this [mail id](0x0is1@protonmail.com).

## Previews
* Heatmap <br>
<img src="https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180028.png" width=30% height=30%> </img>
* Fantasy Insight<br>
<img src="https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_175941.png" width=30% height=30%> </img>
* Boundries <br>
<img src="https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180045.png" width=30% height=30%> </img>
* Schedule<br>
<img src="https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180100.png" width=30% height=30%> </img>
* Fall of wickets<br>
<img src="https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180117.png" width=30% height=30%> </img>
* Partnership<br>
<img src="https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180133.png" width=30% height=30%> </img>
* Score<br>
<img src="https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180152.png" width=30% height=30%> </img>

