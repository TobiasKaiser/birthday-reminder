#!/usr/bin/python3

import sys
import datetime
import smtplib
from email.mime.text import MIMEText
import argparse


class Person:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

    def upcoming_birthday(self):
        day_range = range(0,4)
        for day_interval in day_range:
            day = datetime.date.today() + datetime.timedelta(days=day_interval)
            if self.birthday.month == day.month and self.birthday.day == day.day:
                return True
        return False

    def when(self):
        count_me_down = datetime.date.today()
        new_age = 0
        while count_me_down - self.birthday > datetime.timedelta(days=0):
            count_me_down = datetime.date(day=count_me_down.day, month=count_me_down.month, year=count_me_down.year-1)
            new_age+=1
        days_left = (self.birthday - count_me_down).days
        return new_age, days_left
        

    def __str__(self):
        new_age, days_left = self.when()
        if days_left:
            return "{} wird in {} Tagen {} Jahre alt.".format(self.name, days_left, new_age)
        else:
            return "Heute ist {}'s {}. Geburtstag!".format(self.name, new_age)

def main():

    parser = argparse.ArgumentParser(description="Birthday reminder script.")
    parser.add_argument("directory_file", type=str, nargs=1, help='File Name of the director file')
    parser.add_argument("email_to", type=str, nargs=1, help='Email address to send the reminder to')
    parser.add_argument("--from", dest="email_from", type=str, help="Sender email address")
    parser.add_argument("--smtp-host", dest="email_host", type=str, help="SMTP hostname (default: localhost)")

    args = parser.parse_args()

    bday_file = args.directory_file[0]
    email_to = args.email_to[0]
    if args.email_from:
        email_from = args.email_from
    else:
        email_from = email_to
    if args.email_host:
        email_host = args.email_host
    else:
        email_host = "localhost"

    directory = []

    with open(bday_file, "r") as f:
        for line in f:
            line = line.split(":", 2)
            if len(line) != 2:
                continue
            name_str, bday_str = line 
            name_str = name_str.strip()
            bday_str = bday_str.strip()
            bday = datetime.datetime.strptime(bday_str, "%d.%m.%Y")
            bday = bday.date()
            directory.append(Person(name_str, bday))

    print("Parsed directory of {} persons from {}.".format(len(directory), bday_file))

    upcoming_bday_persons = list(filter(lambda p: p.upcoming_birthday(), directory))


    if len(upcoming_bday_persons) > 0:
        text = "Hallo,\n\n"
        text += "folgende Geburtstage stehen an:\n"
        for person in upcoming_bday_persons:
            text+=" - {}\n".format(
                person
            )
        text+= "\nViele Grüße,\n\n"
        text+= "birthday-reminder"

        print(text)

        msg = MIMEText(text)

        msg['Subject'] = 'Birthday reminder: {}'.format(", ".join(map(lambda p: p.name, upcoming_bday_persons)))
        msg['From'] = email_to
        msg['To'] = email_from

        smtpObj = smtplib.SMTP(email_host)
        smtpObj.send_message(msg)
        smtpObj.quit()

        print("Birthday reminder email was sent.")
    else:
        print("No birthday reminder email was sent.")

if __name__ == "__main__":
    main()
