import stdio
import sys
from markov_model import MarkovModel


# Takes an integer k (model order) and a string s (noisy message) as
# command-line arguments, reads the input text from standard input, and
# prints out the most likely original string.
def main():
    k, s = int(sys.argv[1]), sys.argv[2]
    text = sys.stdin.read()
    model = MarkovModel(text, k)
    stdio.writeln(model.replace_unknown(s))


if __name__ == '__main__':
    main()
