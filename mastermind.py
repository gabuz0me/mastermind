#!/usr/bin/env python

from random import choices, shuffle
from collections import namedtuple, defaultdict
from enum import Enum


class MastermindState:
    COLORS = ('W', 'K', 'R', 'G', 'B', 'Y', 'O', 'P')
    Answer = namedtuple('Answer', ['good', 'wrong'])

    def __init__(self, allow_duplicate = False, nb_color=8, size=5, nb_guess=12) -> None:
        if (not allow_duplicate and nb_color < size): raise Exception
        self.allow_duplicate = allow_duplicate
        self.nb_color = nb_color
        self.size = size
        self.nb_guess = nb_guess

        self.guesses = []
        self.indications = []
        self._secret = self.createSecret()

    def createSecret(self) -> list:
        if not self.allow_duplicate:
            shuffled = list(MastermindState.COLORS)
            shuffle(shuffled)
            return shuffled[0:self.size]
        else:
            return choices(MastermindState.COLORS, k=self.size)

    @classmethod
    def testGuess(cls, guess:list, secret:list) -> Answer:
        if len(guess) != len(secret):
            raise Exception
        color_dict_guess = defaultdict(lambda:0)
        color_dict_secret = defaultdict(lambda:0)
        nb_good = 0
        nb_wrong = 0
        for i in range(len(guess)):
            if (guess[i] == secret[i]):
                nb_good += 1
            else:
                color_dict_guess[guess[i]]+=1
                color_dict_secret[secret[i]]+=1
        for k in color_dict_guess.keys():
            nb_wrong += min(color_dict_guess[k], color_dict_secret[k])
        return MastermindState.Answer(nb_good, nb_wrong)

    def guess(self, guess:list) -> bool:
        answer = MastermindState.testGuess(guess, self._secret)
        self.guesses.append(guess)
        self.indications.append(answer)
        if answer.good == len(guess):
            return True
        return False

    @property
    def secret(self) -> str:
        return " ".join(self._secret)


class Mastermind:
    def __init__(self, colors:bool = False, allow_duplicate = False, nb_color=8, size=5, nb_guess=12) -> None:
        self.mastermind = MastermindState(allow_duplicate, nb_color, size, nb_guess)
        self.displayer = MastermindDisplayer(self.mastermind, colors)

    def start(self) -> int:
        nb = 1
        # print(str(self.mastermind._secret))
        while True:
            self.displayer.show()
            if nb > self.mastermind.nb_guess:
                print(f"Answer was : {self.mastermind.secret}")
                break
            guess = input(" > ").strip().upper().replace(' ', '')
            if (len(guess) != len(self.mastermind._secret)):
                print("Invalid guess size!")
                continue
            if self.mastermind.guess(guess):
                print("Well done!")
                break
            nb+=1
        return nb


class MastermindDisplayer:
    COLOR_CODES = {
        # https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
        # 'W' : 97, # bright white
        # 'K' : 90, # bright black
        # 'R' : 31, # red
        # 'G' : 32, # green
        # 'B' : 34, # blue
        # 'Y' : 93, # bright yellow
        # 'O' : 33, # yellow
        # 'P' : 95, # bright magenta
        'W' : 15,
        'K' : 7,
        'R' : 1,
        'G' : 2,
        'B' : 12,
        'Y' : 3,
        'O' : 208,
        'P' : 13,
        'START' : '\u001b[38;5;',
        'END'   : 'm', # ;1 is boldness
        'RESET' : '\u001b[0m',
    }

    @classmethod
    def colored(cls, color, msg) -> str:
        CC = MastermindDisplayer.COLOR_CODES
        if not color in CC:
            raise TypeError(f'Unknown color {color}')
        color_str = CC['START'] + str(CC[color]) + CC['END']
        return color_str + str(msg) + CC['RESET']
        
    def __init__(self, mastermind:MastermindState, colors:bool = False) -> None:
        self.colors = colors
        self.mastermind = mastermind

    def show(self) -> None:
        print(f"[##] ! ? < {'| '*len(self.mastermind._secret)}>")
        for i in range(len(self.mastermind.guesses)):
            indic = self.mastermind.indications[i]
            if not self.colors:
                guess = " ".join(self.mastermind.guesses[i])
            else:
                guess = ""
                for g in self.mastermind.guesses[i]:
                    guess += MastermindDisplayer.colored(g, g)
                    guess += " "
            good = '.' if indic.good == 0 else indic.good
            wrong = '.' if indic.wrong == 0 else indic.wrong
            if self.colors:
                if indic.good > 0:
                    good = MastermindDisplayer.colored('G', good)
                if indic.wrong > 0:
                    wrong = MastermindDisplayer.colored('O', wrong)
            print(f"[{i+1:2}] {good} {wrong}   {guess}")

if __name__ == '__main__':
    # print("Testing Colors:")
    # print("\u001b[38;5;3;1m TEST 8-bit \u001b[0m")
    # print("\u001b[93;1m TEST-ANSI \u001b[0m")
    # print("")
    mastermind = Mastermind(True)
    mastermind.start()
