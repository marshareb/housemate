from datetime import date

def get_date_difference(date1, date2):
    date_1 = list(map(lambda x: int(x), date1.split("-")))
    date_1 = date(date_1[0], date_1[1], date_1[2])
    date_2 = list(map(lambda x: int(x), date2.split("-")))
    date_2 = date(date_2[0], date_2[1], date_2[2])
    return int(abs(date_1-date_2).days)

def cycle(lis):
    return lis[1:] + [lis[0]]

class BotController:
  # Static Members
  chores = ['Dishes', 'Trash', 'Sweeping']
  last_date = "2017-08-15"

  UPDATE_WORDS       = ['update']
  GREETING_WORDS = ['hello', 'hi', 'what\'s up'] 
  HELP_WORDS     = ['help', 'you do?']
  CHORES_WORDS = ['chores', 'do']

  # Field List:
  #  (none)

  def __init__(self):
    pass

  def text_preprocessing(self, text):
    return text.lower()

  def process_message(self, recd_msg):
    today_date = str(date.today())
    if get_date_difference(BotController.last_date, today_date) != 0:
        for i in range(get_date_difference):
            BotController.chores = cycle(BotController.chores)
    msg_to_send = {} # reply

    # Preprocessing
    text = recd_msg['text'].lower()

    # Helper function
    used_any = lambda word_list: any(map(lambda x : x in text, word_list))

    # Use some hard-coded rules to decide what this message says
    if used_any(BotController.UPDATE_WORDS):
      today_date = str(date.today())
      if get_date_difference(BotController.last_date, today_date) != 0:
        for i in range(get_date_difference):
            BotController.chores = cycle(BotController.chores)
      msg_to_send['text'] = 'I\'ve updated!'
    elif used_any(BotController.GREETING_WORDS):
      msg_to_send['text'] = 'Greetings to you, as well, {}!'.format(recd_msg['author'])
    elif used_any(BotController.HELP_WORDS):
      msg_to_send['text'] = ('Hi! I\'m the friendly house mate, the chatbot.  I don\'t do much right now,' +
                             ' but I will help remind you who has to do what chore. I\'m still restricted to three chores.')
    elif used_any(BotController.CHORES_WORDS):
        msg_to_send['text'] = ('James: Your chore is ' + BotController.chores[0] +
                               '. Chase: Your chore is ' + BotController.chores[1] +
                               '. Mike: Your chore is ' + BotController.chores[2] +
                               '. Make sure to update me to have accurate chores.')
    else:
      msg_to_send['text'] = 'I can\'t tell what you\'re talking about.'

    return msg_to_send
