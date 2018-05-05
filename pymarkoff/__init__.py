#!/usr/bin/env python3
"""A module for creating Markov models of sequences
and generating sequences based on that model.
Use the from_sentences() or from_words() depending on the format of your data.

"""

import pprint as pp
import re
import random
import time
import itertools
import bisect
import pydot
from collections import Counter
import pdb
import queue
from itertools import islice, chain


class InvalidStateError(Exception):
    """A simple exception to indicate when Markov is trying to reference
    a nonexistent state."""
    pass


class Anchor():
    """A parent class for chain anchors."""

    def __init__(self, s=None):
        self.description = s

    def __len__(self, ):
        return 0

    def __cmp__(self, other):
        if isinstance(other, str):
            return -1

    def __eq__(self, other):
        return type(self) == type(other)

    def __str__(self):
        return "Anchor()"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((type(self), ))


class Head(Anchor):
    """A dummy class used internally to anchor the beginning of an input chain.
    Don't bother reading about this"""

    def __str__(self):
        return self.description if self.description else "[Head]"

    def __repr__(self):
        return "Head()"


class Tail(Anchor):
    """A dummy class used internally to anchor the end of an input chain.
    Don't bother reading about this"""

    def __str__(self):
        return self.description if self.description else "[Tail]"

    def __repr__(self):
        return "Tail()"


class Markov:
    """A Markov Chain modeller and sequence generator using the model.
    Get a lot of input and produce a short output multiple times.
    Input should be lists of strings beginning with an emptystring.
    The Head object is used as the entry point every time generate() is called."""

    def __init__(self, seeds=None, orders=(1, ), discrete=True):
        """Seeds should be an iterable of iterables.
        This is so that entry points can be determined automatically.
        discrete=True Enables analysis of chains as having specific start and end points.
        discrete=False treats all chains as a continuous time series, more or less.
        When discrete=False, each seed must have 2 states.
        That is in order to establish a transition."""
        if seeds is None:
            raise ValueError("Must provide seeds!")
        for i in orders:
            if i < 0:
                raise ValueError(
                    "{} is an invalid order for analysis!".format(i))
        self.transitions = dict()
        # force orders to be descending
        self.orders = tuple(sorted(orders)[::-1])
        # self.cur_state = self.start
        self.discrete = discrete
        self.feed(seeds)

    def feed(self, seeds) -> None:
        """Feed the generator with a list of lists, called seeds.
        I.e. m = pymarkoff.Markov()
        m.feed([['The','quick','brown','fox','jumped','over','the','lazy','dog.']])
        m.generate() => ['The','lazy','dog.']

        """
        for seed in seeds:
            # go through each seed
            orders_buffer = {o: list() for o in self.orders}
            # store only a moving window of the input chains
            short_memory = queue.deque([], max(self.orders) + 1)
            extra_bits = []
            # handle the the input being separate chains
            if self.discrete:
                short_memory.append(Head())
                extra_bits.append(Tail())

            for state in chain(seed, extra_bits):
                short_memory.append(state)
                # slice the window based on orders being modelled
                for o in orders_buffer.keys():
                    if len(short_memory) < o + 1:
                        break
                    run = list(islice(short_memory, 0, o + 2))
                    head = tuple(run[:-1])
                    tail = run[-1]
                    # update the transition table
                    try:
                        self.transitions[head].update([tail])
                    except KeyError:
                        self.transitions[head] = Counter([tail])

    def get_next(self, state):
        """Exposed Internal helper function.
        Takes a tuple of one or more states and predicts the next one.
        Example:
            If the object has been fed the string 'Bananas',
                In: ('B',)
                Out: 'a'
        """
        try:
            state_transitions = self.transitions[state]
            choice = weighted_random(
                *list(zip(*list(state_transitions.items())[::-1])))
        except KeyError:
            raise InvalidStateError("state {} never fed in. Brain:{}".format(
                repr(state),
                dict(self).keys()))
        return choice

    def generate(self, *, max_length=100) -> list:
        """Returns a list of states chosen by simulation.
        Simulation starts from a state chosen from known head states
        and ends at either a known terminating state or when the chain
        reaches max_length, whichever comes first."""
        state = Head()
        result = [state]
        choice = state
        i = 0
        sorted_orders = sorted(self.orders)[::-1]
        import pudb
        pudb.set_trace()
        while i <= max_length and not isinstance(state, Tail):
            # check for transitions in the highest allowed order first
            # then check lower orders (which are more likely to have a hit).
            for cur_order in sorted_orders:
                try:
                    # reach back for a sequence of states of length less equal
                    # to the current order.
                    temp_state = tuple(
                        result[len(result) - (cur_order):len(result)])
                    # choice = random.choice(self.transitions[temp_state])
                    choice = self.get_next(temp_state)
                    print(choice)
                    break
                except InvalidStateError as e:
                    # An InvalidStateError happens when there aren't transitions for an
                    # arbitrary higher order state
                    # In which case, carry on and continue to the next lowest
                    # order.
                    # raise e
                    pass

            state = choice
            result.append(choice)
            i += 1
        # slice off the head and  tail
        result.pop(0)
        result.pop(-1)
        return result

    def next_word(self, *args, **kwargs) -> str:
        """Treat chain generator output as a word and format accordingly.
        Passes arguments to generate()"""
        return ''.join(self.generate(*args, **kwargs))

    def next_sentence(self, *args, **kwargs) -> str:
        """Treat chain generator output as a sentence
        and format accordingly.
        Passes arguments to generate()"""
        return ' '.join(self.generate(*args, **kwargs))

    def __str__(self) -> str:
        return str(self.transitions)

    def __iter__(self) -> tuple:
        """Yield items in the transition table like a dict."""
        for item in self.transitions.items():
            # yield (t[0],sorted(t[1]))
            yield item

    def to_graph(self) -> pydot.Dot:
        """Return a pydot.Dot graph object representing the internal transition table."""
        # pdb.set_trace()
        g = pydot.Dot()
        for k, v in dict(self).items():
            for target in v:
                weight = v[target] / sum(v.values())
                g.add_edge(
                    pydot.Edge(
                        str(k), str((target, )),
                        label="{:.2f}".format(weight)))
        return g


