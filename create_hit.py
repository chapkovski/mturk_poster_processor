"""Module creates a HIT from a template and configuration stored in yaml file"""
from jinja2 import Environment, FileSystemLoader, Markup
from client import get_client
from pprint import pprint
import yaml
import sys

main_file_loader = FileSystemLoader('templates')
main_env = Environment(loader=main_file_loader)
template = main_env.get_template('template.xml')
# The following is needed just to check if xml is rendered correctly
# from lxml import etree
external_submit_live = 'https://www.mturk.com/mturk/externalSubmit'
external_submit_sandbox = 'https://workersandbox.mturk.com/mturk/externalSubmit'


def make_hit_from_template(html_file, context=dict(), hit_configuration='hit_configuration', sandbox=True):
    with open(f'./templates/{hit_configuration}.yaml') as file:
        hit_config = yaml.load(file, Loader=yaml.FullLoader)
    context['endpoint'] = external_submit_sandbox if sandbox else external_submit_live
    html_data = main_env.get_template(html_file).render(context)
    html_question = template.render(html_data=html_data)
    # this one is needed just to check that template was correctly rendered
    # etree.fromstring(html_question)
    # The following is just to quickly check up that template results in a correct html file
    with open("logs/__temp.html", "w") as file:
        file.write(html_data)

    hit_config['Question'] = html_question
    hit = get_client(sandbox=sandbox).create_hit(**hit_config)['HIT']
    return hit


if __name__ == '__main__':
    pprint(make_hit_from_template('phase_one.html', sandbox=False).get('HITId'))
