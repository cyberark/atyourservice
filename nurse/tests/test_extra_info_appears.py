import pytest
from nurse import nurse, blank_archiver, checklistjson, asciicolors, NO_DESCRIPTION_MESSAGE
from .checklists import checklist_1
from .common import UserInputMocker

class UserInputExtraInfoMocker(UserInputMocker):
    def _get_user_input_mock(self, prompt, prefill):
        prompt = prompt.replace("-> ", "")

        # assert priority
        expected_question = list(self.value.keys())[0]
        assert expected_question in prompt

        info = self.value[expected_question]

        for text in info["expected_text"]:
            assert text in prompt

        user_answer = info["user_input"]

        # it will not be called again
        del self.value[expected_question]

        return user_answer

class ExtraInfoTestApp(object):
    def __init__(self, checklist):
        self.config = checklistjson("")

        # it is expected from the checklistjson class that this is not to be deepcopy(), so it can still be modified from outside
        self.config.set_value(checklist)

    def run(self):
        n = nurse(self.config, archiver=blank_archiver, dry_run=False)
        for item in n.checklist():
            # the prompts will contain extra information from the description
            item.print_extra_info()
            item.perform(dry_run=False)

ExtraInfoTestApp.__test__ = False

def test_all_questions_asked_with_extra_info(mocker):
    user_input_dict = {"Question 7" : {"expected_text": ["Description 7"], "user_input": "Y"},
                       "Question 1" : {"expected_text": ["Description 1"], "user_input": "Y"}, 
                       "Followup to Question 1" : {"expected_text": [NO_DESCRIPTION_MESSAGE], "user_input": "Y"}, 
                       "Followup to Followup Question 1": {"expected_text": ["Description 20"], "user_input": "Y"}, 
                       "Question 8" : {"expected_text": ["Description 8"], "user_input": "Y"},
                       "Followup to Question 8" : {"expected_text": ["Followup Description 8"], "user_input": "Y"},
                       "Question 9" : {"expected_text": ["Description 9"], "user_input": "Y"},
                       "Question 10" : {"expected_text": [NO_DESCRIPTION_MESSAGE], "user_input":"Y"},
                       "Question 4" : {"expected_text": ["Command 1 Description"], "user_input": "Y"},
                       "Question 5" : {"expected_text": ["Command 2 Description", "Command 3 Description"], "user_input": "Y"},
                       "Question 2" : {"expected_text": ["Description 2"], "user_input": "Y"},
                       "Question 3" : {"expected_text": ["Description 3"], "user_input": "Y"},
                       "Question 6" : {"expected_text": ["Description 6"], "user_input": "Y"}}

    mock = UserInputExtraInfoMocker(user_input_dict).patch(mocker)
    
    app = ExtraInfoTestApp(checklist_1)
    checklist_1["configuration"]["defaults"]["priority"] = 100
    app.run()

    assert mock.isSuccess()
