Originally a proof of concept, I've used this in enough projects that I've decided to publish it tomake it easier to import.
The name is a play on words similar to Markup/Markdown.

# Basic Use #

Instantiate with `m = markoff.Markov(seeds)` where `seeds` is an iterable of sub-iterables. Each sub-iterable being a chain in the set of chains you want to model.

You can supply it with just one chain or many.

Then use `m.generate(max_length=100)` to produce a single chain limited to `max_length` automatically terminating at any character of `.!?`.
You can also supply a `terminators` argument to make the chain

# Example #

## Code ##

```
m = markoff.Markov(
	[
		['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog.'],
		['Jack', 'and', 'Jill', 'ran', 'up', 'the', 'hill', 'to', 'fetch', 'a', 'pail', 'of', 'water.']
	]
)
[m.generate() i for i in range(5)]
```

## Output ##

```
[
	'The quick brown fox jumped over the hill to fetch a pail of water.',
	'The quick brown fox jumped over the lazy dog.',
	'The quick brown fox jumped over the hill to fetch a pail of water.',
	'Jack and Jill ran up the hill to fetch a pail of water.',
	'Jack and Jill ran up the lazy dog.'
 ]
```
# Notes #

This module is still under development and is mostly for me to play around with and learn Markov Chains. Cheers.