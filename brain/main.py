import random

# Used any function
def used_any(text, word_list):
    return any(list(map(lambda x: x in text, word_list)))


class Brain:
    # Chores to keep track of
    chores_daily = ['(Dishes)', '(Trash)', '(General Cleanliness)']
    chores_weekly = ['(Living Room and Hall)', '(Bathroom)', '(Kitchen)']

    # People who live in the apartment
    people = ['james', 'chase', 'mike']

    # Assignment hashtable
    chores_assignment_daily = {'James': '', 'Chase': '', 'Mike': ''}
    chores_assignment_weekly = {'James': '', 'Chase': '', 'Mike': ''}

    # Completed Chores hashtable
    completed_chores = {'dishes' : False, 'trash' : False, 'general_cleanliness' : False, 'living_room_and_hall' : False,
                        'bathroom' : False, 'kitchen' : False}

    # Stuff for fun
    JOKES = ['What’s the difference between a G-spot and a golf ball? A guy will actually search for a golf ball.',
             'Why was the guitar teacher arrested? For fingering a minor.',
             'Why does Santa Claus have such a big sack? He only comes once a year.']
    SONG = ['https://www.youtube.com/watch?v=y6120QOlsfU',
            'https://www.youtube.com/watch?v=L_jWHffIx5E',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ']

    rent_check = False

    # Key Words
    DATE_WORDS = ['date']
    UPDATE_WORDS = ['update']
    GREETING_WORDS = ['hello', 'hi', 'what\'s up', 'sup']
    JOKE_WORDS = ['joke', 'jokes']
    HELP_WORDS = ['help']
    CHORES_WORDS = ['chores', 'chore']
    SONG_WORDS = ['music', 'sing']
    COMPLETED_WORDS = ['finished']
    UNDO_WORDS = ['back']
    TODO_WORDS = ['do', 'done']
    TRADE_WORDS = ['trade']


    # Resets completed chores.
    def reset_chores(self, daily):
        if daily == True:
            for i in self.chores_daily:
                self.completed_chores[i] = False
        else:
            for i in self.chores_weekly:
                self.completed_chores[i] = False

    # Update the chores
    def update_chores(self, daily):
        temp = []
        if daily == True:
            for i in self.chores_daily:
                temp.append(i)
            for i in self.chores_assignment_daily:
                x = random.choice(temp)
                self.chores_assignment_daily[i] = x
                temp.remove(x)
        else:
            for i in self.chores_weekly:
                temp.append(i)
            for i in self.chores_assignment_weekly:
                x = random.choice(temp)
                self.chores_assignment_weekly[i] = x
                temp.remove(x)

    def trade(self, person1, person2, time):
        if time == 'daily':
            chore1 = self.chores_assignment_daily[person1]
            chore2 = self.chores_assignment_daily[person2]
            self.chores_assignment_daily[person1] = chore2
            self.chores_assignment_daily[person2] = chore1
        else:
            chore1 = self.chores_assignment_weekly[person1]
            chore2 = self.chores_assignment_weekly[person2]
            self.chores_assignment_weekly[person1] = chore2
            self.chores_assignment_weekly[person2] = chore1

    def __init__(self, Bot, date):
        self.last_date = date
        self.last_week = date
        self.bot = Bot
        # Initialize chores
        self.update_chores(True)
        self.update_chores(False)

    def check_date(self, obdate):
        hour = obdate.time().hour
        date = obdate.date()
        if int(hour) == 5 and int(date.day) == 28:
            self.bot.post("Don't forget about rent!")
        if self.last_date != date:
            # Asign new daily chores
            self.update_chores(True)

            # Reset chores daily
            self.reset_chores(True)

            self.last_date = date

            self.bot.post("It's a new day!")
        if int(abs((date - self.last_week).days)) >= 7:
            # Assign new people to weekly chores
            self.update_chores(False)

            # Reset chores weekly
            self.reset_chores(False)

            # Reset date
            self.last_week = date

            self.bot.post("Finished updating!")

    def process_message(self, last_message):
        # Check if any word lists were used.
        if '!housemate' in last_message:
            if used_any(last_message, self.UPDATE_WORDS):
                # To double check if updating is working.
                self.bot.post('Updating...')
                chore_assignment_daily = self.update_chores(True)
                self.bot.post('Finished updating!')
            elif used_any(last_message, self.GREETING_WORDS):
                self.bot.post('Heyo')
            elif used_any(last_message, self.JOKE_WORDS):
                x = random.choice(self.JOKES)
                self.bot.post(x)
            elif used_any(last_message, self.SONG_WORDS):
                x = random.choice(self.SONG)
                self.bot.post(x)
            elif used_any(last_message, self.CHORES_WORDS):
                msg_to_send = ""
                for i in self.chores_assignment_daily:
                    msg_to_send += i
                    msg_to_send += ": your daily chore is "
                    msg_to_send += self.chores_assignment_daily[i]
                    msg_to_send += " and your weekly chore is "
                    msg_to_send += self.chores_assignment_weekly[i]
                    msg_to_send += "\n"
                msg_to_send += "Make sure to do them!"
                self.bot.post(msg_to_send)
            elif used_any(last_message, self.COMPLETED_WORDS):
                last_message = last_message.split()
                last_message.remove('!housemate')
                last_message.remove('finished')

                try:
                    if last_message[0] not in self.completed_chores:
                        self.bot.post("Nice try, but " + str(last_message[0]) + " isn\'t a chore.")
                    else:
                        self.completed_chores[last_message[0]] = True
                        self.bot.post("Congrats on completing " + str(last_message[0]) + "!")
                except:
                    self.bot.post("Sorry, I don't understand.")
            elif used_any(last_message, self.UNDO_WORDS):
                last_message = last_message.split()
                last_message.remove('!housemate')
                last_message.remove('back')
                try:
                    if last_message[0] not in self.completed_chores:
                        self.bot.post("Nice try, but " + str(last_message[0]) + " isn\'t a chore.")
                    else:
                        self.completed_chores[last_message[0]] = False
                        self.bot.post("Innocent mistake. Just don't do it again ;)")
                except:
                    self.bot.post("Sorry, I don't understand.")
            elif used_any(last_message, self.TRADE_WORDS):
                last_message = last_message.split()
                last_message.remove('!housemate')
                last_message.remove('trade')
                try:
                    if last_message[2] == 'daily' or last_message[2] == 'weekly':
                        if last_message[0] in self.people and last_message[1] in self.people:
                            self.trade(last_message[0].title(), last_message[1].title(), last_message[2])
                            self.bot.post("Trade complete.")
                        else:
                            self.bot.post("I don't understand the names. Try again")
                    else:
                        self.bot.post("I don't understand the time frame. Try again.")
                except:
                    self.bot.post("Sorry, I don't understand.")
            elif used_any(last_message, self.TODO_WORDS):
                msg_to_send = ""
                chores = []
                for i in self.completed_chores:
                    if self.completed_chores[i] == False:
                        chores.append(i)
                if len(chores) == 0:
                    self.bot.post("Congrats! There's no chores to do!")
                msg_to_send += "To be done: \n"
                for i in chores:
                    msg_to_send += str(i)
                    msg_to_send += "\n"
                self.bot.post(msg_to_send)
            elif used_any(last_message, self.HELP_WORDS):
                self.bot.post("I\'m here to let you know what chores need to be done and when!")
            else:
                self.bot.post("Sorry, I don't understand.")