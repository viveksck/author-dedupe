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


import sys
import author
import flln_partition

token_to_authors = {}


def load_names(names_file):
    print "loading author names"
    names_handle = open(names_file)
    for n in names_handle:
        try:
            a = author.Author(n.rstrip())
            sim_authors = token_to_authors.setdefault(a.token(), [])
            sim_authors.append(a)
        except author.MalformedAuthorName, e:
            print e

def merge_names(out_file):
    print "merging author names"
    out_handle = open(out_file, "w")
    for t, authors in token_to_authors.iteritems():
        try:
            fp = flln_partition.FllnPartition(authors)
            fp.merge()
            fp.store(out_handle)
        except UnicodeEncodeError, e:
            print e


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <names_in_file> <names_out_file>" % sys.argv[0]
    else:
        load_names(sys.argv[1])
        merge_names(sys.argv[2])

