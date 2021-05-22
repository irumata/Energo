import csv
from collections import Counter
import numpy as np
from tensorflow.keras.utils import to_categorical

csv_1 = "Аварии_погода_САЦ_2020.xlsx - Аварии_2020_Природные.csv"
csv_2 = "Аварии_Причины_САЦ_2020.xlsx - Аварии 2020.csv"
file_stat = "stat.txt"
features = []
features_dict = {
    "Атмосферные перенапряжения (гроза)" : 0,
    "Воздействие животных и птиц" : 1,
    "Ветровые нагрузки" : 2,
    "Прочие воздействия неблагоприятных природных явлений " : 3,
    "Термическое повреждение, перегрев, пережог" : 4,
    "Гололедно-изморозевые отложения" : 5,
    "Пожары" : 4,
    "Природные пожары" : 4,
    "Падение деревьев (природные)" : 2,
    "Взрыв, загорание, пожар" : 4,
    "Погодные явления" : 3,
    "Разрушение фундамента, строительных конструкций, ослабление крепления оборудования к фундаменту": 6,
    "Гололёдообразование" : 5,
    "Паводок" : 7,
    "Воздействие повторяющихся стихийных явлений" : 3,
}

csv_1_writerows = []
with open(csv_1) as csvfile:
    csv_1_reader = csv.reader(csvfile)
    for row in csv_1_reader:
        #print(row[2])
        features.append(row[2])
        if row[2] in features_dict.keys():
            temp_row = row
            temp_row.extend(list(to_categorical(features_dict[row[2]])))
            csv_1_writerows.append(temp_row)

csv_2_writerows = []
with open(csv_2) as csvfile:
    csv_1_reader = csv.reader(csvfile)
    for row in csv_1_reader:
        #print(row[2])
        features.append(row[2])
        if row[2] in features_dict.keys():
            temp_row = row
            temp_row.extend(list(to_categorical(features_dict[row[2]])))
            csv_2_writerows.append(temp_row)

with open(csv_1.rsplit(".",1)[0] + "output.csv", "w") as f:
    writer = csv.writer(f, delimiter ='$')
    writer.writerows(csv_1_writerows)

with open(csv_2.rsplit(".",1)[0] + "output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(csv_2_writerows, delimiter ='$')

print("Counting marks")
counts = Counter(features)

print("Zipping Values")
labels, values = zip(*counts.items())

# sort your values in descending order
print("Sorting Values")
indSort = np.argsort(values)[::-1]

# rearrange your data
labels = np.array(labels)[indSort]
values = np.array(values)[indSort]
indexes = np.arange(len(labels))

with open(file_stat,'w') as f:
    for i in range(0,len(labels)):
        print(labels[i],":",values[i])
        f.write(str(str(labels[i])+":"+str(values[i])+"\n"))