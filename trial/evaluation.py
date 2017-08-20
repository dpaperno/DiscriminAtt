#!/usr/bin/env python
import sys
import os
import os.path
import csv

def f1_score(evaluation):

    tp = 0
    fp = 0
    fn = 0

    for i in evaluation.values():
            if i[0] == i[1]:
                tp = tp+1
            elif i[0] == 1:
                fp = fp+1
            elif i[0] == 0:
                fn = fn+1

    if tp>0:
        precision=float(tp)/(tp+fp)
        recall=float(tp)/(tp+fn)
        f1 = 2*((precision*recall)/(precision+recall))
        return f1
    else:
        return 0

# as per the metadata file, input and output directories are the arguments
[_, input_dir, output_dir] = sys.argv

# unzipped submission data is always in the 'res' subdirectory
# https://github.com/codalab/codalab-competitions/wiki/User_Building-a-Scoring-Program-for-a-Competition#directory-structure-for-submissions
submission_file_name = 'answer.txt'
submission_dir = os.path.join(input_dir, 'res')
submission_path = os.path.join(submission_dir, submission_file_name)
if not os.path.exists(submission_path):
    message = "Expected submission file '{0}', found files {1}"
    sys.exit(message.format(submission_file_name, os.listdir(submission_dir)))
evaluation = {}
with open(submission_path) as submission_file:
    reader = csv.reader(submission_file)
    i = 0
    for row in reader:
        i = i+1
        a = int(row[3])
        evaluation[i] = [a]

# unzipped reference data is always in the 'ref' subdirectory
# https://github.com/codalab/codalab-competitions/wiki/User_Building-a-Scoring-Program-for-a-Competition#directory-structure-for-submissions
truth = []
with open(os.path.join(input_dir, 'ref', 'truth.txt')) as truth_file:
    reader = csv.reader(truth_file)
    i = 0
    for row in reader:
        i = i+1
        a = int(row[3])
        evaluation[i].append(a)

# the scores for the leaderboard must be in a file named "scores.txt"
# https://github.com/codalab/codalab-competitions/wiki/User_Building-a-Scoring-Program-for-a-Competition#directory-structure-for-submissions
with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
    score = f1_score(evaluation)
    output_file.write("f1:{0}\n".format(score))
