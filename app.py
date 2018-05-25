import brain
import datetime
import groupy
from flask import Flask, render_template, request
import time
from multiprocessing import Process
import os

app = Flask(__name__)

@app.route('/')
def home():
    choreList = writer.get()
    templateData = {
        'daily_chores' : choreList[0],
        'weekly_chores' : choreList[1]
    }
    return render_template('home.html', **templateData)

@app.route('/home')
def home2():
    choreList = writer.get()
    templateData = {
        'daily_chores' : choreList[0],
        'weekly_chores' : choreList[1]
    }
    return render_template('home.html', **templateData)

@app.route('/update')
def update():
    writer.write_command('UPDATE')
    return render_template('update.html')

@app.route('/chores')
def chores():
    writer.write_command('CHORES')
    choreList = writer.get()
    templateData = {
        'daily_chores': choreList[0],
        'weekly_chores': choreList[1]
    }
    return render_template('home.html', **templateData)

@app.route('/trade')
def trade():
    return render_template('trade.html')

@app.route('/trade', methods=['POST'])
def trade_post():
    text = request.form['input']
    writer.write_command('TRADE\n' + str(text))
    return render_template('trade.html')


@app.route('/completed_chore')
def completed_chore():
    return render_template('completed_chore.html')

@app.route('/completed_chore', methods=['POST'])
def completed_chore_post():
    text = request.form['input']
    writer.write_command('COMPLETE\n' + str(text))
    return render_template('completed_chore.html')

@app.route('/todo')
def todo():
    writer.write_command('TODO')
    todo = writer.get_todo()
    templateData = {
        'todo' : todo
    }
    return render_template('todo.html', **templateData)


class Writer:
    def __init__(self, brain):
        self.brain = brain
        self.chores_assignment_daily = self.brain.chores_assignment_daily
        self.chores_assignment_weekly = self.brain.chores_assignment_weekly
        f = open('info.txt', 'w')
        f.write(str(self.chores_assignment_daily) + "\n")
        f.write(str(self.chores_assignment_weekly))
        f.close()

    def update(self):
        self.chores_assignment_daily = self.brain.chores_assignment_daily
        self.chores_assignment_weekly = self.brain.chores_assignment_weekly
        chores = []
        for i in self.brain.completed_chores:
            if self.brain.completed_chores[i] == False:
                chores.append(i)
        msg_to_send = ''
        msg_to_send += "To be done: "
        for i in chores:
            msg_to_send += str(i) + " "
        f = open('info.txt', 'w')
        f.write(str(self.chores_assignment_daily) + "\n")
        f.write(str(self.chores_assignment_weekly))
        f.close()
        f = open('todo.txt', 'w')
        f.write(str(msg_to_send))
        f.close()

    def get(self):
        f = open('info.txt', 'r')
        x = f.readlines()
        f.close()
        return [x[0], x[1]]

    def get_todo(self):
        f = open('todo.txt', 'r')
        x = f.readlines()
        f.close()
        return x[0]

    def write_command(self, command):
        f = open('command.txt', 'w', os.O_NONBLOCK)
        f.write(command)
        f.close()

    def read_command(self):
        f = open('command.txt', 'r', os.O_NONBLOCK)
        x = f.readlines()[0]
        f.close()
        return x

    def read_trade(self):
        f = open('command.txt', 'r', os.O_NONBLOCK)
        x = f.readlines()[1]
        f.close()
        print(x)
        print(1)
        return x

def process_message(message):
    return message.lower()

def get_location():
    import requests
    r = requests.get('https://api.ipdata.co').json()
    address = str(r['city']) + ', ' + str(r['region'])
    cons_key = ''
    cons_key_sec = ''
    acc_key = ''
    acc_key_sec = ''
    return str(address), (cons_key, cons_key_sec, acc_key, acc_key_sec)

def bot_loop(brain, writer):
    print(brain.group)
    brain.process_message('!housemate chores')
    while True:
        current_date = datetime.datetime.now()
        brain.check_date(current_date)
        writer.update()
        if writer.read_command() != 'NONE':
            print(writer.read_command())
            if writer.read_command() == 'UPDATE':
                brain.process_message('!housemate update')
                writer.write_command('NONE')
            elif writer.read_command() == 'CHORES':
                brain.process_message('!housemate chores')
                writer.write_command('NONE')
            elif 'TRADE' in writer.read_command():
                x = writer.read_trade()
                x = x.split()
                timeframe = x[-1]
                x = ' '.join(x)
                x = x.lower()
                persons = []
                for i in brain.people:
                    if i in x:
                        persons.append(i)
                try:
                    brain.process_message('!housemate trade ' + str(persons[0]) + ' ' + str(persons[1]) + ' ' + str(timeframe))
                except:
                    print('ERROR')
                    pass
                writer.write_command('NONE')
            elif 'COMPLETE' in writer.read_command():
                x = writer.read_trade()
                try:
                    brain.process_message('!housemate finished ' + str(x))
                except:
                    print('ERROR')
                writer.write_command('NONE')
            elif 'TODO' in writer.read_command():
                brain.process_message('!housemate todo')
                writer.write_command('NONE')
        # Grab the most recent message in the group and lowercase it.
        last_message = group.messages().newest.text
        brain.process_message(last_message.lower())
        time.sleep(1)


if __name__ == '__main__':
    # Get the appropriate variables


    # Apartment here is the name of the group you want Housemate to watch
    index = 0
    groups = groupy.Group.list()
    for i in range(len(groups)):
        if str(groups[i]).split()[0] == 'Newtest,':
            index = i
            break
    group = groups[index]

    # Get members of the group.
    members = group.members()[0:3]

    # Housemate here is the name of the bot that housemate will be using.
    index = 0
    bots = groupy.Bot.list()

    for i in range(len(bots)):
        if str(bots[i]) == 'Test':
            index = i
            break

    bot = bots[i]
    # Assign the two dates to check.
    last_date = datetime.datetime.now().date()
    last_week = datetime.datetime.now().date()

    location, k = get_location()

    brain = brain.Brain(bot, datetime.datetime.now().date(), location, members, group)
    writer = Writer(brain)

    p = Process(target=bot_loop, args=(brain, writer,))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
