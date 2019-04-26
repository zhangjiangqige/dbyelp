import re
import time
from pprint import pprint

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
            print_formatted_text('Wrong input.')
            continue

        if answer == 0:
            break
        if answer == 1:
            resp = requests.post(base_url + '/clean/restore').json()
            if resp['success'] == 1:
                print_formatted_text('Clean task finished successfully.')
            else:
                print_formatted_text('Task failed.')
        else:
            data = {
                'task': tasks[answer - 2]['name']
            }
            resp = requests.post(base_url + '/clean/run', data=data).json()
            if resp['success'] == 1:
                print_formatted_text('Clean task finished successfully.')
            else:
                print_formatted_text('Task failed.')


def split_data():
    resp = requests.post(base_url + '/validate/split').json()
    if resp['success'] == 1:
        print_formatted_text('Clean task finished successfully.')
    else:
        print_formatted_text('Task failed.')


parameters = {
    'review_count': [(0, 50), (50, 100), (100, float('inf'))],
    'fans': [(0, 1000), (1000, 2000), (2000, float('inf'))],
    'useful_prop': [(0, 10), (10, 15), (15, float('inf'))]
}


def set_params():
    while 1:
        print_formatted_text(HTML('''<ansiblue>Defaults are:
review_count: [(0, 50), (50, 100), (100, inf)],
fans: [(0, 1000), (1000, 2000), (2000, inf)],
useful_prop: [(0, 10), (10, 15), (15, inf)]
</ansiblue>'''))
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
            print_formatted_text('Wrong input.')
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
        print_formatted_text('Updated {}'.format(param_name))


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
            print_formatted_text('Wrong input.')
            continue
        if answer == 0:
            break
        elif answer == 1:
            set_params()
        else:
            pass



def test():
    pass


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
4) run the decision tree model
5) exit
'''))
        answer = prompt('>> ')
        try:
            answer = int(answer)
            assert 1 <= answer <= 5
        except:
            print_formatted_text('Wrong input.')
            continue

        funcs[answer]()



if __name__ == '__main__':
    init(False)
    base_url = 'http://{}:{}'.format(
        '127.0.0.1' if config.conf['host'] == '0.0.0.0' else config.conf['host'],
        config.conf['port'])
    print_formatted_text('Server is {}'.format(base_url))
    main()
