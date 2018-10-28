#!/usr/bin/python

import argparse
import datetime
import subprocess
import pickle
import os.path
import regex
import pdb

storageFile = "./tasks.pkl"


def main():
    taskAction = argparse.ArgumentParser(description="Select an action for Todo")
#    taskAction.add_mutually_exclusive_group(required=True)
    taskAction.add_argument("--add", "-a", \
            help="Add a task to your ToDo list")
    taskAction.add_argument("--delete", "-d", \
            help="Remove a task from your ToDo list")
    taskAction.add_argument("--reminder", "-r", \
            help="Set a reminder for your task")
    taskAction.add_argument("--list", "-l", \
            help="Set a reminder for your task", default=False, action="store_true")
    args = taskAction.parse_args()
    
    task = Task(args)
    managetasks = ManageTasks(task)
    
    #subprocess.check_output(['systemctl', 'restart', 'todo-timer.timer']) 
    
class ManageTasks():
    def __init__(self,task):
        self.db = []
        self.opendb()
        self.task = task
        self.actionSwitch()

	
    def opendb(self):
        if os.path.isfile(storageFile):
            with open(storageFile, "rb") as handle: 
                self.db = pickle.load(handle)

    def savedb(self):
        with open(storageFile, "wb") as handle: 
            pickle.dump(self.db, handle)
        
    def actionSwitch(self):
        if self.task.add != None:
            self.new()
        if self.task.delete != None:
            self.delete()
        if self.task.list != None:
            self.list()

    def new(self):
        self.db.append(self.task)
        self.savedb()
    
    def delete(self):
        for index,delTask in enumerate(self.db):    
            if self.task.delete in delTask.add:
                del self.db[index]
                self.delete()          ##function must be recursive to update self.db indexes

    def edit(self):
        pass

    def list(self):
    	print [listTask.add for listTask in self.db]

    def __del__(self):
        self.savedb()
        del self.db
        del self.task



class Task():
    def __init__(self,classargs):
        self.create_time = datetime.datetime.time(datetime.datetime.now())
        self.add = classargs.add
        self.delete = classargs.delete
        self.reminder = classargs.reminder
        self.list = classargs.list

if __name__ == "__main__":
    main()

