#!/usr/bin/env python
import sys
import os
import os.path
import csv

def f1_score(evaluation):

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for i in evaluation.values():
            if i[0] == i[1] and i[1] == 1: 
                tp = tp+1
            if i[0] == i[1] and i[1] == 0: 
                tn = tn+1
            elif i[0] != i[1] and i[1] == 1: 
                fp = fp+1
            elif i[0] != i[1] and i[1] == 0: 
                fn = fn+1
    if tp>0:
        precision=float(tp)/(tp+fp)
        recall=float(tp)/(tp+fn)
        f1_positives = 2*((precision*recall)/(precision+recall))
    if tn>0:
        precision=float(tn)/(tn+fn)
        recall=float(tn)/(tn+fp)
        f1_negatives = 2*((precision*recall)/(precision+recall))
    if f1_positives and f1_negatives:
        f1_average = (f1_positives+f1_negatives)/2.0
        return f1_average
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
        if len(row) != 4:
            message = "Submission file has row of length "+str(len(row))+", len 3 needed."
            sys.exit(message)
        i = i+1
        if type(int(row[3])) != int:
            message = "Value is not of type int."
            sys.exit(message)
        a = int(row[3])
        evaluation[i] = [a]

# unzipped reference data is always in the 'ref' subdirectory
# https://github.com/codalab/codalab-competitions/wiki/User_Building-a-Scoring-Program-for-a-Competition#directory-structure-for-submissions
with open(os.path.join(input_dir, 'ref', 'truth.txt')) as truth_file:
    reader = csv.reader(truth_file)
    i = 0
    for row in reader:
        if len(row) != 4:
            message = "Truth file has row of length "+str(len(row))+", len 3 needed."
            sys.exit(message)
        i = i+1
        if type(int(row[3])) != int:
            message = "Value is not of type int."
            sys.exit(message)
        a = int(row[3])
        evaluation[i].append(a)

if not evaluation:
    message = "evaluation empty"
    sys.exit(message)

for v in evaluation.values():
    if len(v) != 2:
        message = "Length of value must 2."
        sys.exit(message)

# the scores for the leaderboard must be in a file named "scores.txt"
# https://github.com/codalab/codalab-competitions/wiki/User_Building-a-Scoring-Program-for-a-Competition#directory-structure-for-submissions


with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
    score = f1_score(evaluation)
    output_file.write("correct:{0}\n".format(score))

with open(os.path.join(output_dir, 'stderr.txt'), 'w') as stderr_file:
    score = f1_score(evaluation)
    stderr_file.write('output from scoring function ='+str(score)+'\n')
    stderr_file.write("correct:{0}\n".format(score))

