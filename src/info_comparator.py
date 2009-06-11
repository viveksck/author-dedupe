#!/usr/bin/python

# Copyright 2008, Jeffrey Regier, jeff [at] stat [dot] berkeley [dot] edu

# This file is part of Author-Dedupe.
#
# Author-Dedupe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Author-Dedupe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Author-Dedupe.  If not, see <http://www.gnu.org/licenses/>.

import sys, re
import author
import flln_partition
from collections import defaultdict


class Counter():
    map = defaultdict(int)
    total = 0

    def incr(self, key):
        self.map[key] += 1
        self.total += 1

    def get_prop(self, key):
        return self.map[key] / float(self.total)


class InfoComparator():
    """Evaluates the mutual information between two authors, given a training dataset"""

    fn_map, fl_map, ln_map = Counter(), Counter(), Counter()

    def __init__(self, authors):
       for a in authors:
            self.fl_map.incr(a.first_name[0])
            if len(a.first_name) > 1:
                self.fl_map.incr(a.first_name)
            for m in a.middle_names:
                self.fl_map.incr(m[0])
                if len(m) > 1:
                    self.fn_map.incr(m)
            self.ln_map.incr(a.last_name)

    def compare(self, p1, p2):
        def shorter(s1, s2):
            return s1 if len(s1) < len(s2) else s2

        fn = shorter(p1.first_name(), p2.first_name())
        f_map = self.fn_map if len(fn) > 1 else self.fl_map
        gen_prob = f_map.get_prop(fn)

        # assumes that fn and ln are independent, which may lead us to 
        # overestimate the similarity between two names. (initials are safer.)
        gen_prob *= self.ln_map.get_prop(p1.last_name())

        if len(p1.middle_names()) != len(p2.middle_names()):
            # this is a bit stricter than what we require for name compatibility
            return gen_prob

        for mi in range(len(p1.middle_names())):
            m = shorter(p1.middle_names()[mi], p2.middle_names()[mi])
            f_map = self.fn_map if len(fn) > 1 else self.fl_map
            gen_prob *= f_map.get_prop(m)

        return gen_prob
