def eval_translate(param):
    if len(param) == 0:
        return ''
    if len(param) < 3:
        return param[0]

    x = to_float(eval_metric([param[1], 'u']))
    y = to_float(eval_metric([param[2], 'u']))

    plan = plpy.prepare('select ST_Translate($1, $2, $3) as r', ['geometry', 'float', 'float'])
    res = plpy.execute(plan, [param[0], x, y ])

    return res[0]['r']

# TESTS
# IN ['010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641', '0', '0']
# OUT '010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641'
# IN ['010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641', '2px', '2u']
# OUT '010300002031BF0D000100000004000000DA1AB6822452354185EB51383FAE5641EFC8FDA3245235413D0AD75340AE5641552F640A29523541000000303FAE5641DA1AB6822452354185EB51383FAE5641'
