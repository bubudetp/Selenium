import re

def split_string_by_add(str):
    new_str = ""
    split = str.split()
    for char in split:
        if char == ":":
            new_str += "-+"
        else:
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


def extract_number_from_anime_title(title, anime_name):
    # Remove the anime name from the title
    title.lower()
    remainder = title.replace(anime_name, "").strip()
    match = re.search(r"\d+", remainder)
    return int(match.group()) if match else None
