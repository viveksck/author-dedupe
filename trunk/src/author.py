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
        name_str = re.sub(r'[()\'"?~*!@#$\%^&]', '', name_str)
        name_str = re.sub(r'\s+', ' ', name_str)
        name_str = re.sub(r' -|- ', ' ', name_str)
        name_str = re.sub(r'^ | $', '', name_str)
        m = re.match('(.+)\s+(.+)', name_str)
        if not m:
            msg = "Cannot split '%s' into first and last names" % name_str
            raise MalformedAuthorName(msg)
        self.first_name = m.group(1)
        self.last_name = m.group(2)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name()

    def clean_first_names(self):
        name = re.sub(r'(Dr|Mr|Mrs|Ms). ', '', self.first_name)
        name_parts = re.split(r'[ -]+', name)
        name_parts = [n for n in name_parts if n]
        if name_parts:
            name_parts[0] = nick_names.get(name_parts[0], name_parts[0])
        return name_parts

    def token(self):
        t = "%s_%s" % (self.last_name, self.first_name[0])
        t = re.sub(r'\W', '', t)
        if len(t) < 3:
            msg = "Cannot create token for '%s'." % self
            raise MalformedAuthorName(msg)
        return t.lower()

