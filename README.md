emojibot
=============
A Slack bot based on [rtmbot](https://github.com/slackhq/python-rtmbot) that suggests images for custom emoji.


Installation
-----------

1. Clone the repo

        git clone git@github.com:yns88/emojibot.git

2. Install dependencies:

        pip install -r requirements.txt

3. Configure rtmbot (https://api.slack.com/bot-users)
        
        cp example_rtmbot.conf rtmbot.conf
        vi rtmbot.conf

*Note*: At this point rtmbot is ready to run, however no plugins are configured.

Running the Bot
-------
./rtmbot.py
