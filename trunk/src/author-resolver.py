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

import sys, re, random
from collections import defaultdict
import author
import info_comparator
import flln_partition
import speller
import output


ordered_authors = []
token_to_authors = defaultdict(set)
parts = set()

def load_names(in_file):
    print "loading names"
    names_handle = open(in_file)

    for n in names_handle:
#        truth, name, article = n.rstrip().split("\t")
        name = n.rstrip()
        try:
            a = author.Author(name)
#            a.truth = truth
#            a.article = article

            ordered_authors.append(a)
            token_to_authors[a.token()].add(a)
        except author.MalformedAuthorName, e:
            print e

def correct_first_names():
    print "correcting first names"
    #TODO: correct middle names too
    for t, authors in token_to_authors.iteritems():
        first_map = defaultdict(int)
        for a in authors:
            first_map[a.first_name] += 1
        sp = speller.SpaceSpeller(first_map)
        for a in authors:
            if len(a.first_name) < 5:
                continue
            candidates = sp.candidates(a.first_name)
            if candidates and candidates[0][0] >= first_map[a.first_name]:
                first_map[a.first_name] -= 1
                a.first_name = candidates[0][1]
                first_map[a.first_name] += 1

def merge_names():
    print "merging author names"
    info_comp = info_comparator.InfoComparator(ordered_authors)
    for t, authors in token_to_authors.iteritems():
        fp = flln_partition.FllnPartition(authors, info_comp)
        fp.merge()
        parts.update(fp.parts)

def correct_last_names():
    print "correcting last names"

    info_comp = info_comparator.InfoComparator(ordered_authors)

    last_name_parts = defaultdict(int)
    for p in parts:
        last_name_parts[p.last_name()] += 1

    # provides other possible last names for an author, based on reverse_token
    # (e.g. j_smith)
    var_name_map = defaultdict(lambda: defaultdict(int))

    def update_var_map(author_iter, delta):
        for a in author_iter:
            var_name_map[a.reverse_token()][a.var_last()] += delta

    update_var_map(ordered_authors, 1)

    def change_last_name(part, new_last):
        update_var_map(p, -1)
        token_to_authors[p.token()].difference_update(part.authors)
        part.change_last_name(new_last)
        update_var_map(p, 1)
        token_to_authors[p.token()].update(p.authors)
        flln_partition.FllnPartition(token_to_authors[part.token()], info_comp).merge()

    ln_speller = speller.Speller(last_name_parts)
    for p in parts:
        # don't even try to correct last names that are similar to more 
        # than one other last name
        if len(ln_speller.candidates(p.last_name())) > 1:
            continue

        # the total number of characters in common is hard to improve upon, as a
        # threshold for determining name similarity
        if len(p.first_name() + p.last_name()) < 10:
            continue

        sp = speller.Speller(var_name_map[p.reverse_token()])
        candidates = sp.candidates(p.var_last())
        if (not candidates) or (candidates[0][0] < var_name_map[p.reverse_token()][p.var_last()]):
            continue

        corrected_ln = p.last_name()[0] + candidates[0][1]
        change_last_name(p, corrected_ln)

def dropped_first_names():
    token_to_parts = defaultdict(set)
    for p in parts:
        token_to_parts[p.token()].add(p)

    last_name_count = defaultdict(int)
    for t in token_to_parts.keys():
        last_name = t[:-2]
        last_name_count[last_name] += 1

    info_comp = info_comparator.InfoComparator(ordered_authors)

    for p in parts:
        # i.e. only 2 of 26 characters are paired with this last name
        if len(p.middle_names()) == 1 and last_name_count[p.last_name()] <= 2:
            m_token = "%s_%s" % (p.last_name(), p.middle_names()[0])
            if m_token != p.token() and m_token in token_to_parts and\
                len(token_to_parts[m_token]) == 1 and (not min(token_to_parts[m_token]).middle_names()):
                p.drop_first_name()
                token_to_authors[p.token()].difference_update(p.authors)
                token_to_authors[m_token].update(p.authors)
                flln_partition.FllnPartition(token_to_authors[m_token], info_comp).merge()               


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s <names_in_file> <names_out_file>" % sys.argv[0]
    else:
        load_names(sys.argv[1])
        correct_first_names()
        merge_names()
        correct_last_names()
        dropped_first_names()
        output.Output(sys.argv[2], ordered_authors).output_all()

