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
from numpy import *


def compatible_names(a1, a2):
    short = a1.clean_first_names()
    long = a2.clean_first_names()

    if len(short) > len(long):
        return compatible_names(a2, a1)

    def comp_name(w1, w2):
        w1 = re.sub(r'\W', '', w1)
        w2 = re.sub(r'\W', '', w2)
        l = min(len(w1), len(w2))
        if not l:
            return False
        return w1[:l] == w2[:l]
 
    # the front first names must be compatible
    if not comp_name(short[0], long[0]):
        return False

    # try finding each word of long in short, and remove the
    # word from short if found
    for wl in long:
        if not short:
            break
        ws = short.pop(0)
        if not comp_name(ws, wl):
            short.insert(0, ws)

    # true iff short is a compatible substring of long
    return (short == [])

 
class FllnPartition():
    """(first-letter-first-name, last-name) partition
    """

    def __init__(self, authors):
        for a1_id in range(len(authors)):
            a1 = authors[a1_id]
            a1.numpy_id = a1_id #hack

        self.load_parts(authors)
        self.load_compat_mat(authors)

    def load_parts(self, authors):
        def singleton_part(a):
            part = partition_part.PartitionPart()
            part.add(a)
            return part
        self.parts = [singleton_part(a) for a in authors]

    def load_compat_mat(self, authors):
        self.compat_mat = zeros((len(authors), len(authors)))

        for a1_id in range(len(authors)):
            self.compat_mat[a1_id][a1_id] = 1
            for a2_id in range(len(authors)):
                if a2_id <= a1_id:
                    continue
                a1, a2 = authors[a1_id], authors[a2_id]
                if compatible_names(a1, a2):
                    self.compat_mat[a1_id][a2_id] = 1
                    self.compat_mat[a2_id][a1_id] = 1
     
    def stricter_than(self, less_p, more_p):
        less_id = less_p.fingerprint_id()
        more_id = more_p.fingerprint_id()
        if self.compat_mat[less_id, more_id] == 0:
            return False
        for a3_id in range(self.compat_mat.shape[0]):
            if self.compat_mat[less_id, a3_id] == 1 and self.compat_mat[more_id, a3_id] == 0:
                return False
        return True

    def is_equivalent(self, p1, p2):
        l1 = list(self.compat_mat[p1.fingerprint_id()])
        l2 = list(self.compat_mat[p2.fingerprint_id()])
        return l1 == l2

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

    def merge_iter(self, get_target_f):
        p_id = 0
        while p_id < len(self.parts):
            p = self.parts[p_id]
            target = get_target_f(p)
            if target:
                target.extend(p)
                del self.parts[p_id]
            else:
                p_id += 1

    def merge(self):
        self.merge_iter(self.target_equivalent)

        #iteratively merge the parts into the stricter parts,
        #when there is only one stricter part
        num_iters = 3
        for i in range(num_iters):
            self.merge_iter(self.target_sole_stricter)

        for part in self.parts:
            merged_name = part.full_name()
            for a in part.iter_authors():
                a.merged_name = merged_name

