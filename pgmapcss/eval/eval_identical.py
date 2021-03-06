def eval_identical(param):
    # empty parameter list -> all equal
    if len(param) == 0:
        return 'true'

    # identical comparison
    if len(param) != len(set(param)):
        return 'true'

    return 'false';

# TESTS
# IN ['5', '5']
# OUT 'true'
# IN ['5.0', '5', '3.00']
# OUT 'false'
# IN ['3', '5']
# OUT 'false'
# IN []
# OUT 'true'

