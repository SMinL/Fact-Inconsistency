import sys
import csv
import jsonlines


csv.field_size_limit(sys.maxsize)

real_fact_labels = []#prediction results
prediction_result_of_clinical = []#ground truth
f = open('manucal_label_by_myself.csv','r')
for i,l in enumerate(f):
    if i > 0:
       line = l.strip().split('\t')       
       if line[-5] == 'positive':
          prediction_result_of_clinical.append('1')
       elif line[-5] == 'negative':
          prediction_result_of_clinical.append('0')

       if line[-2] == 'positive':
          real_fact_labels.append('1')
       elif line[-2] == 'negative':
          real_fact_labels.append('0')


real_clinical_results = []
with open("../test.top5.json", "r+", encoding="utf8") as f:
    for item in jsonlines.Reader(f):
        if item['label'] == 'positive':
           real_clinical_results.append('1')
        else:
           real_clinical_results.append('0')

clinical_based_facts = []

for p,r in zip(prediction_result_of_clinical,real_clinical_results):
    if p == r:
       clinical_based_facts.append('1')
    else:
       clinical_based_facts.append('0')

match = []
predict_positive = []
real_positive_in_predict = []
real_positive = []
predict_positive_in_real = []
print(real_fact_labels)
print(clinical_based_facts)

for i, inp in enumerate(zip(real_fact_labels,clinical_based_facts)):
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

acc = len(match)/float(len(real_fact_labels))
print('acc:',acc)

precision = len(real_positive_in_predict)/float(len(predict_positive))

print('precision:',precision)

recall = len(predict_positive_in_real)/float(len(real_positive))

print('recall:',recall)

F1 = 2 * precision * recall / (precision + recall)

print('F1 score',F1)

