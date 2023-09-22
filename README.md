# Mastermind

Classic Mastermind in your console!

---

## Usage

Running `mastermind.py -h` shows this message:

```text
usage: mastermind.py [-h] [-s SIZE] [-c NB_COLORS] [-g NB_GUESSES] [-d] [-n] [-8]

Classic Mastermind in your console!

options:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  length of the secret (default: 5)
  -c NB_COLORS, --nb-colors NB_COLORS
                        number of different colors (2-8) (default: 8)
  -g NB_GUESSES, --nb-guesses NB_GUESSES
                        number of guesses (default: 12)
  -d, --duplicate       allow duplicate colors in generated secret (default: False)
  -n, --no-colors       outputs mastermind without color (default: False)
  -8, --use-8-colors-mode
                        use 8 colors mode (default: False)
```

You can simply run `mastermind.py` to start a game, or tweak its parameters using arguments.

---

![A (lost) game](https://raw.githubusercontent.com/gabuz0me/images/main/mastermind/demo.png)
