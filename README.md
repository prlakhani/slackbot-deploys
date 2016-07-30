# slackbot-deploys
Gentle edits from [github.com/brandonshin/slackbot-workout](https://github.com/brandonshin/slackbot-workout)


# Instructions

1. Clone the repo and navigate into the directory in your terminal.

    `$ git clone git@github.com:prlakhani/slackbot-deploys.git`

2. Go to your slack home page [https://{yourgroup}.slack.com/home](http://my.slack.com/home) & click on **Integrations** on the left sidebar.

    <img src = "https://ctrlla-blog.s3.amazonaws.com/2015/Jun/Screen_Shot_2015_06_05_at_7_21_33_PM-1433557303531.png" width = 300>

3. Scroll all the way down until you see **Slack API** and **Slackbot**. You'll need to access these two integrations.

    <img src="https://ctrlla-blog.s3.amazonaws.com/2015/Jun/Screen_Shot_2015_06_05_at_7_19_44_PM-1433557206307.png" width = 500>

4. In the **Slack API Page**, select **WebAPI** in the left side bar, scroll all the way down, and register yourself an auth token. You should see this. Take note of the token, e.g. `xoxp-2751727432-4028172038-5281317294-3c46b1`. This is your **User Auth Token**

    <img src="https://ctrlla-blog.s3.amazonaws.com/2015/Jun/Screen_Shot_2015_06_05_at_7_00_24_PM-1433557433415.png" width = 500>

5. In the **Slackbot** (Remote control page). Register an integration & you should see this. __Make sure you grab just the token out of the url__, e.g. `AizJbQ24l38ai4DlQD9yFELb`

    <img src="https://ctrlla-blog.s3.amazonaws.com/2015/Jun/Screen_Shot_2015_06_03_at_8_44_00_AM-1433557565175.png" width = 500>

6. Save your SLACK_USER_TOKEN_STRING and SLACK_URL_TOKEN_STRING as environmental variables in your terminal.

    `$ export SLACK_USER_TOKEN_STRING=YOURUSERTOKEN`
    
    `$ export SLACK_URL_TOKEN_STRING=YOURURLTOKEN`
    
    If you need help with this, try adapting the first 5 steps of the guide to [edit your .bash_profile](http://natelandau.com/my-mac-osx-bash_profile/)
    
7. Set up channel and customize configurations

    Open `default.json` and set `teamDomain` (ex: ctrlla) `channelName` (ex: general) and `channelId` (ex: B22D35YMS). Save the file as `config.json` in the same directory. Set any other configurations as you like.

    If you don't know the channel Id, fetch it using

    `$ python fetchChannelId.py channelname`

8. To run locally: if you haven't set up pip for python, go to your terminal and run.
`$ sudo easy_install pip`

9. While in the project directory, run

    `$ sudo pip install -r requirements.txt`

    `$ python slackbot-deploy.py`

Currently, this works using Heroku's scheduler (remember to set up the necessary environment variables), but this can sometimes be unreliable.

TODO: replace above with clock process, [as suggested by Heroku](https://devcenter.heroku.com/articles/clock-processes-python)

TODO: move `allowedToDeploy` config variable into environment variable
