from .parse_defines import parse_defines
from .parse_selectors import parse_selectors
from .parse_properties import parse_properties
from .strip_comments import strip_comments
from .ParseFile import *

def parse_file(stat, file, base_style=None):
    if base_style:
        parse_file(stat, base_style)

    if not 'statements' in stat:
        stat['statements'] = []
        stat['defines'] = {}

    f = ParseFile(file)

    f.set_content(strip_comments(f))

# read statements until there's only whitespace left
    while not f.match('\s*$'):
        r = parse_defines(stat, f)
        if r and r[0] == 'import':
            parse_file(stat, r[1])

        selectors = []
        parse_selectors(selectors, f)

        properties = []
        parse_properties(properties, f)

        for i in selectors:
            statement = i.copy()
            statement['properties'] = properties
            stat['statements'].append(statement)

    return True