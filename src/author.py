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
from nick_names import nick_names


class MalformedAuthorName(Exception):
    pass

class Author():
    def __init__(self, name_str):
        self.original_name = name_str
        self.merged_name = name_str #this gets overwritten

    def __str__(self):
        return self.original_name

    def clean_name(self):
        name_str = re.sub(r'[()\'"?~*!@#$\%^&]', '', self.original_name)
        name_str = re.sub(r'\s+', ' ', name_str)
        name_str = re.sub(r' -|- ', ' ', name_str)
        name_str = re.sub(r'^ | $', '', name_str)
        name_str = re.sub(r'(Dr|Mr|Mrs|Ms). ', '', name_str)
        name_str = re.sub('^([A-Z])([A-Z]) ', r'\1. \2. ', name_str)
        name_str = re.sub('^([A-Z][a-z]+)\. ', r'\1 ', name_str)
        return name_str.title()

    def split_first_last(self):
        cname = self.clean_name()
        m_comma = re.match('(.+), (.+)', cname)
        if m_comma:
            return m_comma.group(2), m_comma.group(1)

        m = re.match('(.+)\s+(.+)', cname)
        if m:
            return m.group(1), m.group(2)

        msg = "Cannot split '%s' into first and last names" % self
        raise MalformedAuthorName(msg)

    def clean_first_names(self):
        first_name, last_name = self.split_first_last()
        name_parts = re.split(r'[ -]+', first_name)
        name_parts = [n for n in name_parts if n]
        if name_parts:
            name_parts[0] = nick_names.get(name_parts[0], name_parts[0])
        return name_parts

    def token(self):
        first_name, last_name = self.split_first_last()
        t = "%s_%s" % (last_name, first_name[0])
        t = re.sub(r'\W', '', t)
        if len(t) < 3:
            msg = "Cannot create token for '%s'." % self
            raise MalformedAuthorName(msg)
        return t.lower()

