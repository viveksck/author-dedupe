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


class PartitionPart():
    def __init__(self):
        self.authors = []

    def add(self, a):
        self.authors.append(a)

    def extend(self, source_part):
        self.authors.extend(source_part.iter_authors())

    # The strictest (i.e. least-compatible) author comes first
    # in the author list, by virtue of the order in which authors are
    # added to it.
    #
    # TODO: Replace this authors list with an unordered set,
    # and don't rely on the order in which authors are added
    # to determine which author is the least-compatible. Instead
    # keep running store of the strictest author, and let
    # this authors "compatiblity fingerprint" server as the
    # fingerprint of the entire partition
    def fingerprint_id(self):
        return self.authors[0].numpy_id #hack

    def first_name(self):
        max_name = ""
        for a in self.authors:
            cur_name = " ".join(a.clean_first_names())
            if len(cur_name) > len(max_name):
                max_name = cur_name
        return max_name

    def last_name(self):
        first_name, last_name = self.authors[0].split_first_last()
        return last_name

    def full_name(self):
        return "%s %s" % (self.first_name(), self.last_name())

    def iter_authors(self):
        return self.authors

