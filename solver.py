import pickle
import random

import pandas as pd


global init

init_flag = False


def init():
    global exempts, letters, solutions, attempts, count
    
    count = 0
    attempts = []
    
    with open('solutions.pkl', 'rb') as f:
        solutions = pickle.load(f)
    
    alphabet = [s for s in 'abcdefghijklmnopqrstuvwxyz']
    
    letters = {
        '1': alphabet,
        '2': alphabet,
        '3': alphabet,
        '4': alphabet,
        '5': alphabet
    }
    
    exempts = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': []
    }


def iteration(guess, code):
    global init_flag, attempts, solution, count, yellows, exemptions
        
    if not init_flag:
        print('yes')
        init()
        init_flag = True
        
    attempts.append(guess)

    yellows = []
    exemptions = []

    for i, colour in enumerate([s for s in code]):
        if colour == 'g':
            letters[str(i+1)] = guess[i]
        elif colour == 'y':
            exempts[str((i+1))] = guess[i]
            yellows.append(guess[i])
        else:
            exemptions.append(guess[i])
    
    if count == 0:
        solution = [word for word in solutions if all(x in word for x in yellows) 
                     and any(x in word[0] for x in letters['1'])
                     and any(x in word[1] for x in letters['2'])
                     and any(x in word[2] for x in letters['3'])
                     and any(x in word[3] for x in letters['4'])
                     and any(x in word[4] for x in letters['5'])
                     and not any(x in word[0] for x in exempts['1'] if exempts['1'])
                     and not any(x in word[1] for x in exempts['2'] if exempts['2'])
                     and not any(x in word[2] for x in exempts['3'] if exempts['3'])
                     and not any(x in word[3] for x in exempts['4'] if exempts['4'])
                     and not any(x in word[4] for x in exempts['5'] if exempts['5'])
                     and not any(x in word for x in exemptions)
                    ]
    else:
        solution = [word for word in solution if all(x in word for x in yellows) 
                     and any(x in word[0] for x in letters['1'])
                     and any(x in word[1] for x in letters['2'])
                     and any(x in word[2] for x in letters['3'])
                     and any(x in word[3] for x in letters['4'])
                     and any(x in word[4] for x in letters['5'])
                     and not any(x in word[0] for x in exempts['1'] if exempts['1'])
                     and not any(x in word[1] for x in exempts['2'] if exempts['2'])
                     and not any(x in word[2] for x in exempts['3'] if exempts['3'])
                     and not any(x in word[3] for x in exempts['4'] if exempts['4'])
                     and not any(x in word[4] for x in exempts['5'] if exempts['5'])
                     and not any(x in word for x in exemptions)
                   ]

    print(solution)
    
    if not solution:
        return 'Solution does not exist'
        
    df = pd.DataFrame(solution, columns=['words'])
    df['scoring'] = df['words'].apply(lambda s: scoring(s, 13, 1))

    df = df[df['words'].isin(solution)].sort_values('scoring', ascending=False)
    
    suggested_guess = df['words'].iloc[0]

    count += 1
    
    if len(solution) == 1:
        if guess not in solution:
            count += 1
        stop = True
        init_flag = False
        return 'Solution is: {}'.format(solution[0])
    
    if count == 6:
        stop = True
        init_flag = False
        return '6 guesses reached'
    
    return suggested_guess
