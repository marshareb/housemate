# Housemate

## What is Housemate?
Housemate is a GroupMe bot designed to keep track of basic household duties. He's also versatile, so you can add other features to him that I haven't thought of.

## How to add Housemate?

First, clone the repo then run

```
pip install -r requirements
```

Next, you'll need to add a .groupy.key file to your home directory, and in it copy and paste your access token. In order to do that,
you'll go to https://dev.groupme.com and click on the access token tab in the top right.

After creating your .groupy.key file, you'll need to next build a bot. While in https://dev.groupme.com, click on the Bots tab
and click Create a Bot. Give the bot the name 'Housemate' and whatever Avatar URL you want. Move your bot to the appropriate group.

Finally, on line 15 in app.py change the name from 'apartment' to the name of your group. Run app.py on a dedicated computer or server, and you now have
a housemate bot!

## Why housemate?

I created Housemate using Groupy as a counterpart to most of the Heroku GroupMe bots. Heroku has the issue of using
Dynos to manage memory, which often messed with the memory of Housemate (since all of the data is saved on temporary memory).
Using the Groupy API along with a refresh rate of checking the messages, you can run Housemate on any computer.


