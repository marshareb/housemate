import brain
import time
import datetime
import groupy

def process_message(message):
    return message.lower()

def get_location():
    # Get the address from address.txt
    # UPDATE: Also grabs Twitter keys
    f = open("address.txt", 'r')
    address = f.readline()
    cons_key = str(f.readline())
    cons_key_sec = str(f.readline())
    acc_key = str(f.readline())
    acc_key_sec = str(f.readline())
    f.close()

    return str(address), (cons_key, cons_key_sec, acc_key, acc_key_sec)


if __name__ == '__main__':
    # Get the appropriate variables


    # apartment here is the name of the group you want Housemate to watch
    index = 0
    groups = groupy.Group.list()
    for i in range(len(groups)):
        print(i)
        if str(groups[i]).split()[0] == 'Apartment,':
            index = i
            break
    group = groups[index]

    # Get members of the group.
    members = group.members()[0:3]

    # Housemate here is the name of the bot that housemate will be using.
    index = 0
    bots = groupy.Bot.list()
    try:
        for i in range(len(bots)):
            if bots[i] == 'Housemate':
                index = i
        bot = bots[index]
    except:
        bot = groupy.Bot.create('Housemate', group)
        bot.post("I'm alive!")

    # Assign the two dates to check.
    last_date = datetime.datetime.now().date()
    last_week = datetime.datetime.now().date()

    location, k = get_location()

    brain = brain.Brain(bot, datetime.datetime.now().date(), location, members, group, k[0], k[1], k[2], k[3])

    bot.post("Hello! I've been updated or the server has been reset.")

    # Loop to continuously run
    while True:
        current_date = datetime.datetime.now()
        brain.check_date(current_date)

        # Grab the most recent message in the group and lowercase it.
        try:
            last_message = group.messages().newest.text
            brain.process_message(last_message.lower())
        except:
            pass

        time.sleep(3)
