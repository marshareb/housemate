import groupy
import datetime
import time

if __name__ == '__main__':
    groups = groupy.Group.list()
    # i represents the index
    i = 0
    for g in groups:
        if g.name == "apartment":
            break
        i += 1
    last_date = datetime.datetime.now().date()
    while True:
        current_date = datetime.datetime.now().date()
        if last_date != current_date:
            groups[i].post("It's a new day.")
            last_date = datetime.datetime.now().date()
        time.sleep(3600)