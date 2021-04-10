
from .models import *
from .summarizer import *
from .question_generation.pipelines import pipeline
from random import randint

nlp = pipeline("question-generation")


def make_questions(snippet):
    '''
    :param snippet: A snippet object which will have Topic, Content
    Using the content of the snippet, generate some questions
    :return: The list of Question Objects generated for snippet
    '''

    snippet_text = snippet.content
    snippet_title = snippet.title

    print(snippet_text)

    json_result = nlp(snippet_text)

    print(json_result)

    # Make 4 lists 1.questions 2.options 3.answers 4.Time using snippet_text
    # See Following Example
    qno = []  # ['Q1', 'Q2']
    questions = []   # ['XYZ', 'PQR']
    options = []     # ['1,2,3,4', '1,2,3,4']
    answers = []     # ['1', '4']
    time = []        # [10, 12]

    for idx, qa_pair in enumerate(json_result):
        qno.append("Q" + str(idx + 1))
        questions.append(qa_pair["question"])
        wrong_options = ['Wrong1', 'Wrong2', 'Wrong3', 'Wrong4']
        idx = randint(0, 3)
        opt_temp = wrong_options
        opt_temp[idx] = qa_pair["answer"]
        options.append(str(opt_temp))
        answers.append(str(idx))
        time.append(20)

    questions_object_list = []

    for x in range(len(questions)):
        new_question = Question.objects.create(content=questions[x], options=options[x], max_time=time[x], correct_option=answers[x])
        new_question.save()
        questions_object_list.append(new_question)

    return questions_object_list

def parse_question(question):
    question_dict = {'maxTimeSec': question.max_time, 'content': question.content}

    options_list = []
    options_split_list = question.options.split(',')

    for option in options_split_list:
        option_dict = {'correct': False, 'content': option}

        if option == question.correct_option:
            option_dict['correct'] = True
        options_list.append(option_dict)

    question_dict['options'] = options_list
    return question_dict

