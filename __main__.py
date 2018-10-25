#!/bin/python

import argparse
import datetime
import pandas


def main():
    cliparser = argparse.ArgumentParser()
    cliparser.add_argument("--add", "-a", help="Add a task to your ToDo list")
    cliparser.add_argument("--delete", "-d", help="Remove a task from your ToDo list")
    cliparser.add_argument("--reminder", "-r", help="Set a reminder for your task")

    args = cliparser.parse_args()


class Task():
    def __init__(self):
        self.create_time = datetime.datetime.time(datetime.datetime.now())
        self.subject = args.add
        self.reminder = args.reminder


if __name__ == "__main__.py":
    main()
