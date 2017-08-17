import groupy
import datetime
import time

if __name__ == '__main__':
    bot = groupy.Bot.list().first
    # i represents the index
    last_date = datetime.datetime.now().date()
    while True:
        print('running...')
        print('last date: ' + str(last_date))
        current_date = datetime.datetime.now().date()
        print('current date: ' + str(current_date))
        if last_date != current_date:
            print('It\'s a new day!')
            bot.post("Beginning daily update...")
            last_date = datetime.datetime.now().date()
    time.sleep(3600)