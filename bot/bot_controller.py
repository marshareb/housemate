import datetime
import random
import os

def file_is_empty(name):
  return os.stat(name).st_size==0

def add_chore(person, chore):
  f = open(str(person + '.txt'), 'a+')
  f.write('\n' + str(chore))
  f.close()

def remove_chore(person, chore):
  f = open(str(person + '.txt'), 'w+')
  for line in f:
    if line == str(chore):
      line.replace(chore, '')
  f.close()

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

def get_chores(person):
  chores = []
  f = open(str(person + '_daily.txt'), 'r')
  fo = open(str(person + '_weekly.txt'), 'r')
  for line in f:
    chores.append(line)
  for line in fo:
    chores.append(line)
  f.close()
  fo.close()
  return chores

def update_daily():
  daily = open('daily_chores.txt', 'r')
  james = open('James_daily.txt', 'w+')
  chase = open('Chase_daily.txt', 'w+')
  mike = open('Mike_daily.txt' 'w+')
  chores = []
  deleteContent(james)
  deleteContent(chase)
  deleteContent(mike)
  for i in daily:
    chores.append(i)
  chores = random.shuffle(chores)
  james.write(chores[0])
  chase.write(chores[1])
  mike.write(chores[2])
  daily.close()
  james.close()
  chase.close()
  mike.close()

def update_weekly():
  weekly = open('weekly_chores.txt', 'r')
  james = open('James_weekly.txt', 'w+')
  chase = open('Chase_weekly.txt', 'w+')
  mike = open('Mike_weekly.txt' 'w+')
  chores = []
  deleteContent(james)
  deleteContent(chase)
  deleteContent(mike)
  for i in weekly:
    chores.append(i)
  chores = random.shuffle(chores)
  james.write(chores[0])
  chase.write(chores[1])
  mike.write(chores[2])
  weekly.close()
  james.close()
  chase.close()
  mike.close()

def from_string(date):
  date = date.split('-')
  date = list(map(lambda x: int(x), date))
  return datetime.date(date[0], date[1], date[2])

def difference_of_dates(date1, date2):
  date1 = from_string(date1)
  date2 = from_string(date2)
  return int(abs((date1-date2).days))

class BotController:
  # Static Members

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

  def process_message(self, recd_msg):
    msg_to_send = {}  # reply
    msg_to_send['text'] = ""
    current_date = str(datetime.datetime.now().date())
    last_dat = open('last_date.txt', 'w+')
    last_date = last_dat.readline()
    last_wek = open('last_week.txt', 'w+')
    last_week = last_wek.readline()
    if last_date == '':
      last_dat.write(str(current_date))
    if last_week == '':
      last_wek.write(str(current_date))
    if file_is_empty('James_daily.txt'):
      msg_to_send['text'] += "I have not been initialized yet. Initializing now."
      update_daily()
      update_weekly()
      last_dat.close()
      last_wek.close()
      return msg_to_send
    if difference_of_dates(str(last_week), current_date) >= 7:
      update_daily()
      update_weekly()
      msg_to_send['text'] += 'It\'s a new week! I\'ve updated the chores. Ask me about chores to see.'
    if last_date != current_date:
      update_daily()
      msg_to_send['text'] += 'It\'s a new day! I\'ve updated the chores. Ask me about chores to see'
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
                             ' but I will help remind you who has to do what chore. \n' +
                             'I\'m still in alpha, so I don\'t promise anything.')
    elif used_any(BotController.UPDATE_WORDS):
      update_daily()
      msg_to_send['text'] += 'Update complete.'
    elif used_any(BotController.CHORES_WORDS):
      msg_to_send['text'] += ""
      for i in ['James', 'Chase', 'Mike']:
        chores = get_chores(i)
        msg_to_send['text'] += i
        msg_to_send['text'] += ": your daily chore is "
        msg_to_send['text'] += chores[0]
        msg_to_send['text'] += " and your weekly chore is "
        msg_to_send['text'] += chores[1]
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
