import pytest
from .checklists import checklist_empty
from .common import UserInputMocker, ArchivingTestApp, assert_lists_identical
import copy

def test_output_into_file(mocker):
    expected_archived_paths = ["a/b/c/echo_command.txt",
                               "b/c/d/python_command.txt"]

    user_input_dict = [("Question 1" , "Y")]

    mock = UserInputMocker(user_input_dict).patch(mocker)

    custom_checklist = copy.deepcopy(checklist_empty)

    custom_checklist["commands"] = [{
            "question": "Question 1",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "command": "echo 'Hello World!'",
                    "description": "Command 1 Description",
                    "output_path":"a/b/c/echo_command.txt"
                },
                {
                    "command": "python -c 'print(\"Hello World!\")'",
                    "description": "Command 2 Description",
                    "output_path":"b/c/d/python_command.txt"
                }
            ]
        }]
    
    app = ArchivingTestApp(custom_checklist)
    actual_archived_paths = app.run()

    assert_lists_identical(expected_archived_paths, actual_archived_paths)

    assert mock.isSuccess()

def test_output_into_file_and_inline(mocker):
    expected_archived_paths = ["b/c/d/python_command.txt"]

    user_input_dict = [("Question 1" , "Y")]

    mock = UserInputMocker(user_input_dict).patch(mocker)

    custom_checklist = copy.deepcopy(checklist_empty)

    custom_checklist["commands"] = [{
            "question": "Question 1",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "command": "echo 'Hello World!'",
                    "description": "Command 1 Description",
                },
                {
                    "command": "python -c 'print(\"Hello World!\")'",
                    "description": "Command 2 Description",
                    "output_path":"b/c/d/python_command.txt"
                }
            ]
        }]
    
    app = ArchivingTestApp(custom_checklist)
    actual_archived_paths = app.run()

    assert_lists_identical(expected_archived_paths, actual_archived_paths)

    assert mock.isSuccess()
