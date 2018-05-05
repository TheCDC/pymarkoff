import unittest
import pymarkoff
from pymarkoff import Head, Tail
from collections import Counter


class TestHelpers(unittest.TestCase):

    def test_from_sentences(self):
        self.maxDiff = None
        b = pymarkoff.from_sentences(
            """The quick brown fox jumped over the lazy dog.
Jack and Jill ran up the hill to fetch a pail of water.""")

        target = {
            (Head(), ): Counter({
                'The': 1,
                'Jack': 1
            }),
            ('The', ): Counter({
                'quick': 1
            }),
            ('quick', ): Counter({
                'brown': 1
            }),
            ('brown', ): Counter({
                'fox': 1
            }),
            ('fox', ): Counter({
                'jumped': 1
            }),
            ('jumped', ): Counter({
                'over': 1
            }),
            ('over', ): Counter({
                'the': 1
            }),
            ('the', ): Counter({
                'lazy': 1,
                'hill': 1
            }),
            ('lazy', ): Counter({
                'dog.': 1
            }),
            ('dog.', ): Counter({
                Tail(): 1
            }),
            ('Jack', ): Counter({
                'and': 1
            }),
            ('and', ): Counter({
                'Jill': 1
            }),
            ('Jill', ): Counter({
                'ran': 1
            }),
            ('ran', ): Counter({
                'up': 1
            }),
            ('up', ): Counter({
                'the': 1
            }),
            ('hill', ): Counter({
                'to': 1
            }),
            ('to', ): Counter({
                'fetch': 1
            }),
            ('fetch', ): Counter({
                'a': 1
            }),
            ('a', ): Counter({
                'pail': 1
            }),
            ('pail', ): Counter({
                'of': 1
            }),
            ('of', ): Counter({
                'water.': 1
            }),
            ('water.', ): Counter({
                Tail(): 1
            })
        }

        # print('sentences', b)
        self.assertEqual(b.transitions, target)

    def test_from_words(self):
        b = pymarkoff.from_words(
            """The quick brown fox jumped over the lazy dog.
Jack and Jill ran up the hill to fetch a pail of water.""")
        target = {
            (Head(), ):
            Counter({
                't': 3,
                'f': 2,
                'o': 2,
                'J': 2,
                'a': 2,
                'T': 1,
                'q': 1,
                'b': 1,
                'j': 1,
                'l': 1,
                'd': 1,
                'r': 1,
                'u': 1,
                'h': 1,
                'p': 1,
                'w': 1
            }),
            ('T', ):
            Counter({
                'h': 1
            }),
            ('h', ):
            Counter({
                'e': 3,
                'i': 1,
                Tail(): 1
            }),
            ('e', ):
            Counter({
                Tail(): 3,
                'r': 2,
                'd': 1,
                't': 1
            }),
            ('q', ):
            Counter({
                'u': 1
            }),
            ('u', ):
            Counter({
                'i': 1,
                'm': 1,
                'p': 1
            }),
            ('i', ):
            Counter({
                'l': 3,
                'c': 1
            }),
            ('c', ):
            Counter({
                'k': 2,
                'h': 1
            }),
            ('k', ):
            Counter({
                Tail(): 2
            }),
            ('b', ):
            Counter({
                'r': 1
            }),
            ('r', ):
            Counter({
                'o': 1,
                Tail(): 1,
                'a': 1,
                '.': 1
            }),
            ('o', ):
            Counter({
                'w': 1,
                'x': 1,
                'v': 1,
                'g': 1,
                Tail(): 1,
                'f': 1
            }),
            ('w', ):
            Counter({
                'n': 1,
                'a': 1
            }),
            ('n', ):
            Counter({
                Tail(): 2,
                'd': 1
            }),
            ('f', ):
            Counter({
                'o': 1,
                'e': 1,
                Tail(): 1
            }),
            ('x', ):
            Counter({
                Tail(): 1
            }),
            ('j', ):
            Counter({
                'u': 1
            }),
            ('m', ):
            Counter({
                'p': 1
            }),
            ('p', ):
            Counter({
                'e': 1,
                Tail(): 1,
                'a': 1
            }),
            ('d', ):
            Counter({
                Tail(): 2,
                'o': 1
            }),
            ('v', ):
            Counter({
                'e': 1
            }),
            ('t', ):
            Counter({
                'h': 2,
                'o': 1,
                'c': 1,
                'e': 1
            }),
            ('l', ):
            Counter({
                Tail(): 3,
                'l': 2,
                'a': 1
            }),
            ('a', ):
            Counter({
                'n': 2,
                'z': 1,
                'c': 1,
                Tail(): 1,
                'i': 1,
                't': 1
            }),
            ('z', ):
            Counter({
                'y': 1
            }),
            ('y', ):
            Counter({
                Tail(): 1
            }),
            ('g', ):
            Counter({
                '.': 1
            }),
            ('.', ):
            Counter({
                Tail(): 2
            }),
            ('J', ):
            Counter({
                'a': 1,
                'i': 1
            })
        }
        self.assertEqual(b.transitions, target)


