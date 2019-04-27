import re
import json
import time
from pprint import pprint, pformat

import requests
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import ProgressBar


from dbyelp import init
from utils import config


base_url = None


def clean_data():
    tasks = requests.get(base_url + '/clean/tasks').json()['tasks']
    tasks_str = ['''{}) {}
    <ansiblue>{}</ansiblue>'''.format(i + 2, t['name'], t['description']) for i, t in enumerate(tasks)]

    while 1:
        print_formatted_text(HTML('<ansiyellow>Enter the number of the clean task you want to execute, or 0 to go back:</ansiyellow>'))
        print_formatted_text(HTML('''0) go back to main menu
1) restore the data
{}
'''.format('\n'.join(tasks_str))))
        answer = prompt('>> ')
        try:
            answer = int(answer)
            assert 0 <= answer <= len(tasks_str) + 1
        except:
            print_formatted_text(HTML('<ansired>Wrong input</ansired>'))
            continue

        if answer == 0:
            break
        if answer == 1:
            resp = requests.post(base_url + '/clean/restore').json()
            if resp['success'] == 1:
                print_formatted_text(HTML('<ansired>Clean task finished successfully</ansired>'))
            else:
                print_formatted_text(HTML('<ansired>Task failed</ansired>'))
        else:
            data = {
                'task': tasks[answer - 2]['name']
            }
            resp = requests.post(base_url + '/clean/run', data=data).json()
            if resp['success'] == 1:
                print_formatted_text(HTML('<ansired>Clean task finished successfully</ansired>'))
            else:
                print_formatted_text(HTML('<ansired>Task failed</ansired>'))


def split_data():
    resp = requests.post(base_url + '/validate/split').json()
    if resp['success'] == 1:
        print_formatted_text(HTML('<ansired>Task finished successfully</ansired>'))
    else:
        print_formatted_text(HTML('<ansired>Task failed</ansired>'))


parameters = {
    'review_count': [(0, 50), (50, 100), (100, 9000), (9000, float('inf'))],
    'fans': [(0, 1000), (1000, 2000), (2000, 3000), (3000, float('inf'))],
    'useful_prop': [(0, 10), (10, 15), (15, 500), (500, float('inf'))]
}

parameters_default = {
    'review_count': [(0, 50), (50, 100), (100, 9000), (9000, float('inf'))],
    'fans': [(0, 1000), (1000, 2000), (2000, 3000), (3000, float('inf'))],
    'useful_prop': [(0, 10), (10, 15), (15, 500), (500, float('inf'))]
}


def set_params():
    while 1:
        print_formatted_text(HTML('''<ansiblue>Defaults are:
{}
</ansiblue>'''.format(pformat(parameters_default))))
        print_formatted_text(HTML('''<ansiyellow>Enter the number of action:</ansiyellow>
0) go back
1) show current parameters
2) change review_count
3) change fans
4) change useful_prop
'''))
        answer = prompt('>> ')
        try:
            answer = int(answer)
            assert 0 <= answer <= 4
        except:
            print_formatted_text(HTML('<ansired>Wrong input</ansired>'))
            continue
        if answer == 0:
            break
        actions = [
            None,
            lambda: pprint(parameters),
            lambda: update_params('review_count'),
            lambda: update_params('fans'),
            lambda: update_params('useful_prop')
        ]
        actions[answer]()


def update_params(param_name):
    global parameters
    valid = re.compile('\[(\(\d+,\d+\),)*\(\d+,(\d+|inf)\)\]')
    print_formatted_text(HTML('<ansiyellow>Enter new values for {}, e.g. [(0, 10), (10, inf)]:</ansiyellow>'.format(param_name)))
    answer = prompt('>> ').replace(' ', '')
    if valid.match(answer) == None:
        print('Wrong input.')
    else:
        answer = answer.replace('inf', 'float("inf")')
        parameters[param_name] = eval(answer)
        print_formatted_text(HTML('<ansired>Updated {}</ansired>'.format(param_name)))


def train():
    while 1:
        print_formatted_text(HTML('''<ansiyellow>Enter the number of action:</ansiyellow>
0) go back
1) set parameters
2) train the decision tree
'''))
        answer = prompt('>> ')
        try:
            answer = int(answer)
            assert 0 <= answer <= 2
        except:
            print_formatted_text(HTML('<ansired>Wrong input</ansired>'))
            continue
        if answer == 0:
            break
        elif answer == 1:
            set_params()
        else:
            data = {
                'params': json.dumps(parameters)
            }
            resp = requests.post(base_url + '/analyze/train', data=data).json()
            if resp['success'] == 1:
                print_formatted_text(HTML('<ansired>Training finished successfully</ansired>\n'))


def test():
    resp = requests.post(base_url + '/validate/validate').json()
    if resp['success'] == 1:
        print_formatted_text(HTML('<ansired>Average error of predicted number of stars: {}</ansired>\n'.format(resp['average_error'])))
    else:
        print_formatted_text(HTML('<ansired>Failed: {}</ansired>'.format(resp['msg'])))


def main():
    funcs = [
        None,
        clean_data,
        split_data,
        train,
        test,
        lambda: exit(0)
    ]
    while 1:
        print_formatted_text(HTML('''<ansiyellow>Enter the number of the action you want to do:</ansiyellow>
1) clean or restore the data
2) split the data into training and validation sets (this is going to take a while)
3) train the decision tree model
4) validate the decision tree model
5) exit
'''))
        answer = prompt('>> ')
        try:
            answer = int(answer)
            assert 1 <= answer <= 5
        except:
            print_formatted_text(HTML('<ansired>Wrong input</ansired>'))
            continue

        funcs[answer]()



if __name__ == '__main__':
    init(False)
    base_url = 'http://{}:{}'.format(
        '127.0.0.1' if config.conf['host'] == '0.0.0.0' else config.conf['host'],
        config.conf['port'])
    print_formatted_text('Server is {}'.format(base_url))
    main()
