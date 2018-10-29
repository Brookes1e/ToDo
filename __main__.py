#!/usr/bin/python

import argparse
import datetime
import subprocess
import pickle
import os.path
import time 
import pdb
import tempfile

storageFile = "./tasks.pkl"


def main():
    taskAction = argparse.ArgumentParser(description="Select an action for Todo")
    
    #----Action Arguments----#
    taskAction.add_argument("--add", "-a", \
            help="Add a task to your ToDo list")
    taskAction.add_argument("--delete", "-d", \
            help="Remove a task from your ToDo list")
    taskAction.add_argument("--reminder", "-r", \
            help="Set a reminder for your task")
    taskAction.add_argument("--list", "-l", \
            help="Set a reminder for your task", default=False, action="store_true")
    taskAction.add_argument("--edit", "-e", \
            help="Edit the infomation stored for the task")
    taskAction.add_argument("--description", "-s", \
            help="Set a description for the task", type=str, default="")
    
    args = taskAction.parse_args()
    
    task = Task(args)
    managetasks = ManageTasks(task)
    
    #subprocess.check_output(['systemctl', 'restart', 'todo-timer.timer']) 
    
class ManageTasks():
    """
    Class to manage user defined actions from the command line
    which control and update the live db instance and then saves
    to a pickle object file on destruction of the instance.   
    """
    def __init__(self,task):
        """
        Initialization of the ManageTasks class, this method also triggers
        other methods in the class that are critical to the applications 
        workflow
        """
        self.db = []
        self.opendb()
        self.task = task
        self.actionSwitch()

	
    def opendb(self):
        """
        Method that provides access of infomation to the instance db from the
        persisted pickle file.
        """
        if os.path.isfile(storageFile):
            with open(storageFile, "rb") as handle: 
                self.db = pickle.load(handle)

    def savedb(self):
        """
        Method that allows the instance db to dump data to the pickle file.
        """
        with open(storageFile, "wb") as handle: 
            pickle.dump(self.db, handle)
        
    def actionSwitch(self):
        """
        Mehod that determines the action method that should be triggered from
        the user CLI inputs. A slightly blunt method which could do with 
        improving...
        """
        if self.task.add != None:
            self.new()
        if self.task.delete != None:
            self.delete()
        if self.task.list != None:
            self.list()
        if self.task.edit != None:
            self.edit()

    def new(self):
        """
        Method to add new tasks to the instance db
        """
        self.db.append(self.task)
        self.savedb()
    
    def delete(self):
        """
        Method for removing tasks from the instance db
        """
        for index,delTask in enumerate(self.db):    
            if self.task.delete in delTask.add:
                del self.db[index]
                self.delete()          ##function must be recursive to update self.db indexes

    def edit(self):
        """
        Method for editing tasks from the instance db
        """
        for index,editTask in enumerate(self.db):    
            if self.task.edit in editTask.add:
                with tempfile.NamedTemporaryFile(mode='r+w+b',delete=False) as temp:
                    temp.write(editTask.add + "\n\n" + editTask.description)
                    temp.flush()
                    temp.close()
                    if os.path.isfile(temp.name):
                        subprocess.call('vi '+temp.name,shell=True)
                
                with open(temp.name,"rb") as temp:
                    viDescription = ""
                    for line_number,line in enumerate(temp):
                        print line_number," ", line
                        if line_number == 0:
                            editTask.add = line[:-1]
                        if line_number >= 2:
                            viDescription = viDescription+line
                            editTask.description = viDescription
                    print editTask.description
        self.savedb()

    def list(self):
        """
        Method for viewing tasks in the instance db
        """
    	print [listTask.add for listTask in self.db]

    def __del__(self):
        """
        Destructor the for ManageTask class, explitly dumping the instance db to persiatnce
        and destroying any initiliazed variables. 
        """
        self.savedb()
        del self.db
        del self.task



class Task():
    """
    Class to hold variable values specific to the task defined by the user,
    works as a container and is useless without the ManageTasks Class wrapper
    """
    def __init__(self,classargs):
        """
        Initilisation function of the Task Class, where the required varibles 
        are defined
        """
        self.create_time = datetime.datetime.time(datetime.datetime.now())
        self.add = classargs.add
        self.delete = classargs.delete
        self.reminder = classargs.reminder
        self.list = classargs.list
        self.edit = classargs.edit
        self.description = classargs.description

if __name__ == "__main__":
    main()

