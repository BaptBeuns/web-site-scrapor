#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 tonio <tonio@father>
#
# Distributed under terms of the MIT license.

import re, codecs, sys, json, time
import utils.scrap as uScrap
from collections import defaultdict
from pprint import pprint


def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    # filter removes possible Nones in texts and tails
    return tostring(node, encoding='unicode', method='text')
    # return ''.join(filter(None,[n.text for n in node.getiterator()]))
    return ''.join(filter(None, parts)).strip()
    parts = (
                list(chain(*([c.text, tostring(c, encoding='utf-8'), c.tail] for c in node.getchildren()))) +
                [node.tail])

def execute_action_tree(soup, actions_list, output=defaultdict(list), level=0):
    if not isinstance(actions_list, list):
        actions_list = [actions_list]

    for actions in actions_list:
        action_type = actions['type']

        if action_type == 'get':
            soups = soup.xpath(actions['which'])
            if not isinstance(soups, list):
                soups = [soups]
            for sub_soup in soups:
                if 'on_item' in actions:
                    output['current_element'] = sub_soup
                    execute_action_tree(sub_soup, actions['on_item'], output, level=level+1)

        elif action_type == 'retrieve-html':
            url = actions['url'].format(**output)
            print("Scraping {}...".format(url))
            soup = uScrap.make_soup(url)
            execute_action_tree(soup, actions['on_item'], output, level=level+1)

        elif action_type == 'iterate':
            if actions['in'] == 'list':
                for item in output[actions['which']]:
                    output[actions['which'] + "_current"] = item
                    try:
                        execute_action_tree(item, actions['on_item'], output, level=level+1)
                    except:

                        print('Skip this one...')
            if actions['in'] == 'range':
                start = actions['start']
                end = actions['end']
                if isinstance(start, unicode):
                    start = int(output[start])
                if isinstance(end, unicode):
                    end = int(output[end])
                for item in range(start, end+1):
                    item = str(item)
                    output[actions['which'] + "_current"] = item
                    execute_action_tree(item, actions['on_item'], output, level=level+1)

        elif action_type == 'store' or action_type == 'display':
            if 'what' not in actions:
                element = soup
            elif actions['what'] == 'from-list':
                element = output[actions['list']]
            elif actions['what'] == 'stringify-children':
                element = stringify_children(soup)
            elif actions['what'] == 'attrib-regex':
                attrib = soup[actions['which']]
                element = re.search(actions['regex'], attrib).groups()[0]
            elif actions['what'] == 'format':
                element = actions['format'].format(**output)

            if action_type == 'display':
                print(element)
            elif action_type == 'store':
                if actions['kind'] == 'list':
                    output[actions['where']].update([element])
                elif actions['kind'] == 'value' or actions['kind'] == 'numeric':
                    output[actions['where']] = element
                elif actions['kind'].split(' ')[0] == 'nth-last-child':
                    index = int(actions['kind'].split(' ')[1])
                    if len(element) > index:
                        output[actions['where']] = list(element.children)[-index].string

        elif action_type == 'create':
            if actions['kind'] == 'range':
                output[actions['where']] += range(int(output[actions['from']]), int(output[actions['to']]))

def Scrapor(input_file, output_file=None):
    # Loading the script
    with open(input_file) as f:
        script = json.load(f)

    # Executing along the tree
    soup = uScrap.make_soup(script['start_url'])
    output = defaultdict(set)
    TTT = time.time()
    t = execute_action_tree(soup, script['actions'], output)

    # Writing output to stdout
    print output
    output_text = u"\n".join(output['celeb'])

    # Writing output to file, specified or not
    if not output_file:
        output_file = "output/" + input_file.split('/')[-1].split('.')[0] + ".csv"
    with codecs.open(output_file, 'w', encoding='utf-8') as f:
        print(output_text)
        f.write(output_text)

    print "Took %s seconds" % (time.time() - TTT)

if __name__=="__main__":
    input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = None
    Scrapor(input_file, output_file)
