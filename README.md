emojibot
=============
A Slack bot based on [rtmbot](https://github.com/slackhq/python-rtmbot) that suggests images for custom emoji.

![Image of emojibot in action](http://i.imgur.com/1Edtk7I.png)


Installation
-----------

1. Clone the repo

        git clone git@github.com:yns88/emojibot.git
        cd emojibot

2. Install dependencies:

        pip install -r requirements.txt

3. Configure rtmbot (https://api.slack.com/bot-users)
        
        cp example_rtmbot.conf rtmbot.conf
        vi rtmbot.conf

Running the Bot
-------
./rtmbot.py
