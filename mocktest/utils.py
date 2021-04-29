import json
from mocktest import db
from mocktest.models import Java, Python

def add_questions_java():
    question_entries = []
    list_files = ['Classes_Methods','Data_Types_Variables_Arrays','Exception','Inheritance','Operators_Control_Statements','Threads']

    for file_name in list_files:
        with open(f'mocktest/static/questions/Java/{file_name}.json') as f:
            data = json.load(f)
        
        for question in data["quiz"]:   
            if(len(question['options']) == 4):
                new_question = Java(question_id=question['id'],
                                        subject=question['subject'],
                                        module=question['module'],
                                        question=question['question'],
                                        answer=question['answer'],
                                        reason=question['reason'],
                                        optiona=question['options'][0]['a'],
                                        optionb=question['options'][1]['b'],
                                        optionc=question['options'][2]['c'],
                                        optiond=question['options'][3]['d']) 
            else:
                new_question = Java(question_id=question['id'],
                                        subject=question['subject'],
                                        module=question['module'],
                                        question=question['question'],
                                        answer=question['answer'],
                                        reason=question['reason'],
                                        optiona=question['options'][0]['a'],
                                        optionb=question['options'][1]['b'])                      
            question_entries.append(new_question)
        db.session.add_all(question_entries)
        db.session.commit()

def add_questions_python():
    question_entries = []
    list_files = ['Python_Basics','List','Loops','Strings','Tuples_Sets','Regular_Expression_Files']

    for file_name in list_files:
        with open(f'mocktest/static/questions/Python/{file_name}.json') as f:
            data = json.load(f)
        for question in data["quiz"]:   
            if(len(question['options']) == 4):
                new_question = Python(question_id=question['id'],
                                        subject=question['subject'],
                                        module=question['module'],
                                        question=question['question'],
                                        answer=question['answer'],
                                        reason=question['reason'],
                                        optiona=question['options'][0]['a'],
                                        optionb=question['options'][1]['b'],
                                        optionc=question['options'][2]['c'],
                                        optiond=question['options'][3]['d']) 
            else:
                new_question = Python(question_id=question['id'],
                                        subject=question['subject'],
                                        module=question['module'],
                                        question=question['question'],
                                        answer=question['answer'],
                                        reason=question['reason'],
                                        optiona=question['options'][0]['a'],
                                        optionb=question['options'][1]['b'])                      
            question_entries.append(new_question)
        db.session.add_all(question_entries)
        db.session.commit()