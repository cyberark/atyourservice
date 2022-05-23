checklist_1 = \
{
    "version": "2022-02-22",
    "configuration": {
        "directory": "<$HOME>",
        "prefix": "Diagnosis_",
        "defaults": {
            "priority": 100
        },
        "begin_message": "Begin Message",
        "end_message": "End Message"
    },
    "questions": [
        {
            "priority": 100,
            "question": "Question 1",
            "description": "Description 1",
            "answer": {
                "user": "",
                "default": "N"
            },
            "followup": [
                {
                    "condition": "Y",
                    "question": "Followup to Question 1",
                    "answer": {
                        "user": "",
                        "default": "Y"
                    },
                    "followup": [
                        {
                            "condition": "Y",
                            "question": "Followup to Followup Question 1",
                            "description": "Description 20",
                            "answer": {
                                "user": "",
                                "default": "Y"
                            },
                            "followup": []
                        }
                    ]
                }
            ]
        },
        {
            "priority": 200,
            "question": "Question 2",
            "description": "Description 2",
            "answer": {
                "user": "",
                "default": ""
            },
            "followup": []
        },
        {
            "priority": 500,
            "question": "Question 6",
            "description": "Description 6",
            "answer": {
                "user": "",
                "default": ""
            },
            "followup": []
        },
        {
            "question": "Question 8",
            "description": "Description 8",
            "answer": {
                "user": "",
                "default": ""
            },
            "followup": [
                {
                    "condition": "Y",
                    "question": "Followup to Question 8",
                    "description": "Followup Description 8",
                    "answer": {
                        "user": "",
                        "default": ""
                    },
                    "followup": []
                }
            ]
        },
        {
            "priority": 20,
            "question": "Question 7",
            "description": "Description 7",
            "answer": {
                "user": "",
                "default": ""
            },
            "followup": []
        }
    ],
    "files": [
        {
            "priority": 300,
            "question": "Question 3",
            "description": "Description 3",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "src": "/etc/redhat-release",
                    "description": "File 1 Description",
                },
                {
                    "src": "/etc/os-release",
                    "description": "File 2 Description",
                }
            ]
        },
        {
            "question": "Question 9",
            "description": "Description 9",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "src": "/etc/redhat-release",
                    "description": "File 1 Description",
                },
                {
                    "src": "/etc/os-release",
                    "description": "File 2 Description",
                }
            ]
        }
        
    ],
    "commands": [
        {
            "question": "Question 10",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "command": "pwd",
                }
            ]
        },
        {
            "question": "Question 4",
            "description": "Description 4",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "command": "pwd",
                    "description": "Command 1 Description",
                }
            ]
        },
        {
            "question": "Question 5",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "command": "pwd",
                    "description": "Command 2 Description",
                },
                {
                    "command": "pwd",
                    "description": "Command 3 Description",
                }
            ]
        }
    ]
}

checklist_no_questions = \
{
    "version": "2022-02-22",
    "configuration": {
        "directory": "<$HOME>",
        "prefix": "Diagnosis_",
        "defaults": {
            "priority": 100
        },
        "begin_message": "Begin Message",
        "end_message": "End Message"
    },
    "questions": [],
    "files": [],
    "commands": []
}

checklist_numerous_followups = \
{
    "version": "2022-02-22",
    "configuration": {
        "directory": "<$HOME>",
        "prefix": "Diagnosis_",
        "defaults": {
            "priority": 100
        },
        "begin_message": "Begin Message",
        "end_message": "End Message"
    },
    "questions": [ 
        {
            "priority": 100,
            "question": "Question 1",
            "description": "Description 1",
            "answer": {
                "user": "",
                "default": "N"
            },
            "followup": [
                {
                    "condition": "Y",
                    "question": "Followup 1",
                    "answer": {
                        "user": "",
                        "default": "Y"
                    },
                    "followup": []
                },
                {
                    "condition": "Y",
                    "question": "Followup 2",
                    "answer": {
                        "user": "",
                        "default": "Y"
                    },
                    "followup": []
                },
                {
                    "condition": "Y",
                    "question": "Followup 3",
                    "answer": {
                        "user": "",
                        "default": "Y"
                    },
                    "followup": [
                        {
                            "condition": "Y",
                            "question": "Followup of Followup 3",
                            "answer": {
                                "user": "",
                                "default": "Y"
                            },
                            "followup": []
                    }
                ]
                },
                {
                    "condition": "N",
                    "question": "Followup 4",
                    "answer": {
                        "user": "",
                        "default": "Y"
                    },
                    "followup": []
                }
            ]
        }],
    "files": [],
    "commands": []
}

checklist_nested_followups = \
{
    "version": "2022-02-22",
    "configuration": {
        "directory": "<$HOME>",
        "prefix": "Diagnosis_",
        "defaults": {
            "priority": 100
        },
        "begin_message": "Begin Message",
        "end_message": "End Message"
    },
    "questions": [ 
        {
            "priority": 100,
            "question": "Question 1",
            "description": "Description 1",
            "answer": {
                "user": "",
                "default": "N"
            },
            "followup": [
                {
                    "condition": "Y",
                    "question": "Followup 1",
                    "answer": {
                        "user": "",
                        "default": "Y"
                    },
                    "followup": [
                        {
                            "condition": "Y",
                            "question": "Followup 2",
                            "answer": {
                                "user": "",
                                "default": "Y"
                            },
                            "followup": [
                                {
                                    "condition": "Y",
                                    "question": "Followup 3",
                                    "answer": {
                                        "user": "",
                                        "default": "Y"
                                    },
                                    "followup": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }],
    "files": [],
    "commands": []
}

checklist_2 =  \
{
    "version": "2022-02-22",
    "configuration": {
        "directory": "<$HOME>",
        "prefix": "Diagnosis_",
        "defaults": {
            "priority": 100
        },
        "begin_message": "Begin Message",
        "end_message": "End Message"
    },
    "questions": [
        {
            "question": "Question 1",
            "description": "Description 1",
            "answer": {
                "user": "",
                "default": "Y"
            },
            "followup": [
                {
                    "condition": "Y",
                    "question": "Followup to Question 1",
                    "answer": {
                        "user": "",
                        "default": "Y"
                    },
                    "followup": [
                        {
                            "condition": "Y",
                            "question": "Followup to Followup Question 1",
                            "description": "Description 20",
                            "answer": {
                                "user": "",
                                "default": "Y"
                            },
                            "followup": []
                        }
                    ]
                }
            ]
        }
    ],
    "files": [
        {
            "question": "Question 2",
            "description": "Description 2",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "src": "/etc/redhat-release",
                    "description": "File 1 Description",
                },
                {
                    "src": "/etc/os-release",
                    "description": "File 2 Description",
                }
            ]
        }        
    ],
    "commands": [
        {
            "question": "Question 3",
            "answer": {
                "user": "",
                "default": "Y",
                "condition": "Y"
            },
            "paths": [
                {
                    "command": "pwd",
                    "description": "Command 1 Description",
                },
                {
                    "command": "pwd",
                    "description": "Command 2 Description",
                }
            ]
        }
    ]
}

checklist_empty =  \
{
    "version": "2022-02-22",
    "configuration": {
        "directory": "<$HOME>",
        "prefix": "Diagnosis_",
        "defaults": {
            "priority": 100
        },
        "begin_message": "Begin Message",
        "end_message": "End Message"
    },
    "questions": [],
    "files": [],
    "commands": []
}