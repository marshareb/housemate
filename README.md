Housemate
========

A bot to help with chores around the house.

You need to run dailyupdater.py separately in order to get around the fact that heroku won't update daily. For example,
we have it running on a raspberry pi server.

This is also personalized for our GroupMe.

Example commands:

```
housemate chores
```

returns who needs to do what chores and by when.

```
housemate jokes
```

returns a random joke.

Chores are determined randomly. There are two subcategories of chores; daily and weekly. These are updated appropriately
so long as you either have dailyupdater.py running or you use the chat daily.


Further instructions TBD.