def weighted_random(choices, weights):
    """Randomly choose an item from choices weighted by weights."""
    cumdist = list(itertools.accumulate(weights))
    cursor = random.random() * cumdist[-1]
    return choices[bisect.bisect(cumdist, cursor)]


def filter_by_user(data) -> list:
    """Return a list from data where each item was interactively allowed by the user."""

    good = []
    for sentence in data:
        print(sentence)
        res = input("Good? y/n >>>").lower()
        if res == 'y':
            good.append(sentence)
        elif res == 'e':
            break
        else:
            pass
    return good


def from_sentences(source, *args, delimiter='\n', **kwargs) -> Markov:
    """A helper function to produce a chain generator from sentences.
    Returns a Markov object that produces sentences.
    Input should be a string of sentences separated by newlines or [delimiter].
    Words in sentences should be separated by spaces.
    """
    chains = [i.split(" ") for i in source.split(delimiter)]
    return Markov(chains, *args, **kwargs)


def from_words(source, *args, delimiter='\n', **kwargs) -> Markov:
    """A helper function to produce a chain generator from words.
    Returns a Markov object that produces words.
    Input should be words separated by newlines or else by [delimiter]
    """
    chains = [list(i) for i in source.split()]
    return Markov(chains, *args, **kwargs)


def main() -> None:
    """An Interactive mode. Mostly used for testing."""
    # I have been playing a lot of Overwatch lately.
    mystr = """Ana
Bastion
D.Va
Genji
Hanzo
Junkrat
Lúcio
McCree
Mei
Mercy
Pharah
Reaper
Reinhardt
Roadhog
Soldier: 76
Sombra
Symmetra
Torbjörn
Tracer
Widowmaker
Winston
Zarya
Zenyatta"""
    seeds = """The quick brown fox jumped over the lazy dog.
Jack and Jill ran up the hill to fetch a pail of water.
Whenever the black fox jumped the squirrel gazed suspiciously.
Five quacking zephyrs jolt my wax bed.
Do wafting zephyrs quickly vex Jumbo?"""

    brain = from_words(mystr, orders=(1, ))
    # brain = from_sentences(mystr, orders=(0, ))
    brain.to_graph().write_png("img/OW Names.png")
    # seeds = [i.split(' ') for i in seeds]
    # print(dict(brain).keys())
    pp.pprint(brain.transitions)
    pp.pprint(brain.transitions[('g', )])
    # print(brain.get_next(("the",)))
    print([brain.next_word() for i in range(10)])
    bbrain = from_sentences(seeds)
    bbrain.to_graph().write_png("img/pangrams.png")
    print(bbrain.next_sentence())

    bananas = from_words("Bananas", orders=tuple(range(10)))
    bananas.to_graph().write_png("img/bananas.png")
    print([bananas.next_word() for i in range(10)])
    # print(sorted(dict(bbrain).keys()))
    # print(brain.next_sentence())
    # results_f = [' '.join(m.generate(max_length=30)) for i in range(10)]


if __name__ == '__main__':
    main()

    # from itertools import product
# combs = '\n'.join(' '.join([''.join(line) for line in zip(*sol)])
#                   for sol in product(permutations(prefixes), permutations(suffixes)))
# print(combs)
