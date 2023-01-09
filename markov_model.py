"""
markov_model.py

A data type that represents a Markov model of order k from a given text string.
"""

import stdio
import stdrandom
import sys
import stdarray
import random


class MarkovModel(object):
    """
    Represents a Markov model of order k from a given text string.
    """

    def __init__(self, text, k):
        """
        Creates a Markov model of order k from given text. Assumes that text
        has length at least k.
        """

        self._k = k
        newtxt = text + text[:k]
        self._st = {}
        size = len(newtxt)
        for count in range(0, size-k):
            hold = newtxt[count:k+count]
            if hold in self._st:
                if newtxt[k+count] in self._st[hold]:
                    self._st[hold][newtxt[k+count]] += 1
                else:
                    self._st[hold][newtxt[k+count]] = 1
            else:
                self._st[hold] = {}
                self._st[hold][newtxt[k+count]] = 1

    def order(self):
        """
        Returns order k of Markov model.
        """
        return self._k

    def kgram_freq(self, kgram):
        """
        Returns number of occurrences of kgram in text. Raises an error if
        kgram is not of length k.
        """
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' +
                             str(self._k))
        elif kgram in self._st:
            return sum(self._st[kgram].values())
        else:
            return 0

    def char_freq(self, kgram, c):
        """
        Returns number of times character c follows kgram. Raises an error if
        kgram is not of length k.
        """

        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' +
                             str(self._k))
        elif kgram not in self._st or c not in self._st[kgram]:
            return 0
        else:
            return self._st[kgram][c]

    def rand(self, kgram):
        """
        Returns a random character following kgram. Raises an error if kgram
        is not of length k or if kgram is unknown.
        """

        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' +
                             str(self._k))
        if kgram not in self._st:
            raise ValueError('Unknown kgram ' + kgram)
        c = len(self._st[kgram])
        char_num = stdarray.create1D(c, 0)
        hold = list(self._st[kgram].keys())
        total = self.kgram_freq(kgram)
        if c > 1:
            for i in range(len(hold)):
                char_num[i] = self.char_freq(kgram, hold[i]) / total
        else:
            char_num[0] = self.char_freq(kgram, hold[0]) / total

        choice = max(char_num)
        char = stdrandom.discrete(char_num)
        hold2 = stdarray.create1D(len(char_num), 0)
        for a in range(c):
            if choice == char_num[a]:
                hold2[a] = char
        return random.choice(hold)

    def gen(self, kgram, T):
        """
        Generates and returns a string of length T by simulating a trajectory
        through the correspondng Markov chain. The first k characters of the
        generated string is the argument kgram. Assumes that T is at least k.
        """
        newtxt = kgram
        hold = list(self._st.keys())
        count = 0
        for i in range(T-self._k):
            newtxt += self.rand(newtxt[i:self._k+i])
        return newtxt

    def replace_unknown(self, corrupted):
        """
        Replaces unknown characters (~) in corrupted with most probable
        characters, and returns that string.
        """

        # Given a list a, argmax returns the index of the maximum element in a.
        size = len(corrupted)
        p = 1
        prob = []

        def argmax(a):
            return a.index(max(a))
        for i in range(size):
            if corrupted[i] == '~':
                prob[:] = []
                p = 1
                kgram_b = corrupted[i-self._k:i]
                kgram_a = corrupted[i+1:i+self._k+1]
                context = kgram_b + '~' + kgram_a
                keyhold = list(self._st[kgram_b].keys())
                for a in range(len(keyhold)):
                    p = 1
                    ntxt = context.replace('~', keyhold[a], 1)
                    for b in range(self._k+1):
                        if ntxt[b:b-self._k-1] in self._st:
                            cal1 = self.char_freq(ntxt[b:b-self._k-1],
                                                  ntxt[self._k+b:self._k+b+1])
                            cal2 = self.kgram_freq(ntxt[b:b-self._k-1])
                            p *= cal1 / cal2
                        else:
                            p = 0
                            break
                    prob.append(p)
                corrupted = corrupted.replace('~', keyhold[argmax(prob)], 1)
        return corrupted


def _main():
    """
    Test client [DO NOT EDIT].
    """

    text, k = sys.argv[1], int(sys.argv[2])
    model = MarkovModel(text, k)
    a = []
    while not stdio.isEmpty():
        kgram = stdio.readString()
        char = stdio.readString()
        a.append((kgram.replace("-", " "), char.replace("-", " ")))
    for kgram, char in a:
        if char == ' ':
            stdio.writef('freq(%s) = %s\n', kgram, model.kgram_freq(kgram))
        else:
            stdio.writef('freq(%s, %s) = %s\n', kgram, char,
                         model.char_freq(kgram, char))


if __name__ == '__main__':
    _main()
