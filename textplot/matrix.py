

import numpy as np
import textplot.utils as utils

from clint.textui import progress
from itertools import combinations
from collections import OrderedDict
from scipy.misc import comb


class Matrix:


    def __init__(self, text):

        """
        Store the text.

        :param text: A text instance.
        """

        self.text = text


    def key(self, term1, term2):

        """
        Get a unique key for a term pair.

        :param term1: The first term.
        :param term2: The second term.
        """

        return '_'.join(sorted((term1, term2)))


    def set_pair(self, term1, term2, **kwargs):

        """
        Set the value for a pair of terms.

        :param term1: The first term.
        :param term2: The second term.
        """

        k = self.key(term1, term2)
        d = self.text.score_braycurtis(term1, term2, **kwargs)
        self.pairs[k] = d


    def get_pair(self, term1, term2):

        """
        Get the value for a pair of terms.

        :param term1: The first term.
        :param term2: The second term.
        """

        k = self.key(term1, term2)
        if k in self.pairs: return self.pairs[k]
        else: return None


    def anchored_pairs(self, anchor):

        """
        Compute the pairs between an anchor term and all other terms.

        :param anchor: The anchor term.
        """

        pairs = OrderedDict()
        for term in self.terms:
            score = self.get_pair(anchor, term)
            if score: pairs[term] = score

        return utils.sort_dict(pairs)


    def index(self, terms=None, **kwargs):

        """
        Index all word pair distances.

        :param terms: A list of terms to index.
        """

        self.pairs = {}

        # Use all terms by default.
        self.terms = terms or self.text.terms.keys()
        pairs = comb(len(self.terms), 2)

        with progress.Bar(expected_size=pairs) as bar:

            i = 0
            for t1, t2 in combinations(self.terms, 2):

                self.set_pair(t1, t2, **kwargs)

                # Update progress.
                i += 1
                if i % 1000 == 0: bar.show(i)
