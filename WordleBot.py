from WordList import FULL_LIST
import pandas as pd
from collections import defaultdict
import copy

original_df = pd.DataFrame(data={'word': FULL_LIST})
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def count_letters(filtered_df):
    def def_value():
        return 0

    letter_dict = defaultdict(def_value)

    for letter in ALPHABET:
        letter_dict[letter] = filtered_df['word'].apply(lambda x: int(letter in x)).sum()

    # for item in filtered_df['word'].values:
    #     for letter in item:
    #         letter_dict[letter] += 1

    return letter_dict


def get_word_value(word, letter_dict):
    value = 0
    last_letter = '_'
    for letter in sorted(word):
        if letter != last_letter:
            value += letter_dict[letter]
            last_letter = letter
    return value


def add_rule(word, result, current_df):
    """incorrect letters are X
    G for letters in green
    Y for letters in yellow
    example: word = 'crane', result = 'XYYBG'
    """

    # Fix words
    word = word.lower()
    result = result.upper()

    g_li, y_li, x_li = [], [], []

    # Reorder indexes, checking green letters first
    for idx, letter in enumerate(result):
        if letter == 'G':
            g_li.append(idx)
        elif letter == 'Y':
            y_li.append(idx)
        else:
            x_li.append(idx)

    loop_li = g_li + y_li + x_li

    # Loop through and reduce dataframe
    green_letter_li = []
    for idx in loop_li:
        value = word[idx]
        if result[idx] == 'G':
            green_letter_li.append(value)
            current_df = current_df[current_df['word'].str[idx] == value]

        elif result[idx] == 'Y':
            current_df = current_df[(current_df['word'].str.contains(value)) &
                                    (current_df['word'].str[idx] != value)]

        elif result[idx] == 'X':
            if value not in green_letter_li:
                current_df = current_df[~current_df['word'].str.contains(value)]
            else:
                current_df = current_df[(current_df['word'].str[idx] != value)]

        else:
            raise ValueError('Results should only contain G, Y, and X')

    return current_df


def filter_df(word, result, dataframe):
    adj_df = add_rule(word, result, dataframe)
    word_dict = count_letters(adj_df)
    adj_df['value'] = adj_df['word'].apply(lambda x: get_word_value(x, word_dict))

    original_df['value'] = original_df['word'].apply(lambda x: get_word_value(x, word_dict))

    return adj_df, original_df


if __name__ == '__main__':
    df = copy.deepcopy(original_df)

    df, orig = filter_df('crane', 'GXXYX', df)
    df, orig = filter_df('conic', 'GXGYY', df)
    print(len(df))
    print(df.sort_values('value', ascending=False).head(10))
