import pytest
from .checklists import *
from .common import UserInputMocker, TestApp

def test_checklist_no_questions(mocker):
    user_input_dict = {}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_no_questions)
    app.run()

    assert mock.isSuccess()

def test_checklist_numerous_followups(mocker):
    user_input_dict = {"Question 1" : "Y",
                       "Followup 1" : "Y", 
                       "Followup 2" : "Y", 
                       "Followup 3" : "Y",
                       "Followup of Followup 3" : "Y"}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_numerous_followups)
    app.run()

    assert mock.isSuccess()

def test_checklist_nested_followups(mocker):
    user_input_dict = {"Question 1" : "Y",
                       "Followup 1" : "Y", 
                       "Followup 2" : "Y", 
                       "Followup 3" : "Y"}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_nested_followups)
    app.run()

    assert mock.isSuccess()