### 1. Cleaning and Parsing ###
Name strings are stripped of titles (e.g. Mr., Dr.), special characters are removed, spacing and capitalization is standardized, common nick names are replaced with full names, etc.

A first name and a last name are extracted from each name string. In general, the characters appearing after the last space are said to be the last name, and the characters appearing before the last space (which may include middle initials and spaces) can be referred to as the first name. However, if the name string contains a comma, the last name appears before the comma and the first name after.

### 2. Top Level Partitioning ###
Form partition _P_ by assigning two name strings to the same part iff they share a last name and they share the first character of their first names. No further effort is made to merge name strings assigned to separate parts of _P_. This ensures the computation remains tractable, since the remaining steps run in O(n<sup>2</sup>) time, or in O(n<sup>3</sup>) time if caching is not used.

Steps 3 - 5 are executed once for each of _P_'s parts.

### 3. Merging Equivalent Names ###
Consider name strings to be composed of words and initials, with spaces, hyphens and periods acting as delimiters. Words have strictly more than one character, whereas initials contain only one character. Only initials may be followed by periods.

Let "pieces" refer to the words and initials of a name string. If two pieces are both words or both initials, then they are compatible if and only if they are the same (i.e. character equivalent). If one piece is a word while the other an initial, then they are compatible if and only if the first letter of the word is the same as the initial.

Two name strings are said to be compatible iff the sequences of their pieces are compatible. Two sequences of pieces of different lengths are compatible iff the shorter sequence is compatible with some subsequence of the longer sequence. Two sequences of pieces of the same length are compatible iff their corresponding pieces are all compatible.

Two name strings, _a_ and _b_, are equivalent iff for any other name string _c_ (found in the same part of partition _P_), _a_ is compatible with _c_ iff _b_ is compatible with _c_.

Apply this notion of equivalence to induce a partition _Q_ on each part of partition _P_.

### 4. Merging Partitions ###
Name string _a_ is said to be stricter than name string _b_ iff for any name string _c_  if _a_ and _c_ are compatible, then _b_ and _c_  are compatible.

Merge any two parts of _Q_, _q1_ and _q2_, if each name string in _q2_ is stricter than each name string in _q1_, and _q2 is the only partition for which this holds_.

### 5. Iterating ###
Repeat step 4 a few times, or until executing step 4 does not alter partition _Q_. Then, repeat steps 3 - 5 for each remaining part of P.