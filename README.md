# Cricbot - yahoo! cricket info provider discord bot

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
* Heatmap
![preview-1](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180028.png)
* Fantasy Insight
![preview-2](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_175941.png)
* Boundries
![preview-3](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180045.png)
* Fall of wickets
![preview-4](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180100.png)
* Schedule
![preview-5](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180117.png)
* Partnership
![preview-6](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180133.png)
* Score
![preview-7](https://raw.githubusercontent.com/0x0is1/inproject-asset-container/master/20210713_180152.png)

