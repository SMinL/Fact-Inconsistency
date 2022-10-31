import sys
import csv
import jsonlines

f = open('/home/lsm/code/2021/transformers/examples/pytorch/text-classification/scibert_for_sci/predict_v3/predict_results_None.txt','r')

all_lines  = []
for i,l in enumerate(f):
    if i > 0: 
       all_lines.append(l.strip().split('\t')[1])
print(len(all_lines))


fn  = open('number.txt','r')
numbers = [int(l.strip()) for l in fn]
examples = []
tag1 = 0
for n in numbers:
    tag2 = tag1 + n
#    print(tag1,tag2)
    examples.append(all_lines[tag1:tag2])
    tag1 = tag1 + n

assert len(examples) == len(numbers)

lines = []
for e in examples:
    cs = []
    for i in e:
        if 'contrasting'== i:
           cs.append('contrasting')
    if len(cs) >4:
       lines.append('0')
    else:
       lines.append('1')
    

test_tags = []
f = open('manucal_label_by_myself.csv','r')
for i,l in enumerate(f):
    if i > 0:
       line = l.strip().split('\t')[1]
       if line == 'positive':
          test_tags.append('1')
       else:
          test_tags.append('0')
match = []
predict_positive = []
real_positive_in_predict = []
real_positive = []
predict_positive_in_real = []

for i, inp in enumerate(zip(test_tags,lines)):
#    print(gold,test)
    gold,test = inp
    if gold == test:
       match.append('yes')
       print(i)
    if test == '1':
       predict_positive.append(test)
       if gold == '1':
          real_positive_in_predict.append(test)

    if gold == '1':
       real_positive.append(gold)
       if test == '1':
          predict_positive_in_real.append(test)

acc = len(match)/float(len(lines))
print('acc:',acc)

precision = len(real_positive_in_predict)/float(len(predict_positive))

print('precision:',precision)

recall = len(predict_positive_in_real)/float(len(real_positive))

print('recall:',recall)

F1 = 2 * precision * recall / (precision + recall)

print('F1 score',F1)


