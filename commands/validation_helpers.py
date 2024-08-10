def validate_params_count(params, count):
    if len(params) != count:
        raise ValueError(
            f'Invalid number of arguments. Expected: {count}; received: {len(params)}.")')
    
def location_from_string(value):
    if value not in ("SYD", "MEL", "ADL", "ASP", "BRI", "DAR", "PER"):
            raise ValueError(f"Location {value} not found.")
    return value

def try_parse_float(s):
    try:
        return float(s)
    except:
        raise ValueError('Invalid value for weight. Should be a number.')

def try_parse_int(s):
    try:
        return int(s)
    except:
        raise ValueError('Invalid value. Should be an integer.')