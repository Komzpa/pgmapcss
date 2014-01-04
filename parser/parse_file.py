from .parse_defines import parse_defines
from .parse_selectors import parse_selectors
from .parse_properties import parse_properties
from .strip_comments import strip_comments
import re

def parse_file(stat, file):
    content = open(file).read()
    stat['statements'] = []
    stat['defines'] = {}

    to_parse = strip_comments(content)

# read statements until there's only whitespace left
    while not re.match('\s*$', to_parse):
        print(to_parse)
        to_parse = parse_defines(stat, to_parse)

        selectors = []
        to_parse = parse_selectors(selectors, to_parse)

        properties = []
        to_parse = parse_properties(properties, to_parse)

        for i in selectors:
            stat['statements'].append({
                'selectors': i,
                'properties': properties
            })

    return stat