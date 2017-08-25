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

In the folder, create a text file called "address.txt", with the name of the city that the house is located in. This is so that
Housemate can grab the weather information for your city.

Finally, on line 15 in app.py change the name from 'apartment' to the name of your group. Run app.py on a dedicated computer or server, and you now have
a housemate bot!

## Why Housemate?

I created Housemate using Groupy as a counterpart to most of the Heroku GroupMe bots. Heroku has the issue of using
Dynos to manage memory, which often messed with the memory of Housemate (since all of the data is saved on temporary memory).
Using the Groupy API along with a refresh rate of checking the messages, you can run Housemate on any computer. Housemate
is still in beta, so he'll probably run into some errors along the way.

## Example of use

Note that in order to call Housemate, you must preface every command with '!housemate'. For example, in order to get
the chores assigned to each person, you message

```
!housemate chores
```

If you want to see what needs to be done in general, you message

```
!housemate done
```

(though I generally like to use '!housemate what needs to be done'). To signify that you finished a chore, you message

```
!housemate finished [chore]
```

Housemate even knows some jokes. To have him tell you a joke, you message

```
!housemate tell me a joke
```

If you'd like to trade a chore with a person, you message

```
!housemate trade [person1] [person2] [timeframe]
```

For example, if James and Mike wanted to trade their daily chores, one of them would message

```
!housemate trade James Mike daily
```

## Future Development

I'd like to have Housemate be integrated to other features in order to have an easy way to create and manage a smart home
from GroupMe.


