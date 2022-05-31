#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import sys, traceback
import pwd
from zipfile import ZipFile
import json
import copy
from itertools import chain
import argparse
import readline
import subprocess
import sys, codecs, locale
import hashlib
import functools

### Constants ###
NO_DESCRIPTION_MESSAGE = "No additional information specified for this question."

class asciicolors:
    HEADER = '\033[95m'
    RED = '\033[31m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    @staticmethod
    def red(msg):
        return asciicolors.RED + msg + asciicolors.ENDC

    @staticmethod
    def blue(msg):
        return asciicolors.BLUE + msg + asciicolors.ENDC

    @staticmethod
    def cyan(msg):
        return asciicolors.CYAN + msg + asciicolors.ENDC

    @staticmethod
    def green(msg):
        return asciicolors.GREEN + msg + asciicolors.ENDC

    @staticmethod
    def underline(msg):
        return asciicolors.UNDERLINE + msg + asciicolors.ENDC

    @staticmethod
    def warning(msg):
        return asciicolors.WARNING + msg + asciicolors.ENDC

def string_to_delta(relative):
    #using simplistic year (no leap months are 30 days long.
    #WARNING: 12 months != 1 year
    unit_mapping = [('mic', 'microseconds', 1),
                    ('millis', 'microseconds', 1000),
                    ('sec', 'seconds', 1),
                    ('minute', 'seconds', 60),
                    ('hr', 'seconds', 3600),
                    ('hour', 'seconds', 3600),
                    ('day', 'days', 1),
                    ('week', 'days', 7),
                    ('mon', 'days', 30),
                    ('year', 'days', 365)]
    try:
        tokens = relative.lower().split(' ')

        # in case "ago" or "in" is not written, it will assume "ago" - which makes more sense in our case
        past = True
        if tokens[-1] == 'ago':
            past = True
            tokens =  tokens[:-1]
        elif tokens[0] == 'in':
            tokens = tokens[1:]


        units = dict(days = 0, seconds = 0, microseconds = 0)
        #we should always get pairs, if not we let this die and throw an exception
        while len(tokens) > 0:
            value = tokens.pop(0)
            if value == 'and':    #just skip this token
                continue
            else:
                value = float(value)

            unit = tokens.pop(0)
            
            match_success = False
            for match, time_unit, time_constant in unit_mapping:
                if unit.startswith(match):
                    units[time_unit] += value * time_constant
                    match_success = True
                    break
        
        if not match_success:
            raise Exception("Failed parsing {}, which is an unknown unit".format(unit))
        if past:
            return -datetime.timedelta(**units)
        return datetime.timedelta(**units)

    except Exception as e:
        raise Exception("Don't know how to parse %s: %s" % (relative, e))
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

class archiver(object):
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path

    def add(self, path, contents=None):
        pass

    def add_file(self, path, contents=None):
        pass

    def close(self):
        pass

    def is_writable(self, path):
        return True

class blank_archiver(archiver):
    def __init__(self, output_file_path):
        super(blank_archiver, self).__init__(output_file_path)

class list_archiver(archiver):
    def __init__(self, output_file_path):
        super(list_archiver, self).__init__(output_file_path)
        self.paths_list = []

    def add_file(self, path, contents=None, reduce=None):
        if reduce is not None and reduce(path):
            return
            
        self.paths_list += [path]

    def add_dir(self, path, reduce=None):
        for obj in os.listdir(path):
            full_path = os.path.join(path, obj)
            if os.path.isdir(full_path):
                self.add_dir(full_path, reduce)
            else:
                self.add_file(full_path, None, reduce)

    def add(self, path, contents=None, reduce=None):
        if contents is not None:
            self.add_file(path, contents=contents)
        else:
            if os.path.isdir(path):
                self.add_dir(path, reduce)
            else:
                self.add_file(path, None, reduce)
    
    def get_paths(self):
        return self.paths_list

class zip_archiver(list_archiver):
    def __init__(self, output_file_path):
        super(zip_archiver, self).__init__(output_file_path)
        self.zipped_file = ZipFile(output_file_path, 'w', allowZip64=True)

    def add_file(self, path, contents=None, reduce=None):
        if contents is not None:
            self.zipped_file.writestr(path, contents)
            return

        if reduce is not None and reduce(path):
            return
        self.zipped_file.write(path)
    
    def close(self):
        self.zipped_file.close()
    
    def is_writable(self, path):
        return os.access(path, os.W_OK)

