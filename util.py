import re
from unidecode import unidecode


def format_encrypted(text):
    return " ".join(text[i:i + 5] for i in range(0, len(text), 5))


def capitalize(match):
    return match.group().capitalize()


def denormalize(text, char_map):
    char_map_swapped = dict(zip(char_map.values(), char_map.keys()))
    for key in char_map_swapped.keys():
        text = text.replace(key, char_map_swapped[key])

    text = text.lower()
    text = text.capitalize()

    regex = re.compile(r'(?<=[.?!]\s)(\w+)')
    text = regex.sub(capitalize, text)

    return text


def normalize(text, char_map):
    text = text.upper()
    text = unidecode(text)
    pattern = r"[^A-Z]"
    match = re.findall(pattern, text)
    if match is None:
        return text
    else:
        char_set = set()

        for char in match:
            if char not in char_set:
                char_set.add(char)
                if char in char_map:
                    text = text.replace(char, char_map[char])
                else:
                    text = text.replace(char, "")

        return text


def gcd(a, b):
    if a < 1 | b < 1:
        raise Exception("Číslo a nebo b je menší než 1")
    while b != 0:
        temp = a
        a = b
        b = temp % b
    return a


def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
