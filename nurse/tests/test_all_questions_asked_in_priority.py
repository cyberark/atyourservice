import pytest
from .checklists import checklist_1
from .common import UserInputMocker, TestApp

def test_all_questions_asked_in_order_priority_100(mocker):
    user_input_dict = {"Question 7" : "Y",
                       "Question 1" : "Y", 
                       "Followup to Question 1" : "Y", 
                       "Followup to Followup Question 1": "Y", 
                       "Question 8" : "Y",
                       "Followup to Question 8" : "Y",
                       "Question 9" : "Y",
                       "Question 10" : "Y",
                       "Question 4" : "Y",
                       "Question 5" : "Y",
                       "Question 2" : "Y",
                       "Question 3" : "Y",
                       "Question 6" : "Y",}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_1)
    checklist_1["configuration"]["defaults"]["priority"] = 100
    app.run()

    assert mock.isSuccess()

def test_all_questions_asked_in_order_priority_200(mocker):
    user_input_dict = {"Question 7" : "Y",
                       "Question 1" : "Y", 
                       "Followup to Question 1" : "Y", 
                       "Followup to Followup Question 1": "Y",      
                       "Question 2" : "Y",
                       "Question 8" : "Y",
                       "Followup to Question 8" : "Y",
                       "Question 9" : "Y",
                       "Question 10" : "Y",
                       "Question 4" : "Y",
                       "Question 5" : "Y", 
                       "Question 3" : "Y",
                       "Question 6" : "Y",}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_1)
    checklist_1["configuration"]["defaults"]["priority"] = 200
    app.run()

    assert mock.isSuccess()

def test_all_questions_asked_in_order_priority_50(mocker):
    user_input_dict = {"Question 7" : "Y",
                       "Question 8" : "Y",
                       "Followup to Question 8" : "Y",
                       "Question 9" : "Y",
                       "Question 10" : "Y",
                       "Question 4" : "Y",
                       "Question 5" : "Y",
                       "Question 1" : "Y", 
                       "Followup to Question 1" : "Y", 
                       "Followup to Followup Question 1": "Y",      
                       "Question 2" : "Y",
                       "Question 3" : "Y",
                       "Question 6" : "Y",}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_1)
    checklist_1["configuration"]["defaults"]["priority"] = 50
    app.run()

    assert mock.isSuccess()

def test_all_questions_asked_in_order_priority_10(mocker):
    user_input_dict = {"Question 8" : "Y",
                       "Followup to Question 8" : "Y",
                       "Question 9" : "Y",
                       "Question 10" : "Y",
                       "Question 4" : "Y",
                       "Question 5" : "Y",
                       "Question 7" : "Y",
                       "Question 1" : "Y", 
                       "Followup to Question 1" : "Y", 
                       "Followup to Followup Question 1": "Y",      
                       "Question 2" : "Y",
                       "Question 3" : "Y",
                       "Question 6" : "Y",}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_1)
    checklist_1["configuration"]["defaults"]["priority"] = 10
    app.run()

    assert mock.isSuccess()

def test_all_questions_asked_in_order_priority_300(mocker):
    user_input_dict = {"Question 7" : "Y",
                       "Question 1" : "Y", 
                       "Followup to Question 1" : "Y", 
                       "Followup to Followup Question 1": "Y",   
                       "Question 2" : "Y",  
                       "Question 8" : "Y",
                       "Followup to Question 8" : "Y",
                       "Question 3" : "Y",
                       "Question 9" : "Y",
                       "Question 10" : "Y",
                       "Question 4" : "Y",
                       "Question 5" : "Y",
                       "Question 6" : "Y",}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_1)
    checklist_1["configuration"]["defaults"]["priority"] = 300
    app.run()

    assert mock.isSuccess()

def test_all_questions_asked_in_order_priority_300_no_followup(mocker):
    user_input_dict = {"Question 7" : "Y",
                       "Question 1" : "N",
                       "Question 2" : "Y",  
                       "Question 8" : "N",
                       "Question 3" : "Y",
                       "Question 9" : "Y",
                       "Question 10" : "Y",
                       "Question 4" : "Y",
                       "Question 5" : "Y",
                       "Question 6" : "Y",}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = TestApp(checklist_1)
    checklist_1["configuration"]["defaults"]["priority"] = 300
    app.run()

    assert mock.isSuccess()