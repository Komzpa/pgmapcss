def eval_sort(param):
    if len(param) == 0:
        return ''

    l = param[0].split(';')

    l = sorted(l)

    return ';'.join(l)

# TESTS
# IN ['foo;bar']
# OUT 'bar;foo'
