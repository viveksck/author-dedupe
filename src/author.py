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
import nick_names


class MalformedAuthorName(Exception):
    pass

class Author():
    def __init__(self, name_str):
        self.original_name = name_str
        self.merged_name = name_str #this gets overwritten
        self.first_name, self.middle_names, self.last_name, self.suffix = self.split_name()

    def __str__(self):
        return self.original_name

    def clean_name(self):
        name_str = re.sub(r'[{}_()\'"?~*!@#$\%^&]', '', self.original_name)
        name_str = re.sub(r'\s+', ' ', name_str)
        name_str = re.sub(r' -|- ', ' ', name_str)
        name_str = re.sub(r'(?i)^(Dr|Mr|Mrs|Ms)\. ', '', name_str)
        name_str = re.sub('^([A-Z])([A-Z]) ', r'\1. \2. ', name_str)
        name_str = re.sub('^([A-Z][a-z]+)\. ', r'\1 ', name_str)
        name_str = re.sub('\. *', ' ', name_str)
        name_str = re.sub(' ((van|de|del|da|do|el|la|di|von|der) )+', ' ', name_str)
        name_str = re.sub(r'^ +| +$', '', name_str)
        name_str = re.sub(r'\s+', ' ', name_str)
        return name_str.lower()

    def split_name(self):
        cname = self.clean_name()

        suffix = ""
        m_suffix = re.search(r'(?i)^(.*) (jr|iii|iv)$', cname)
        if m_suffix:
            cname, suffix = m_suffix.group(1), m_suffix.group(2)

        not_last_name, last_name = "", ""

        # smith, john c
        m = re.match('(?P<last>.+), (?P<first>.+)', cname)
        if not m:
            # smith j c
            m = re.match('^(?P<last>\S{2,}) (?P<first>(?:[a-z] )*[a-z])$', cname)
        if not m:
            # j c smith
            m = re.match('^(?P<first>.+?) (?P<last>\S+)$', cname)
        if not m:
            msg = "Cannot split '%s' into first and last names" % self
            raise MalformedAuthorName(msg)

        not_last_name, last_name = m.group("first"), m.group("last")

        name_parts = re.split(r'[ -]+', not_last_name)
        name_parts = [n for n in name_parts if n]
        first_name = nick_names.nick_names.get(name_parts[0], name_parts[0])
        middle_names = name_parts[1:]

        return first_name, middle_names, last_name, suffix
        

    def reverse_token(self):
        return self.first_name + "_" + self.last_name[0]

    def var_last(self):
        return self.last_name[1:]

    def token(self):
        t = "%s_%s" % (self.last_name, self.first_name[0])
        t = re.sub(r'\W', '', t)
        if len(t) < 3:
            msg = "Cannot create token for '%s'." % self
            raise MalformedAuthorName(msg)
        return t.lower()
