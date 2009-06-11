import collections


class Output():
    def __init__(self, out_base, authors):
        self.out_base = out_base
        self.authors = authors

    def convert_names(self):
        print "outputing author names"
        out_handle = open(self.out_base, "w")
        for a in self.authors:
            out_handle.write("%30s  -->  %s\n" % (a.original_name, a.merged_name))

    def dedupe_output(self):
        print "outputing author names"
        out_handle = open(self.out_base, "w")
        import re
        for a in self.authors:
            name = a.merged_name.title()
            name = re.sub(r'(\b\w) ', r'\1. ', name)
            out_handle.write("%s\n" % name)

    def output_need_merge(self):
        truth_to_authors = {}
        for a in self.authors:
            truth_to_authors.setdefault(a.truth, []).append(a)

        def all_same_prediction(authors):
            if not authors:
                return True #vacuously true
            prev = authors[0]
            for a in authors:
                if a.merged_name != prev.merged_name:
                    return False
            return True

        def unique_list(l):
            temp = {}
            for i in l:
                temp[i] = True
            return sorted(temp.keys())

        out_handle = open(self.out_base + ".nm", "w")
        for t, authors in truth_to_authors.items():
            if not all_same_prediction(authors):
                names = [a.merged_name for a in authors]
                out_handle.write("%s\n" % ", ".join(unique_list(names)))

    def output_need_split(self):
        prediction_to_authors = {}
        for a in self.authors:
            prediction_to_authors.setdefault(a.merged_name, []).append(a)

        def all_same_truth(authors):
            if not authors:
                return True #vacuously true
            prev = authors[0]
            for a in authors:
                if a.truth != prev.truth:
                    return False
            return True

        out_handle = open(self.out_base + ".ns", "w")
        for p, authors in prediction_to_authors.items():
            if not all_same_truth(authors):
                names = [a.original_name for a in authors]
                out_handle.write("%s\n" % ", ".join(names))

    def compute_performance(self):
        me_to_doc = collections.defaultdict(float)
        truth_to_doc = collections.defaultdict(float)
        truth_to_me = {}

        for a in self.authors:
            me_to_doc[a.merged_name] += 1
            truth_to_doc[a.truth] += 1
            truth_to_me.setdefault(a.truth, collections.defaultdict(float))[a.merged_name] += 1

        def get_f_cell(truth, me):
            n1 = truth_to_me[truth].get(me, [])
            n2 = me_to_doc[me]
            n3 = truth_to_doc[truth]
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
        for truth, num_docs in truth_to_doc.items():
            total_true += num_docs

        overall_f = 0
        for truth, num_docs in truth_to_doc.items():
            def f_cell_bound(me):
                return get_f_cell(truth, me)
            fscore = max(truth_to_me[truth].keys(), key=f_cell_bound)
            fscore = get_f_best(truth)
            prop_true = num_docs / total_true
            overall_f += prop_true * fscore

        print "f-score: ", overall_f

    def output_all(self):
#        self.compute_performance()
#        self.output_need_split()
#        self.output_need_merge()
#        self.convert_names()
        self.dedupe_output()



