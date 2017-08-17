import datetime
import random


class BotController:
  # Static Members
  chores_daily = ['(Dishes)', '(Trash)', '(General Cleanliness)']
  chores_weekly = ['(Living Room and Hall)', '(Bathroom)', '(Kitchen)']
  last_date = datetime.datetime.now().date()
  last_week = datetime.datetime.now().date()
  # For rent
  check_monthly = False

  chore_assignment_daily = {'James' : '(Dishes)', 'Chase' : '(Trash)', 'Mike' : '(General Cleanliness)'}
  chore_assignment_weekly = {'James': '(Living Room and Hall)', 'Chase' : '(Bathroom)', 'Mike' : '(Kitchen)'}


  completed_chores = {'dishes' : False, 'trash' : False, 'general_cleanliness' : False,
                            'livingroom_and_hall': False, 'bathroom': False, 'kitchen': False}

  JOKES = ['What’s the difference between a G-spot and a golf ball? A guy will actually search for a golf ball.',
           'Why was the guitar teacher arrested? For fingering a minor.',
           'Why does Santa Claus have such a big sack? He only comes once a year.']
  SONG = ['https://www.youtube.com/watch?v=y6120QOlsfU',
          'https://www.youtube.com/watch?v=L_jWHffIx5E',
          'https://www.youtube.com/watch?v=dQw4w9WgXcQ']
  DATE_WORDS       = ['date']
  UPDATE_WORDS = ['update']
  GREETING_WORDS = ['hello', 'hi', 'what\'s up', 'sup', 'hey']
  JOKE_WORDS = ['joke', 'jokes']
  HELP_WORDS     = ['help', 'you do?']
  CHORES_WORDS = ['chores', 'chore']
  SONG_WORDS = ['music', 'sing']
  COMPLETED_WORDS = ['completed']
  FINISHED_WORDS = ['done']
  # Field List:
  #  (none)

  def __init__(self):
    pass

  def text_preprocessing(self, text):
    return text.lower()

  def update_daily(self):
    temp = []
    for i in self.chores_daily:
      temp.append(i)
    for i in self.chore_assignment_daily:
      x = random.choice(temp)
      self.chore_assignment_daily[i] = x
      temp.remove(x)
    self.last_date = datetime.datetime.now().date()

  def update_weekly(self):
    temp = []
    for i in self.chores_weekly:
      temp.append(i)
    for i in self.chore_assignment_weekly:
      x = random.choice(temp)
      self.chore_assignment_weekly[i] = x
      temp.remove(x)
    self.last_week = datetime.datetime.now().date()

  def process_message(self, recd_msg):
    msg_to_send = {}  # reply
    msg_to_send['text'] = ""
    current_date = datetime.datetime.now().date()
    if current_date.day == 28 and self.check_monthly == False:
      msg_to_send['text'] += "Don't forget about rent!\n"
      self.check_monthly = True
    elif current_date.day != 28 and self.check_monthly == True:
      self.check_monthly = False
    if int(abs(self.last_week - current_date).days) >= 7:
      self.update_weekly(self)
      self.update_daily(self)
      msg_to_send['text'] += 'It\'s a new week! I\'ve updated the chores. Ask me about chores to see.'
      for i in self.completed_weekly_chores:
          self.completed_weekly_chores[i] = False
    if self.last_date != current_date:
      self.update_daily()
      msg_to_send['text'] += 'It\'s a new day! I\'ve updated the chores. Ask me about chores to see'
      for i in self.completed_daily_chores:
          self.completed_daily_chores[i] = False
      return msg_to_send

    # Preprocessing
    text = recd_msg['text'].lower()

    # Helper function
    used_any = lambda word_list: any(map(lambda x : x in text, word_list))

    # Use some hard-coded rules to decide what this message says
    if used_any(BotController.GREETING_WORDS):
      msg_to_send['text'] = 'Greetings to you {}!'.format(recd_msg['author'])
    #elif used_any(BotController.DATE_WORDS):
    #  msg_to_send['text'] += 'The last date is ' + str(BotController.last_date) + ' and the current date is ' + str(current_date)
    elif used_any(BotController.HELP_WORDS):
      msg_to_send['text'] += ('Hi! I\'m  housemate, the friendly chatbot.  I don\'t do much right now,' +
                             ' but I will help remind you who has to do what chore.')
    elif used_any(BotController.UPDATE_WORDS):
      self.update_daily()
      msg_to_send['text'] += 'Update complete.'
    elif used_any(BotController.COMPLETED_WORDS):
      # clean up message
      msg = recd_msg['text'].split()
      msg.remove('housemate')
      msg.remove('completed')
      if len(msg) != 1:
        msg_to_send['text'] += 'Error: cannot find chore.'
      else:
        if msg[0] in self.completed_chores:
          self.completed_chores[msg[0]] = True
          msg_to_send['text'] += 'Congrats for finishing the chore ' + str(msg[0])
        else:
          msg_to_send['text'] += 'Error: cannot find chore.'
    elif used_any(BotController.CHORES_WORDS):
      msg_to_send['text'] += ""
      for i in BotController.chore_assignment_daily:
        msg_to_send['text'] += i
        msg_to_send['text'] += ": your daily chore is "
        msg_to_send['text'] += BotController.chore_assignment_daily[i]
        msg_to_send['text'] += " and your weekly chore is "
        msg_to_send['text'] += BotController.chore_assignment_weekly[i]
        msg_to_send['text'] += "\n"
      msg_to_send['text'] += "Make sure to do them!"
    elif used_any(BotController.JOKE_WORDS):
      msg_to_send['text'] += random.choice(BotController.JOKES)
    elif used_any(BotController.FINISHED_WORDS):
      chores = []
      for i in self.completed_chores:
        if self.completed_chores[i] == False:
          chores.append(i)
      if len(chores) == 0:
        msg_to_send['text'] += 'Congrats! All chores are done!'
      else:
        msg_to_send['text'] += "Chores to be done: \n"
        for i in chores:
          msg_to_send['text'] += str(i) + "\n"
    elif used_any(BotController.SONG_WORDS):
      msg_to_send['text'] += random.choice(BotController.SONG)
    else:
      msg_to_send['text'] += 'I can\'t tell what you\'re talking about.'

    return msg_to_send
