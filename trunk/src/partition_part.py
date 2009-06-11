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
        self.authors = set()

    def __str__(self):
        return self.full_name()

    def __iter__(self):
        return self.authors.__iter__()

    def add(self, a):
        self.authors.add(a)

    def extend(self, source_part):
        self.authors.update(source_part.authors)

    def first_name(self):
        return max([a.first_name for a in self.authors], key=len)

    def middle_names(self):
        return max([a.middle_names for a in self.authors], key=len)

    def last_name(self):
        #any author will do
        return min(self.authors).last_name

    def reverse_token(self):
        return "%s_%s" % (self.first_name(), self.last_name()[0])

    def var_last(self):
        #any author will do
        return min(self.authors).var_last()

    def token(self):
        #any author will do
        return min(self.authors).token()

    def full_name(self):
        middle_name = " ".join(self.middle_names())
        if middle_name:
            middle_name += ' '
        return "%s %s%s" % (self.first_name(), middle_name, self.last_name())

    def change_last_name(self, new_last):
        for a in self.authors:
            a.last_name = new_last

    def drop_first_name(self):
        new_first_name = self.middle_names()[0]
        new_middle_names = self.middle_names()[1:]
        for a in self.authors:
            a.first_name = new_first_name
            a.middle_names = new_middle_names
