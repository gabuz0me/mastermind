#!/usr/bin/env python3

import argparse
from collections import namedtuple, defaultdict
from random import choices, shuffle
from textwrap import dedent

class MastermindState:
    COLORS = ('W', 'K', 'R', 'G', 'B', 'Y', 'O', 'P')
    Answer = namedtuple('Answer', ['good', 'wrong'])

    def __init__(self, allow_duplicate = False, nb_color=8, size=5, nb_guess=12) -> None:
        if (not allow_duplicate and nb_color < size):
            raise Exception("If duplicate colors are not allowed, secret length must not be longer than the number of colors")
        if (nb_color < 2 or nb_color > len(MastermindState.COLORS)):
            raise Exception(f"Number of color must be between 2 and {len(MastermindState.COLORS)}")
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
            raise Exception("Guess length must be secret length")
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

class MastermindDisplayer:
    COLOR_CODES_8 = {
        # https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit
        'W' : 97, # bright white
        'K' : 90, # bright black
        'R' : 31, # red
        'G' : 32, # green
        'B' : 34, # blue
        'Y' : 93, # bright yellow
        'O' : 33, # yellow
        'P' : 95, # bright magenta
        'START' : '\u001b[',
        'END'   : ';1m', # ;1 is boldness
        'RESET' : '\u001b[0m',
    }
    COLOR_CODES_256 = {
        # https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
        'W' : 15,
        'K' : 238,
        'R' : 1,
        'G' : 2,
        'B' : 12,
        'Y' : 3,
        'O' : 208,
        'P' : 13,
        'START' : '\u001b[38;5;',
        'END'   : ';1m', # ;1 is boldness
        'RESET' : '\u001b[0m',
    }

    def __init__(self, mastermind:MastermindState, use_colors:bool = False, use_8_color:bool = False) -> None:
        self.use_colors = use_colors
        self.mastermind = mastermind
        self.use_8_colors = use_8_color

    def colored(self, color, msg) -> str:
        if not self.use_colors:
            return msg
        CC = MastermindDisplayer.COLOR_CODES_8 if self.use_8_colors else MastermindDisplayer.COLOR_CODES_256
        if not color in CC:
            return msg # No coloring
        color_str = CC['START'] + str(CC[color]) + CC['END']
        return color_str + str(msg) + CC['RESET']

    @property
    def secret(self) -> str:
        secret = ""
        for color in self.mastermind._secret:
            secret += self.colored(color, color) + " "
        return secret[0:-1]

    @property
    def allowed_colors(self) -> str:
        string = "Allowed colors are:"
        for i in range(self.mastermind.nb_color):
            color = self.mastermind.COLORS[i]
            string += " " + self.colored(color, color)
        return string

    def show(self) -> None:
        _=self.colored
        print(f"[{_('B','##')}] {_('G','!')} {_('O','?')}   {_('W','| '*len(self.mastermind._secret))}")
        for i in range(len(self.mastermind.guesses)):
            indic = self.mastermind.indications[i]
            guess = ""
            for g in self.mastermind.guesses[i]:
                guess += self.colored(g, g)
                guess += " "
            good = '.' if indic.good == 0 else indic.good
            if indic.good > 0:
                good = self.colored('G', good)
            wrong = '.' if indic.wrong == 0 else indic.wrong
            if indic.wrong > 0:
                wrong = self.colored('O', wrong)
            nb = f"{i+1:2}"
            print(f"[{_('B', nb)}] {good} {wrong}   {guess}")
            
    def start(self) -> int:
        nb = 1
        # print(str(self.mastermind._secret))
        print(self.allowed_colors)
        while True:
            # Showing gameboard
            self.show()

            # Finish if lost
            if nb > self.mastermind.nb_guess:
                print(self.colored('B', f"You lost!\nAnswer:    {self.secret}"))
                break

            # Input and intercept user breaking
            try:
                guess = input(" > ").strip().upper().replace(' ', '')
            except KeyboardInterrupt:
                print(self.colored('B', f"\nAnswer:    {self.secret}"))
                break

            # Check for invalid guess size
            if (len(guess) != len(self.mastermind._secret)):
                print(self.colored(
                    'R',
                    f"Invalid guess size:{len(guess)} (must be {len(self.mastermind._secret)})"
                ))
                continue

            # Check for invalid colors in guess
            invalid_color = ""
            for color in guess:
                if color not in self.mastermind.COLORS:
                    invalid_color = color
                    break
            if invalid_color:
                print(self.colored('R', f"Invalid color: {invalid_color}"))
                continue
                    
            # Finish if won
            if self.mastermind.guess(guess):
                print(self.colored('G', "Well done!"))
                break

            nb+=1
        return nb

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=dedent("""\
            Classic Mastermind in your console!
            """
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-s', '--size',
        help="length of the secret",
        type=int,
        default=5,
    )
    parser.add_argument(
        '-c', '--nb-colors',
        help=f"number of different colors (2-{len(MastermindState.COLORS)})",
        type=int,
        default=8,
    )
    parser.add_argument(
        '-g', '--nb-guesses',
        help="number of guesses",
        type=int,
        default=12,
    )
    parser.add_argument(
        '-d', '--duplicate',
        help="allow duplicate colors in generated secret",
        action='store_true',
    )
    parser.add_argument(
        '-n', '--no-colors',
        help="outputs mastermind without color",
        action='store_true',
    )
    parser.add_argument(
        '-8', '--use-8-colors-mode',
        help="use 8 colors mode",
        action='store_true',
    )
    args = parser.parse_args()
    #print(args)

    # Creating the displayer beforehand to express errors in a colored way.
    displayer = MastermindDisplayer(
        None,
        use_colors=not args.no_colors,
        use_8_color=args.use_8_colors_mode,
    )
    try:
        mastermind = MastermindState(
            allow_duplicate=args.duplicate,
            nb_color=args.nb_colors,
            size=args.size,
            nb_guess=args.nb_guesses,
        )
        displayer.mastermind = mastermind
        displayer.start()
    except Exception as e:
        print(displayer.colored('R', e))
