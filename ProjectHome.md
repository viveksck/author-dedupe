Slight variations in the spellings of people's names can make it difficult to tell which names refer to the same person. This problem is particularly striking when processing large sets of author names.

Author-Dedupe is Python software for merging author names which refer to the same person. Simple string matching via regular expressions is used, but that's just the start. Author-Dedupe then iteratively partitions the authors' names. The algorithm is detailed on the DedupeAlgorithm page.

Input is read from a file containing one author name per line. For each line of input, one line containing the corrected name is written to the output file. An example appears below.


---


**Sample Input**
```
Smith, J. Allyn
J. A. Smith
Joan A. Smith
Joan Smith
Jodie A. Smith
Jeff Smith
Smith, Jeffrey B.
Jeffrey H. Smith
Jeff H. Smith
J. H. Smith
John-David T. Smith
John D. Smith
J. D. T. Smith
J. -D. T. Smith
John Smith
Jack Smith
J. D. Smith
James L. Smith
J. Lleweilun Smith
J. L. Smith
James Smith
James E. Smith
J. E. Smith
James G. Smith
J. G. Smith
```


---


**Sample Output**
```
J. Allyn Smith
J. Allyn Smith
Joan A. Smith
Joan A. Smith
Jodie A. Smith
Jeffrey Smith
Jeffrey B. Smith
Jeffrey H. Smith
Jeffrey H. Smith
Jeffrey H. Smith
John D. T. Smith
John D. T. Smith
John D. T. Smith
John D. T. Smith
John D. T. Smith
John D. T. Smith
John D. T. Smith
James L. Smith
James L. Smith
James L. Smith
James Smith
James E. Smith
James E. Smith
James G. Smith
James G. Smith
```


---


