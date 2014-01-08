import pgmapcss.db as db
import re
eval_param = ', object, current, render_context'

def valid_func_name(func):
    if re.match('[a-zA-Z_0-9]+$', func):
        return func

    else:
        raise Exception('Illegal eval function name: ' + func)

def compile_eval(value):
    global eval_param

    if type(value) == str:
        if value[0:2] == 'v:':
            return db.format(value[2:])
        elif value[0:2] == 'f:':
            return 'eval_' + valid_func_name(value[2:]) + '(\'{}\'' + eval_param + ')'
        else:
            raise Exception('compiling eval: ' + repr(value))

    if len(value) == 0:
        return ''

    if not value[0][0:2] in ('f:', 'o:'):
        return compile_eval(value[0])

    param = [ compile_eval(i) for i in value[1:] ]

    if value[0][0:2] == 'o:':
        conn = db.connection()
        res = conn.prepare('select * from eval_operators where op = $1')
        result = res(value[0][2:])
        if not len(result):
            raise Exception('compiling eval: unknown operator ' + result[0][2:])
        func = result[0]['func']

    elif value[0][0:2] == 'f:':
        func = value[0][2:]

    if func == 'cond':
        ret = '(CASE WHEN eval_boolean(Array[' + param[0] + ']' + eval_param + ') = \'true\' THEN ' + param[1]
        if len(param) > 2:
            ret += ' ELSE ' + param[2]
        ret += ' END)'
        return ret

    else:
        return 'eval_' + valid_func_name(func) + '(Array[' + ', '.join(param) + ']::text[]' + eval_param + ')'