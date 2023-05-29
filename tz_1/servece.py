import datetime

import requests

import db.db_func as db_func

def get_questions(questions_num):
    response = requests.get(f'https://jservice.io/api/random?count={questions_num}')
    if response.status_code == 200:
        Question_class = Question_compostit()
        count, last = Question_class.fabric_raw_json(response.json())
        return count, last
    
class Question_compostit():
    def __init__(self):
        self.questions = []
        self.ids = []
        self.get_ids()

    def get_ids(self):
        self.ids = db_func.get_ids()
        

    def save_questions(self):
        with db_func.make_session() as session:
            session.add_all(self.questions)
            session.commit()
        self.questions = []



    def fabric_raw_json(self, raw):
        re_request_count = 0
        for request_question in raw:
            if request_question['id'] in self.ids:
                re_request_count += 1
            else:
                new_question = db_func.Question(
                    id=int(request_question['id']),
                    text_question=request_question['question'],
                    answer=request_question['answer'],
                    created_at=datetime.datetime.strptime(request_question['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    )
                self.questions.append(new_question)
        self.save_questions()
        self.get_ids()
        last = raw[-1]['question']
        return re_request_count, last
        
