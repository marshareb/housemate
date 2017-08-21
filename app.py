import brain
import time
import datetime
import groupy

def process_message(message):
    return message.lower()

if __name__ == '__main__':
    # Get the appropriate variables

    # Housemate here is the name of the bot that housemate will be using.
    index = 0
    bots = groupy.Bot.list()
    for i in range(len(bots)):
        if bots[i] == 'Housemate':
            index = i

    bot = bots[index]

    # apartment here is the name of the group you want Housemate to watch
    index = 0
    groups = groupy.Group.list()
    for i in range(len(groups)):
        if groups[i] == 'apartment':
            index = i

    group = groups[index]

    # Assign the two dates to check.
    last_date = datetime.datetime.now().date()
    last_week = datetime.datetime.now().date()

    brain = brain.Brain(bot, datetime.datetime.now().date())

    #bot.post("Hello! I've been updated or the server has been reset.")

    # Loop to continuously run
    while True:
        current_date = datetime.datetime.now()
        brain.check_date(current_date)

        # Grab the most recent message in the group and lowercase it.
        try:
            last_message = group.messages().newest.text
            brain.process_message(last_message.lower())
        except:
            print("Server down. Will try again later.")

        time.sleep(3)