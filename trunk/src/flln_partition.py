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


import re
import author
import partition_part
from collections import defaultdict


def compatible_names(a1, a2):
    def compatible_name_part(w1, w2):
        w1 = re.sub(r'\W', '', w1)
        w2 = re.sub(r'\W', '', w2)
        l = min(len(w1), len(w2))
        if not l:
            return False
        return w1[:l] == w2[:l]

    short, long = list(a1.middle_names), a2.middle_names
    if len(short) > len(long):
        return compatible_names(a2, a1)

    # the front first names must be compatible
    # (note: last names here are always equal)
    if not compatible_name_part(a1.first_name, a2.first_name):
        return False

    # try finding each middle name of long in short, and remove the
    # middle name from short if found
    for wl in long:
        if not short:
            break
        ws = short.pop(0)
        if not compatible_name_part(ws, wl):
            short.insert(0, ws)

    # true iff short is a compatible substring of long
    return short == []


class FllnPartition():
    """(first-letter-first-name, last-name) partition"""

    def __init__(self, authors, info_comp):
        self.info_comp = info_comp
        self.load_parts(authors)
        self.load_compat_mat(authors)

    def load_parts(self, authors):
        self.parts = set()
        def singleton_part(a):
            part = partition_part.PartitionPart()
            part.add(a)
            return part
        self.parts.update([singleton_part(a) for a in authors])

    def load_compat_mat(self, authors):
        self.compat_map = defaultdict(set)
        for a1 in authors:
            for a2 in authors:
                if compatible_names(a1, a2):
                    self.compat_map[a1].add(a2)
     
    def get_partition_compat(self, part):
        compat_maps = [self.compat_map[a] for a in part]
        return reduce(set.intersection, compat_maps)

    def stricter_than(self, less_p, more_p):
        less_compat = self.get_partition_compat(less_p)
        more_compat = self.get_partition_compat(more_p)
        return less_compat < more_compat

    def is_equivalent(self, p1, p2):
        compat1 = self.get_partition_compat(p1)
        compat2 = self.get_partition_compat(p2)
        return compat1 == compat2

    def target_equivalent(self, source_p):
        for p in self.parts:
            if p == source_p:
                continue
            if self.is_equivalent(source_p, p):
                return p

    def find_stricter(self, source_p):
        stricter = []
        for p in self.parts:
            if p == source_p:
                continue
            if self.stricter_than(p, source_p):
                stricter.append(p)
        return stricter

    def target_sole_stricter(self, source_p):
        stricter = self.find_stricter(source_p)
        if len(stricter) == 1:
            return stricter[0]
        elif len(stricter) > 1:
            for s in stricter:
                if self.info_comp.compare(source_p, s) < 7e-6:
                    return s

    def merge_iter(self, get_target_f):
        num_changes = 0
        # copy avoids a run time error when the set changes size
        for p in set.copy(self.parts):
            target = get_target_f(p)
            if target:
                target.extend(p)
                self.parts.remove(p)
                num_changes += 1
        return num_changes

    def merge(self):
        self.merge_iter(self.target_equivalent)

        #iteratively merge the parts into the stricter parts,
        #when there is only one stricter part
        while self.merge_iter(self.target_sole_stricter):
            pass

        #TODO: why doesn't it ever help to do this more than once?

        for part in self.parts:
            merged_name = part.full_name()
            for a in part:
                a.merged_name = merged_name

