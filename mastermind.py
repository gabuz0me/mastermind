#!/usr/bin/env python

from random import choices, shuffle
from collections import namedtuple, defaultdict

class Mastermind:
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
            shuffled = list(Mastermind.COLORS)
            shuffle(shuffled)
            return shuffled[0:self.size]
        else:
            return choices(Mastermind.COLORS, k=self.size)

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
        return Mastermind.Answer(nb_good, nb_wrong)

    def guess(self, guess:list) -> bool:
        answer = Mastermind.testGuess(guess, self._secret)
        self.guesses.append(guess)
        self.indications.append(answer)
        if answer.good == len(guess):
            return True
        return False

    def showTerrain(self) -> None:
        print(f"[##] ! ? < {'| '*len(self._secret)}>")
        for i in range(len(self.guesses)):
            indic = self.indications[i]
            guess = " ".join(self.guesses[i])
            print(f"[{i+1:2}] {indic.good} {indic.wrong}   {guess}")

    @property
    def secret(self) -> str:
        return " ".join(self._secret)

    def start(self) -> int:
        nb = 1
        # print(str(self._secret))
        while True:
            self.showTerrain()
            if nb > self.nb_guess:
                print(f"Answer was : {self.secret}")
                break
            guess = input(" > ").strip().upper().replace(' ', '')
            if (len(guess) != len(self._secret)):
                print("Invalid guess size!")
                continue
            if self.guess(guess):
                break
            nb+=1
        return nb


if __name__ == '__main__':
    mastermind = Mastermind()
    mastermind.start()
