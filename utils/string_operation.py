def split_string_by_add(str):
    new_str = ""
    split = str.split()
    for char in split:
        new_str += char + "+"

    new_str_len = len(new_str)
    return new_str[0: new_str_len - 1].lower()

def split_string_by_mid_dash(str):
    new_str = ""
    split = str.split()
    for char in split:
        new_str += char + "-"

    new_str_len = len(new_str)
    return new_str[0: new_str_len - 1].lower()
