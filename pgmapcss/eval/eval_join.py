def eval_join(param):
    if len(param) < 2:
        return ''

    l = param[0].split(';')

    return param[1].join(l)

# TESTS
# IN ['restaurant;bar', ', ']
# OUT 'restaurant, bar'
