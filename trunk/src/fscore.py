#!/usr/bin/python
import re, sys


me_to_doc = {}
truth_to_doc = {}
truth_to_me = {}


for line in sys.stdin:
    truth, me = line.split("\t")
    me_to_doc.setdefault(me, []).append(True)
    truth_to_doc.setdefault(truth, []).append(True)
    truth_to_me.setdefault(truth, {}).setdefault(me, []).append(True)

def get_f_cell(truth, me):
    n1 = float(len(truth_to_me[truth].get(me, [])))
    n2 = float(len(me_to_doc[me]))
    n3 = float(len(truth_to_doc[truth]))
    precision = n1 / n2
    recall = n1 / n3
    return (2 * precision * recall) / (precision + recall)

def get_f_best(truth):
    best_fscore = -1
    for me in truth_to_me[truth]:
        fscore = get_f_cell(truth, me)
        if fscore > best_fscore:
            best_fscore = fscore
    return best_fscore

total_true = 0.
for truth, docs in truth_to_doc.items():
    total_true += float(len(docs))

overall_f = 0
for truth, docs in truth_to_doc.items():
    fscore = get_f_best(truth)
    prop_true = len(docs) / total_true
    overall_f += (prop_true * fscore)

print overall_f
