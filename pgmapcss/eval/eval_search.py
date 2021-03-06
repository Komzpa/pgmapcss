def eval_search(param):
    if len(param) < 2:
        return ''

    l = param[0].split(';')

    try:
        return str(l.index(param[1]))
    except ValueError:
        return 'false'

# TESTS
# IN ['pizza;kebab;noodles', 'pizza']
# OUT '0'
# IN ['pizza;kebab;noodles', 'noodles']
# OUT '2'
# IN ['pizza;kebab;noodles', 'burger']
# OUT 'false'
