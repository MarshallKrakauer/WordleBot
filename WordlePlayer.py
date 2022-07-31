from WordList import FULL_LIST
from WordleSolver import count_letters, get_word_value, add_rule, filter_df
import pandas as pd
import numpy as np
import random
from collections import defaultdict
import copy
import collections

original_df = pd.DataFrame(data={'word': FULL_LIST})
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def list_to_string(start_list):
    result_str = ''
    for x in start_list:
        result_str += x
    return result_str


def play_wordle(df, solution, guess_num, guess, noisy=True):
    result_li = ['_', '_', '_', '_', '_']
    solution_li = [letter for letter in solution]
    second_check_li = []

    # Check for Correct Letters
    for i in range(0, 5):
        if guess[i] == solution[i]:
            result_li[i] = 'G'
            solution_li[i] = '_'
        else:
            second_check_li.append(i)

    # Then check if letter is in remaining part of word
    for i in second_check_li:
        if guess[i] in solution:
            result_li[i] = 'Y'
        else:
            result_li[i] = 'X'

    df, _ = filter_df(guess, list_to_string(result_li), df)

    df.sort_values('value', ascending=False, inplace=True)
    df.reset_index(inplace=True, drop=True)
    next_guess = df.loc[0, 'word']

    if noisy:
        print( '~~~~~~~~~~~~~~~~~~~~',
              '\nsolution:', solution,
              '\nguess number:', guess_num,
              '\nguess:', guess,
              '\nresult:', result_li,
              '\nnext_guess:', next_guess,)

    if result_li != ['G', 'G', 'G', 'G', 'G']:
        return play_wordle(copy.deepcopy(df), solution, guess_num + 1, next_guess, noisy)
    else:
        if noisy:
            print('WINNER!!!!!!')
        return guess_num

if __name__ == '__main__':
    sample_solution = random.choice(FULL_LIST)
    guess_num_li = []
    loser_li = []
    for idx, word in enumerate(FULL_LIST):
        if idx % 200 == 0 and idx > 0:
            print('current word:', word)
        num_guesses = play_wordle(copy.deepcopy(original_df), word, 1, 'crane', False)
        if num_guesses > 6:
            loser_li.append(word)
        guess_num_li.append(num_guesses)

    guess_summary = collections.Counter(guess_num_li)
    guess_summary = sorted(guess_summary.items(), key=lambda i: i[0])
    print(guess_summary)
    print('losers:', loser_li)

    '''df = copy.deepcopy(original_df)

    df, orig = filter_df('crane', 'GXXYX', df)
    df, orig = filter_df('conic', 'GXGYY', df)
    print(len(df))
    print(df.sort_values('value', ascending=False).head(10))'''
