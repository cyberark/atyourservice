from nurse import nurse, checklistjson, blank_archiver, asciicolors, list_archiver

def assert_lists_identical(expected_list, actual_list):
    for expected_path in expected_list:
        assert expected_path in actual_list

    for actual_path in actual_list:
        assert actual_path in expected_list
class UserInputMocker(object):
    def __init__(self, value):
        self.value = value

    def _remove_colors(self, mocker):
        for attr in dir(asciicolors):
            # skip internal
            if callable(getattr(asciicolors, attr)) or str(attr).startswith("__"):
                continue

            mocker.patch.object(asciicolors, attr, "")

    def isSuccess(self):
        return len(self.value) == 0

    def patch(self, mocker):
        self._remove_colors(mocker)
        mocker.patch('nurse._get_user_input', side_effect=self._get_user_input_mock)
        return self

    def _get_user_input_mock(self, prompt, prefill):
        prompt = prompt.replace("-> ", "")

        # assert priority
        expected_question = self.value[0][0]
        assert expected_question == prompt

        user_answer = self.value[0][1]

        # it will not be called again
        del self.value[0]

        return user_answer

class TestApp(object):
    def __init__(self, checklist):
        self.config = checklistjson("")

        # it is expected from the checklistjson class that this is not to be deepcopy(), so it can still be modified from outside
        self.config.set_value(checklist)

    def run(self):
        n = nurse(self.config, archiver=blank_archiver, dry_run=False)
        for item in n.checklist():
            item.perform(dry_run=False)

# this needs to be defined to disable pytest running this class as a test
TestApp.__test__ = False

class ArchivingTestApp(object):
    def __init__(self, checklist):
        self.config = checklistjson("")

        # it is expected from the checklistjson class that this is not to be deepcopy(), so it can still be modified from outside
        self.config.set_value(checklist)

    def run(self):
        n = nurse(self.config, archiver=list_archiver, dry_run=False)

        for item in n.checklist():
            item.perform(dry_run=False)
        
        return n.archiver.get_paths()
        
ArchivingTestApp.__test__ = False