class TestInputOutput(unittest.TestCase):

    def test_simple_transitions_order_1(self):
        b = pymarkoff.Markov(seeds=['aaa'])
        target = {
            (pymarkoff.Head(), ): Counter({
                'a': 1
            }),
            ('a', ): pymarkoff.Counter({
                pymarkoff.Tail(): 1,
                'a': 2,
            })
        }
        self.assertEqual(b.transitions, target)

    def test_simple_transitions_order_3(self):
        b = pymarkoff.Markov(seeds=['aaaaaa'], orders=(3, ))
        target = {
            (Head(), 'a', 'a'): Counter({
                'a': 1
            }),
            ('a', 'a', 'a'): Counter({
                'a': 3,
                Tail(): 1
            })
        }
        self.assertEqual(b.transitions, target)

    def test_transitions_long_input_order_1(self):
        b = pymarkoff.Markov(seeds=['abcdefg'])
        target = {
            (pymarkoff.Head(), ): Counter({
                'a': 1
            }),
            ('a', ): Counter({
                'b': 1
            }),
            ('b', ): Counter({
                'c': 1
            }),
            ('c', ): Counter({
                'd': 1
            }),
            ('d', ): Counter({
                'e': 1
            }),
            ('e', ): Counter({
                'f': 1
            }),
            ('f', ): Counter({
                'g': 1
            }),
            ('g', ): Counter({
                pymarkoff.Tail(): 1
            })
        }
        self.assertEqual(b.transitions, target)

    def test_transitions_long_input_order_3(self):
        b = pymarkoff.Markov(seeds=['abcdefg'], orders=(3, ))
        target = {
            (Head(), 'a', 'b'): Counter({
                'c': 1
            }),
            ('a', 'b', 'c'): Counter({
                'd': 1
            }),
            ('b', 'c', 'd'): Counter({
                'e': 1
            }),
            ('c', 'd', 'e'): Counter({
                'f': 1
            }),
            ('d', 'e', 'f'): Counter({
                'g': 1
            }),
            ('e', 'f', 'g'): Counter({
                Tail(): 1
            })
        }
        self.assertEqual(b.transitions, target)

    def test_transition_repeated_states_order1(self):
        b = pymarkoff.Markov(seeds=['aaaabbbbcccccabcabc'])
        # print('t', b.transitions)
        target = {
            (Head(), ): Counter({
                'a': 1
            }),
            ('a', ): Counter({
                'a': 3,
                'b': 3
            }),
            ('b', ): Counter({
                'b': 3,
                'c': 3
            }),
            ('c', ): Counter({
                'c': 4,
                'a': 2,
                Tail(): 1
            })
        }
        self.assertEqual(b.transitions, target)

    def test_transition_repeated_states_order3(self):
        b = pymarkoff.Markov(seeds=['aaaabbbbcccccabcabc'], orders=(3, ))
        target = {
            (Head(), 'a', 'a'): Counter({
                'a': 1
            }),
            ('a', 'a', 'a'): Counter({
                'a': 1,
                'b': 1
            }),
            ('a', 'a', 'b'): Counter({
                'b': 1
            }),
            ('a', 'b', 'b'): Counter({
                'b': 1
            }),
            ('b', 'b', 'b'): Counter({
                'b': 1,
                'c': 1
            }),
            ('b', 'b', 'c'): Counter({
                'c': 1
            }),
            ('b', 'c', 'c'): Counter({
                'c': 1
            }),
            ('c', 'c', 'c'): Counter({
                'c': 2,
                'a': 1
            }),
            ('c', 'c', 'a'): Counter({
                'b': 1
            }),
            ('c', 'a', 'b'): Counter({
                'c': 2
            }),
            ('a', 'b', 'c'): Counter({
                'a': 1,
                Tail(): 1
            }),
            ('b', 'c', 'a'): Counter({
                'b': 1
            })
        }

        self.assertEqual(b.transitions, target)
