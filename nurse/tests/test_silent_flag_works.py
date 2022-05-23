import pytest
from nurse import nurse, blank_archiver, checklistjson, asciicolors
from .checklists import *
from .common import UserInputMocker


class SilentTestApp(object):
    def __init__(self, checklist):
        self.config = checklistjson("")

        # it is expected from the checklistjson class that this is not to be deepcopy(), so it can still be modified from outside
        self.config.set_value(checklist)

    def run(self):
        n = nurse(self.config, archiver=blank_archiver, dry_run=False)

        for item in n.checklist():
            item.keep_silent()
            item.perform(dry_run=False)
        
SilentTestApp.__test__ = False

def test_checklist_silent_flag(mocker):
    # No input should have been entered
    user_input_dict = {}

    mock = UserInputMocker(user_input_dict).patch(mocker)
    
    app = SilentTestApp(checklist_2)
    app.run()

    assert mock.isSuccess()