def calculate_sha256(path):
    with open(path,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash

def _get_user_input(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        if sys.version_info[0] < 3:
            return raw_input(prompt)
        else:
            return input(prompt)  # or raw_input in Python 2
    finally:
        readline.set_startup_hook()

def get_user_input(prompt, prefill=''):
    COMMON_USER_CHOICE = {"n": "N", 
                          "no": "N",
                          "y": "Y", 
                          "ye": "Y", 
                          "yes": "Y"
                          }
    
    user_input = _get_user_input(prompt, prefill)
    if user_input.lower() in COMMON_USER_CHOICE:
        user_input = COMMON_USER_CHOICE[user_input.lower()]
    return user_input

class checklistjson(object):
    def __init__(self, path):
        self._path = path
        self._value = {}
        return

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path
        return

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        return

    def load(self):
        def _replace_tokens_with_envars(value):
            for var_key, var_value in os.environ.items():
                value = value.replace("<${}>".format(var_key), var_value)
            return value

        with open(self._path, 'r') as fd:
            try:
                # before loading the checklist.json as a JSON type, replace the <$TOKEN> with the corresponding environment variable
                self._value = json.loads(_replace_tokens_with_envars(fd.read()), strict=False)
            except json.decoder.JSONDecodeError as e:
                print(asciicolors.red("Error parsing {}: ".format(self._path) + str(e)))
                raise e
        return
    
    def save(self, override_path=None):
        if override_path is None:
            override_path = self._path

        with open(override_path, 'r') as fd:
            json.dump(self._value, fd, indent=4)
        return

    def copy(self, path=None):
        if path is None:
            new_inst = checklistjson(self._path)
        else:
            new_inst = checklistjson(path)

        new_inst.set_value(copy.deepcopy(self.get_value()))
        return new_inst
    
class action(object):
    """
    This class should be used as a base for actions. 
    
    The `perform` must be implemented for the new type, which will execute the corresponding action logic parsed from the checklist.json file. 
    """

    def __init__(self, configuration, data):
        self.data = data
        self.configuration = configuration
        self.silent = False
        self.extra_info = False

        if "priority" not in self.data:
            self.data["priority"] = self.configuration["defaults"]["priority"]

    def priority(self):
        return self.data["priority"]

    def keep_silent(self):
        # When there is no pre-defined `user` value, override it with the default value
        if len(self.data["answer"]["user"]) == 0:
            self.data["answer"]["user"] = self.data["answer"]["default"]
        self.silent = True

    def print_extra_info(self):
        self.extra_info = True

    def description(self):
        return ""

    def perform(self, dry_run=False):
        pass

    def get_user_answer(self):
        # check if user answer has already been filled out
        if self.data["answer"]["user"] != "" or self.silent:
            return
        
        if self.extra_info:
            self.data["question"] += "\n[{}]\n Enter input: ".format(self.description())

        if self.data["answer"]["user"] == "" or self.data["answer"]["user"] is None:
            self.data["answer"]["user"] = get_user_input(prompt=asciicolors.cyan("-> " + self.data["question"]), prefill=self.data["answer"]["default"])
            
            # if extra_info is off, when a user inputs "?", displays additional information just for this question
            if self.data["answer"]["user"] == "?" and not self.extra_info:
                # clear input so it re-asks when calling this function again
                self.data["answer"]["user"] = ""
                
                # enable extra_info and re-call this function. It will ask the question with additional info this time.
                self.print_extra_info()
                self.get_user_answer()
        else:
            self.data["answer"]["user"] = self.data["answer"]["default"]

    def _should_perform(self):
        return self.data["answer"]["user"] == self.data["answer"]["condition"]

    def __repr__(self):
        return str((self.data["question"], self.priority()))

    def __str__(self):
        return str((self.data["question"], self.priority()))

class question(action):
   def perform(self, previous_answer=None, dry_run=False):
        if not self._should_followup(previous_answer):
            return

        self.get_user_answer()

        #if dry_run:
            # Continue. Questions are supported in dry_run

        # Should the following question be asked?
        if self._should_perform() and "followup" in self.data:
            followup_questions_by_priority = sorted([question(self.configuration, obj) for obj in self.data["followup"]], key=lambda x: x.priority(), reverse=False)
            for q in followup_questions_by_priority:
                if self.silent:
                    q.keep_silent()                
                if self.extra_info:
                    q.print_extra_info()
                q.perform(previous_answer=self.data["answer"]["user"])

   def description(self):
       if "description" in self.data:
           return self.data["description"]
       else:
           return NO_DESCRIPTION_MESSAGE

   def _should_followup(self, previous_answer=None):
        if previous_answer is None:
           return True
        elif previous_answer is not None and "condition" not in self.data:
            return False
        elif previous_answer is not None and "condition" in self.data and previous_answer != self.data["condition"]:
            return False
        return True

   def _should_perform(self):
        # either the user answer or default answer kicked in
        return len(self.data["answer"]["user"]) > 0

class files_batch(action):
    def __init__(self, configuration, data, archive):
        super(files_batch, self).__init__(configuration, data)
        self.archive = archive

    def perform(self, dry_run=False):
        def is_not_acceptable(path, oldest_acceptable_time):
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(path)) 

            # subtract a second, in case they are very similar times - it's better to include than not
            if modified_time + datetime.timedelta(seconds=1) <= oldest_acceptable_time:
                return True
            return False
        
        self.get_user_answer()
        
        if dry_run:
            return

        # Should the files batch be retrieved?
        if self._should_perform():
            for path in self.data["paths"]:
                if not os.path.exists(path["src"]):
                    path["status"] = "Path Not Found"
                    continue
                try:
                    if "until" in path:
                        # calculate the oldest_acceptable_time from the string representation
                        oldest_acceptable_time = datetime.datetime.today() + string_to_delta(path["until"])

                        # implement lambda to reduce files which are older than the configured range (e.g. 20 days ago)
                        # the path["src"] may contain a parent directory while the file_path will be a specific file, thats why it is needed
                        reduce_old_files = lambda file_path: is_not_acceptable(file_path, oldest_acceptable_time)
                        self.archive.add(path["src"], reduce=reduce_old_files)
                    else:
                        self.archive.add(path["src"])
                    path["status"] = "Added"
                except Exception as e:
                    path["status"] = str(e)

    def description(self):
        description = ""
        if "description" in self.data:
            description = self.data["description"]

        for path in self.data["paths"]:
            if "description" in path:
                description += "\n{} - {}".format(path["src"], path["description"])
        
        if len(description) == 0:
            description = NO_DESCRIPTION_MESSAGE

        return description

class commands_batch(action):
    def __init__(self, configuration, data, archive):
        super(commands_batch, self).__init__(configuration, data)
        self.archive = archive

    def perform(self, dry_run=False):
        self.get_user_answer()
        
        if dry_run:
            return

        # Should the commands_batch be executed?
        if self._should_perform():
            for path in self.data["paths"]:
                try:
                    command_output = subprocess.check_output(path["command"], shell=True)
                    path["status"] = "Executed"

                    if "output_path" in path:
                        self.archive.add(path["output_path"], contents=command_output)
                    else:
                        path["output"] = str(command_output.decode()).split("\n")
                except Exception as e:
                    path["status"] = str(e)
                    continue
        return

    def description(self):
        description = ""
        if "description" in self.data:
            description = self.data["description"]

        for path in self.data["paths"]:
            if "description" in path:
                if len(description) > 0:
                    description += "\n"
                description += "{} - {}".format(path["command"], path["description"])
        
        if len(description) == 0:
            description = NO_DESCRIPTION_MESSAGE

        return description

class nurse(object):
    def __init__(self, readonly_checklistjson, archiver=zip_archiver, dry_run=False):
        # Objects in Python are passed by reference. The actions in this script act inplace. 
        self.checklistjson = readonly_checklistjson.copy()

        self.archive_path = os.path.join(self.checklistjson.get_value()["configuration"]["directory"], 
                                         "{}{}.zip".format(self.checklistjson.get_value()["configuration"]["prefix"],
                                                           datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%s")))

        os.environ["NURSE_ZIP_PATH"] = self.archive_path

        self.archiver = archiver(self.archive_path)
        
        # Check for write access
        if not self.archiver.is_writable(os.path.dirname(self.archive_path)):
            raise Exception("Error: Permission denied: {}".format(self.archive_path))
        self.dry_run = dry_run

        return

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        checklist_response = json.dumps(self.checklistjson.get_value(), cls=MyEncoder, indent=4)
        self.archiver.add("checklist_response.json", contents=checklist_response)

        # Save the currently running nurse.py to archive, if a file actually exists
        if '__file__' in globals():
            self.archiver.add(os.path.realpath(__file__))

        if self.dry_run:
            print("\nNo information is stored in a dry-run.")
        else:
            print("\nAll information has been successfully stored in {}".format(self.archive_path))

        self.archiver.close()

        if "end_message" in self.checklistjson.get_value()["configuration"]:
            print("\n{}".format(self.checklistjson.get_value()["configuration"]["end_message"]))

    def _questions_generator(self):
        for item in self.checklistjson.get_value()["questions"]:
            yield question(self.checklistjson.get_value()["configuration"], item)
    
    def _files_batch_generator(self):
        for item in self.checklistjson.get_value()["files"]:
            yield files_batch(self.checklistjson.get_value()["configuration"], item, self.archiver)
    
    def _commands_generator(self):
        for item in self.checklistjson.get_value()["commands"]:
            yield commands_batch(self.checklistjson.get_value()["configuration"], item, self.archiver)

    def introduce(self):
        if "begin_message" in self.checklistjson.get_value()["configuration"]:
            print("\n{}".format(self.checklistjson.get_value()["configuration"]["begin_message"]))

    def record(self, **kwargs):
        self.checklistjson._value["state"] = {}

        # override any previously stored state
        for k,v in kwargs.items():
            self.checklistjson._value["state"][k] = v

    def checklist(self):
        return sorted(chain(self._questions_generator(), self._files_batch_generator(), self._commands_generator()), key=lambda x: x.priority(), reverse=False)

class app_state(object):
        def __init__(self):
            self._info = {}
            self._exception_occured = False
            self._printable_exception_message = ""
            self.put(exception_occured="No")
            pass
        
        def get_exception_message(self):
            return self._printable_exception_message

        def has_exception_occured(self):
            return self._exception_occured

        def exception_occured(self):
            exc_type, exc_value, _ = sys.exc_info()
            exc_traceback = traceback.format_exc()
            self._exception_occured = True
            self.put(exception_occured="Yes", exception_type=str(exc_type), exception_msg=str(exc_value), exception_traceback=str(exc_traceback))
            self._printable_exception_message = "\n--Exception {} Start--\n{}\n--Exception End--\n".format(exc_type, exc_traceback)

        def info(self):
            return self._info

        def put(self, **kwargs):
            # override any previously stored state
            for k,v in kwargs.items():
                self._info[k] = v

class app(object):
    def __init__(self, args):
        self.args = args
        self.nurse = None
        self.state = app_state()

    def _initialize(self):
        if not (os.path.exists(self.args.path) and os.path.isfile(self.args.path)):
            print(asciicolors.red(asciicolors.underline("Error: Failed to find checklist.json in path {}. nurse.py requires it to work.".format(self.args.path))))
            raise Exception("Error: Failed to find checklist.json in path {}. nurse.py requires it to work.".format(self.args.path))

        self.config = checklistjson(self.args.path)
        self.config.load()

        chosen_archiver = zip_archiver

        if self.args.dry_run:
            chosen_archiver = blank_archiver

        self.nurse = nurse(self.config, archiver=chosen_archiver, dry_run=self.args.dry_run)
        
        nurse_sha256_calc = ""

        if '__file__' in globals():
            nurse_sha256_calc = calculate_sha256(os.path.realpath(__file__))

        # save in archive how nurse is executed
        self.nurse.record(args={arg:getattr(self.args, arg) for arg in vars(self.args)}, 
                          status=self.state.info(), 
                          nurse_sha256=nurse_sha256_calc,
                          checklist_sha256=calculate_sha256(self.args.path))

        if self.args.hash is not None:
            readable_hash = calculate_sha256(self.args.path)

            if readable_hash != self.args.hash:
                print(asciicolors.warning(asciicolors.underline("File Integrity Error: {} != {}".format(readable_hash, self.args.hash))))
                raise Exception("File Integrity Error: {} != {}".format(readable_hash, self.args.hash))
            else:
                print(asciicolors.green(asciicolors.underline("File Integrity Verified. Proceeding...\n")))
        else:
            print(asciicolors.warning(asciicolors.underline("File Integrity Not Verified. Use at your own descretion. Proceeding...\n")))

        if self.args.silent:
            print("Silent mode has been turned on. The configuration will be evaluated and an archive will be created accordingly.\n")
        else:
            print("Please answer all the questions below to help us diagnose the issue you're facing. An archive will be created based on your answers.\n")

    def open(self):
        print(asciicolors.GREEN + "{}\n".format("<>" * 30))
        print("""
    ███╗   ██╗██╗   ██╗██████╗ ███████╗███████╗    ██╗   ██╗ ██╗
    ████╗  ██║██║   ██║██╔══██╗██╔════╝██╔════╝    ██║   ██║███║
    ██╔██╗ ██║██║   ██║██████╔╝███████╗█████╗      ██║   ██║╚██║
    ██║╚██╗██║██║   ██║██╔══██╗╚════██║██╔══╝      ╚██╗ ██╔╝ ██║
    ██║ ╚████║╚██████╔╝██║  ██║███████║███████╗     ╚████╔╝  ██║
    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═══╝   ╚═╝                                             
        """)
        print("{}\n".format("<>" * 30) + asciicolors.ENDC)
        return self

    def __enter__(self):
        return self

    def prompt_save_before_exit(self, path_to_keep=None):
        if path_to_keep is None:
            return
        print(asciicolors.red("\nInterruption occured.\n"))
        user_input = get_user_input(asciicolors.cyan("-> Would you like to keep interrupted {} before exiting? [Y/n]".format(path_to_keep)), "Y")

        if user_input != "Y":
            os.remove(path_to_keep)
            print("Removed {}".format(path_to_keep))
        else:
            print("Keeping {}".format(path_to_keep))

    def __exit__(self, type, value, traceback):
        if type is not None:
            self.state.exception_occured()

            if not self.args.dry_run:
                try:
                    self.prompt_save_before_exit(os.getenv("NURSE_ZIP_PATH"))
                except:
                    pass
        
        if self.nurse is not None:
            self.nurse.__exit__(type, value, traceback)
        self.try_exit_gracefully()
    
    def try_exit_gracefully(self, success_exit_message=None):
        if self.state.has_exception_occured() and self.args.verbose:
            exit_message="An exception occured. Exiting."
        elif self.state.has_exception_occured() and not self.args.verbose:
            exit_message="An exception occured. Enable `--verbose` for more information. Exiting."
        elif success_exit_message != None:
            exit_message=success_exit_message
        else:
            exit_message="Nurse completed successfully"

        if self.args.verbose and self.state.has_exception_occured():
            print(self.state.get_exception_message())

        print("\n{}".format(exit_message))

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    def run(self):
        self._initialize()

        self.nurse.introduce()
        
        for item in self.nurse.checklist():
            if self.args.silent:
                # Use the default answer pre-configured in the checklist.json for the user's answers
                item.keep_silent()
            elif self.args.extra_info:
                item.print_extra_info()
            
            try:
                item.perform(dry_run=self.args.dry_run)
            except (KeyboardInterrupt, Exception) as e:
                self.state.exception_occured()
                raise e

def main():
    parser = argparse.ArgumentParser(description="Nurse utility: Information capturing tool using the corresponding configurable instructions located in a 'checklist.json' file.")
    parser.add_argument("-p", dest="path", default="checklist.json", help="path to the checklist.json configuration file")
    parser.add_argument("-hash", "--hash", dest="hash", help="verify with a corresponding sha256 hash of the checklist.json for security")
    parser.add_argument("-s", "--silent", dest="silent", action="store_true", help="use the pre-configured default answers from the checklist.json as the user's answers")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="print logs and additional information for troubleshooting the Nurse utility")
    parser.add_argument("-d", "--dry-run", dest="dry_run", action="store_true", help="run Nurse without saving any of the output")
    parser.add_argument("--extra-info", dest="extra_info", action="store_true", help="prints additional information on questions, files and commands")
    args = parser.parse_args()

    application = app(args)
    
    with application.open() as session:
        session.run()

if __name__ == "__main__":
    main()