Originally a proof of concept, I've used this in enough projects that I've decided to publish it tomake it easier to import.
#Basic Use

Instantiate with `m = markoff.Markov(seeds)` where `seeds` is an iterable of sub-iterables. Each sub-iterable being a chain in the set of chains you want to model.

You can supply it with just one chain or many.



