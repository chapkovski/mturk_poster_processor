"""Module retrieves assignment answers and stores them in a csv"""
from client import get_client, get_balance
from pprint import pprint
from process_answer import get_answer
import pandas as pd
import csv, sys
import json

retrievable_keys = ['AssignmentId','WorkerId','HITId','SubmitTime','AcceptTime']
def get_results_from_hit(HITId, resulting_file):
    fieldnames = None
    res = []
    client = get_client(sandbox=False)


    token = ' '

    params = dict(HITId=HITId)
    while token:
        if token and len(token) > 1:
            params.update(dict(NextToken=token))
        resp = client.list_assignments_for_hit(**params)

        token = resp.get('NextToken')
        assignments = resp.get('Assignments')

        for i in assignments:
            answer = get_answer(i.get('Answer'))

            assignment_extra_data ={j:i.get(j) for j in retrievable_keys }

            answer.update(assignment_extra_data)
            res.append(answer)
    if len(res) > 0:
        fieldnames = []
        for i in res:
            fieldnames.extend(i.keys())

        fieldnames = list(set(fieldnames))

        with open(resulting_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(resulting_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for i in res:
            print(i)
            writer.writerow(i)


if __name__ == '__main__':
    HITId = '33W1NHWFYI7TU50J3NV27GIVCTNTZ5'
    resulting_file = './logs/results3.csv'
    get_results_from_hit(HITId, resulting_file)
