from flask import Flask, render_template
import BotMe.main as Bot
import time
from multiprocessing import Process, Value


app = Flask(__name__)      

class Test:
   def __init__(self):
      self.num_times_ran = 0      

   def update(self):
      f = open('test.txt', 'w')
      self.num_times_ran += 1
      f.write(str(self.num_times_ran) + "\n")
      f.close()

   def get(self):
      f = open('test.txt', 'r')
      x = f.readlines()
      return x[-1]      

x = Test()

@app.route('/')
def home():
  z = x.get()
  return render_template('home.html', variable = z)
 
def bot_loop(bot, x):
  while True:
     if '!bot' in str(bot.retrieve_message()[1]):
        bot.post_message('Test')
        x.update()
        print(x.get())
  time.sleep(1)

if __name__ == '__main__':
  bot = Bot.Manager('dSMejIEUduqXwDsxB8eO0ReZX26of3SHDojotjp2')
  bot.create_bot('Test', 'Test')
  p = Process(target = bot_loop, args=(bot,x,))
  p.start()  
  app.run(debug=True, use_reloader = False)
  p.join()
