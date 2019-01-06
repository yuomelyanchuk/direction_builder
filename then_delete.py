import configparser


config = configparser.ConfigParser();

config.read('init')

config

for k, v in config.items():
    print(k, v)


init = {}

import json

init['name'] = 'wine'
init['host'] = 'localhost'
init['port'] = '5672'
init['type'] = 'check purchase'
init['listen_queue'] = ['input']
init['yes_section'] = {'send_message': ['chees'], 'message': 'wine;section true'}
init['no_section'] = {'send_message': ['reco-wine'], 'message': 'wine;section false'}
init['always_section'] = {'send_message': ['message1'], 'message': 'wine;section always'}

if init.get('yes_section',''):


init

with open('init.json', 'w') as fp:
    json.dump(init, fp,  indent=4)

with open('init.json', 'r') as fp:
    init = json.load(fp)


init.listen_queue


listen_queue = init.get('listen_queue', '')

type(init['listen_queue'])


type(init)



a={'a':'b','c':'d'}

json.dumps(a)

json.loads()

edge=[]

import csv

vertices_path = "./routing_graph/edge.csv"

with open(vertices_path) as infile:
    reader = csv.DictReader(infile, delimiter=';')
    for row in reader:
        edge.append(row)


edge[0]

sss = dict(vertices[])

vertices[0].get('worker_name')

type(row)

row.get('worker_name')