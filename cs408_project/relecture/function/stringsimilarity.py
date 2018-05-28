import jellyfish
import re


def get_text_list(text_file):
    file = open(text_file, "r")
    count = -1
    text_list = []
    for line in file:
        indicator = '%s,"' % (count + 1)
        if indicator == line[:len(indicator)]:
            count += 1
            text_list.append(line[3:])
        else:
            text = text_list[count]
            text += line
            text_list[count] = text
    return text_list


def get_intersection(a, b):
    s1 = set(a)
    s2 = set(b)
    result_set = s1.intersection(s2)
    final_list = list(result_set)
    return final_list


def get_difference(a, b):
    s1 = set(a)
    s2 = set(b)
    result_set = s2.difference(s1)
    final_list = list(result_set)
    return final_list


def token_set_ratio(old_text, new_text):
    old_text_list = re.findall(r"[\w']+", old_text)
    new_text_list = re.findall(r"[\w']+", new_text)

    if len(old_text_list) == 0 or len(new_text_list) == 0:
        return 0

    old_text_list = sorted(old_text_list)
    new_text_list = sorted(new_text_list)

    common_list = get_intersection(old_text_list, new_text_list)
    old_text_list_diff = get_difference(common_list, old_text_list)
    new_text_list_diff = get_difference(common_list, new_text_list)

    common_list = sorted(common_list)
    old_text_list_diff = sorted(old_text_list_diff)
    new_text_list_diff = sorted(new_text_list_diff)

    old_text_list = common_list + old_text_list_diff
    new_text_list = common_list + new_text_list_diff

    common_text_join = " ".join(str(x) for x in common_list)
    old_text_join = " ".join(str(x) for x in old_text_list)
    new_text_join = " ".join(str(x) for x in new_text_list)

    r1 = 100 - jellyfish.levenshtein_distance(common_text_join, old_text_join) / len(old_text_join) * 100
    r2 = 100 - jellyfish.levenshtein_distance(common_text_join, new_text_join) / len(new_text_join) * 100
    r3 = 100 - jellyfish.levenshtein_distance(old_text_join, new_text_join) / max(len(old_text_join),
                                                                                  len(new_text_join)) * 100

    result = max(r1, r2, r3)

    return round(result, 1)


def get_ratio(text_list):
    old_text = ""
    result_list = []

    first_page = True
    for text in text_list:
        if not first_page:
            result = token_set_ratio(old_text, text)
            result_list.append(result)
        else:
            first_page = False
        old_text = text

    return result_list


def get_string_similarity(text_file):
    text_list = get_text_list(text_file)
    result = get_ratio(text_list)
    return result
