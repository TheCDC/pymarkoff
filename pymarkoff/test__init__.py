import unittest
import pymarkoff
from pymarkoff import Head, Tail
from collections import Counter


class TestInputOutput(unittest.TestCase):

    def test_simple_transitions_order_1(self):
        b = pymarkoff.Markov(seeds=['a'])
        target = {
            (pymarkoff.Head(), ): Counter({
                'a': 1
            }),
            ('a', ): pymarkoff.Counter({
                pymarkoff.Tail(): 1
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
