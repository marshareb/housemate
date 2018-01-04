import random
import weather
import groupy
import urllib.request

def get_currency(code):
   # Get the appropriate url
   url = 'https://finance.yahoo.com/quote/' + str(code) + 'USD=X/'
   # Open url and convert page into a string
   f = urllib.request.urlopen(url)
   x = str(f.read()).split('<')
   return float(x[236].split('>')[-1].replace(',',''))

# Used any function
def used_any(text, word_list):
    return any(list(map(lambda x: x in text, word_list)))


class Brain:
    # Chores to keep track of
    chores_daily = ['(Dishes)', '(Trash)', '(General Cleanliness)']
    chores_weekly = ['(Living Room and Hall)', '(Bathroom)', '(Kitchen)']

    chores_hashtable = {'(Dishes)' : 'dishes', '(Trash)' : 'trash', '(General Cleanliness)' : 'general_cleanliness'}

    # Completed Chores hashtable
    completed_chores = {'dishes' : False, 'trash' : False, 'general_cleanliness' : False, 'living_room_and_hall' : False,
                        'bathroom' : False, 'kitchen' : False}

    completed_chores_daily = ['dishes', 'trash', 'general_cleanliness']
    completed_chores_weekly = ['living_room_and_hall', 'bathroom', 'kitchen']

    # Stuff for fun
    JOKES = ['A man is washing his car with his son when the boy goes \'Dad, can\'t we use a sponge?\'',
             'Dads are like boomerangs. \n\n\nI hope',
             'What\'s the difference between in-laws and outlaws? Outlaws are wanted.']

    SONG = ['https://www.youtube.com/watch?v=y6120QOlsfU',
            'https://www.youtube.com/watch?v=L_jWHffIx5E',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ']

    last_hour = False
    rent_check = False
    reminder = False
    weather_check = False


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
    WEATHER_WORDS = ['forecast', 'weather']
    ROLL_WORDS = ['roll']
    CRYPTO_WORDS = ['price']

    # Resets completed chores.
    def reset_chores(self, daily):
        if daily == True:
            for i in self.completed_chores_daily:
                self.completed_chores[i] = False
        else:
            for i in self.completed_chores_weekly:
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

    def roll(self, die):
        return random.randint(1, int(die))

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

    def __init__(self, Bot, date, location, members, group):
        self.weather = weather.Weather()
        self.people = []
        self.group = group
        for i in members:
            self.people.append(i.nickname.lower())

        self.members = {}
        self.chores_assignment_daily = {}
        self.chores_assignment_weekly = {}

        # Get the user id and initialize things
        for i in members:
            self.members[i.nickname] = i.user_id
            self.chores_assignment_daily[i.nickname] = ''
            self.chores_assignment_weekly[i.nickname] = ''

        self.location = location
        self.last_date = date
        self.last_week = date
        self.bot = Bot
        # Initialize chores
        self.update_chores(True)
        self.update_chores(False)

    def get_weather(self, not_tomorrow = True):
        try:
            weather = self.weather.lookup_by_location(self.location)
        except:
            raise ValueError("Address file is empty")
        try:        
            if not_tomorrow:
               # Get the forecast for today
               forecast = weather.forecast()[0]
               message = ""
               message += ("The forecast for today is " + str(forecast['text']) + ". \n")
               message += ("The high for today is " + str(forecast['high']) + " and the low for today is " +
                             str(forecast['low']) + ".")
            else:
               # Get the forecast for tomorrow
               forecast = weather.forecast()[1]
               message = ""
               message += ("The forecast for tomorrow is " + str(forecast['text'] + ". \n"))
               message += ("The high for tomorrow is " + str(forecast['high']) + " and the low for tomorrow is " +
                                                                               str(forecast['low']) + ".")
        except:
            message = "Unable to get weather. Try again later."        
        self.bot.post(message)

    def check_date(self, obdate):
        hour = obdate.time().hour
        minute = obdate.time().minute
        date = obdate.date()
        # init the last_hour variable.
        if self.last_hour == False:
            self.last_hour = obdate.time().hour

        if int(hour) == 10 and int(minute) == 30 and int(date.day) == 20 and self.rent_check == False:
            self.rent_check = True
            self.bot.post("Don't forget about rent!")
        if int(hour) == 6 and int(minute) == 30 and self.weather_check == False:
            self.weather_check = True
            self.get_weather()

        if int(hour) >= 20 and self.reminder == False:
            # Find which daily chores have been completed.
            x = []
            for i in self.completed_chores_daily:
                if not self.completed_chores[i]:
                    x.append(i)
            # Compose the message
            if x == []:
                pass
            else:
                msg = ""
                msg += "Reminder: you still need to do "
                for i in x:
                    msg += i
                    msg += "\n"
                self.bot.post(msg)
            self.reminder = True

        if self.last_date != date:
            # Asign new daily chores
            self.update_chores(True)

            # Reset reminder
            self.reminder = False

            # Reset chores daily
            self.reset_chores(True)

            self.last_date = date

            # Reset daily variables
            self.weather_check = False
            self.rent_check = False

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
                self.update_chores(True)
                self.bot.post('Finished updating!')
            elif used_any(last_message, self.GREETING_WORDS):
                self.bot.post('Heyo')
            elif used_any(last_message, self.JOKE_WORDS):
                x = random.choice(self.JOKES)
                self.bot.post(x)
            elif used_any(last_message, self.SONG_WORDS):
                x = random.choice(self.SONG)
                self.bot.post(x)
            elif used_any(last_message, self.WEATHER_WORDS):
                last_message = last_message.split()
                last_message.remove('!housemate')
                if last_message[0] == 'forecast' or last_message[0] == 'weather':
                    last_message.remove(last_message[0])
                if len(last_message) == 0:
                    self.get_weather()
                else:
                    if last_message[0] == 'tomorrow':
                        self.get_weather(not_tomorrow = False)
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
            elif used_any(last_message, self.ROLL_WORDS):
                last_message = last_message.split()
                last_message.remove('!housemate')
                last_message.remove('roll')
                try:
                    self.bot.post("You rolled a " + str(self.roll(int(last_message[0]))))
                except:
                    self.bot.post("Sorry, I don't understand.")
            elif used_any(last_message, self.CRYPTO_WORDS):
                last_message = last_message.split()
                last_message.remove('!housemate')
                last_message.remove('price')
                try:
                    self.bot.post("The price for " + str(last_message[0]) + " is " + str(get_currency(str(last_message[0]))))
                except:
                    self.bot.post("Sorry, I don't understand.")
            else:
                self.bot.post("Sorry, I don't understand.")
