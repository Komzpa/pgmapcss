def stat_all_scale_denominators(stat):
    return sorted(list(set([
            v['selectors']['min_scale']
            for v in stat['statements']
        ] + \
        [
            v['selectors']['max_scale']
            for v in stat['statements']
            if v['selectors']['max_scale'] != None
        ])),
        reverse=True)

def stat_properties(stat):
    return list(set([
        p['key']
        for v in stat['statements']
        for p in v['properties']
        if p['assignment_type'] == 'P'
    ]))

def stat_property_values(prop, stat, include_illegal_values=False):
    """Returns set of all values used on this property in any statement.
    Returns boolean 'True' if property is result of an eval expression."""
    values = {
        True if p['value_type'] == 'eval' else p['value']
        for v in stat['statements']
        for p in v['properties']
        if p['assignment_type'] == 'P' and p['key'] == prop
    }

    if include_illegal_values:
        return values

    if 'values' in stat['defines'] and prop in stat['defines']['values']:
        allowed_values = stat['defines']['values'][prop]['value'].split(';')

        if True in values:
            values = values + allowed_values

        values = {
            v if v in allowed_values else allowed_values[0]
            for v in values
        }

    values = {
        v
        for v in values
        if v != None
    }

    return values