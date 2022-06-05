import pytest
from .checklists import *
from .common import UserInputMocker, ArchivingTestApp, assert_lists_identical
import os
import shutil
import copy
from nurse import nurse, string_to_delta
from datetime import datetime, timedelta
import sys
import time

if sys.version_info[0] == 2:
    import errno

    class FileExistsError(OSError):
        def __init__(self, msg):
            super(FileExistsError, self).__init__(errno.EEXIST, msg)

class FilesystemObject(object):
    def create(self, in_path="."):
        pass

class Directory(FilesystemObject):
    def __init__(self, name=None, contains=[]):
        self.name = name
        self.contains = contains

    def create(self, in_path="."):
        self.my_path = os.path.join(in_path, self.name)
        
        try:
            os.mkdir(self.my_path)
        except (FileExistsError, OSError) as fe:
            pass

        for obj in self.contains:
            obj.create(self.my_path)

    def delete(self):
        shutil.rmtree(self.my_path)

class File(FilesystemObject):
    def __init__(self, name=None, modified_time=None):
        self.name = name
        self.modified_time = modified_time

    def create(self, in_path="."):
        # use this instead of datetime.timestamp to support Python 2.7
        def to_seconds(date):
            return time.mktime(date.timetuple())

        self.my_path = os.path.join(in_path, self.name)

        with open(self.my_path, "w") as fd:
            fd.write("This is a mock file used for testing purposes.")
        
        new_access_time = to_seconds(datetime.now())
        new_modified_time = to_seconds(self.modified_time)

        os.utime(self.my_path, (new_access_time, new_modified_time))
    
    def delete(self):
        shutil.rmtree(self.my_path)

def str_to_datetime(string):
    return datetime.today() + string_to_delta(string)

def test_checklist_nested_files(mocker):
    user_input_dict = [("Question 1" , "Y")]

    expected_archived_paths = ["./mock_files/New1.txt",
                               "./mock_files/test_1/New2.txt",
                               "./mock_files/test_1/test_2/New3.txt"]

    # Generate Tree
    Tree = Directory("mock_files", [Directory("test_1", 
                                              [File("Old2.txt", str_to_datetime("10 years ago")), 
                                               File("New2.txt", str_to_datetime("10 days ago")),
                                               Directory("test_2", [File("Old3.txt", str_to_datetime("31 days ago")),
                                                                    File("New3.txt", str_to_datetime("29 days ago"))])]), 
                                    File("New1.txt", str_to_datetime("5 days ago")),
                                    File("Old1.txt", str_to_datetime("5 years ago"))])

    Tree.create()

    mock = UserInputMocker(user_input_dict).patch(mocker)

    custom_checklist = copy.deepcopy(checklist_empty)

    custom_checklist["files"] = [{
            "question": "Question 1",
            "description": "Description 1",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "src": "./mock_files",
                    "description": "Directory 1 Description",
                    "until": "30 days ago"
                }
            ]
        }]        
    
    app = ArchivingTestApp(custom_checklist)
    actual_archived_paths = app.run()

    assert mock.isSuccess()

    assert_lists_identical(expected_archived_paths, actual_archived_paths)

    Tree.delete()

def test_checklist_hours_filter(mocker):
    user_input_dict = [("Question 1" , "Y")]

    expected_archived_paths = ["./mock_files/New1.txt"]

    # Generate Tree
    Tree = Directory("mock_files", [File("New1.txt", str_to_datetime("60 minutes ago"))])

    Tree.create()

    mock = UserInputMocker(user_input_dict).patch(mocker)

    custom_checklist = copy.deepcopy(checklist_empty)

    custom_checklist["files"] = [{
            "question": "Question 1",
            "description": "Description 1",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "src": "./mock_files",
                    "description": "Directory 1 Description",
                    "until": "1 hour ago"
                }
            ]
        }]        
    
    app = ArchivingTestApp(custom_checklist)
    actual_archived_paths = app.run()

    assert mock.isSuccess()

    assert_lists_identical(expected_archived_paths, actual_archived_paths)

    Tree.delete()