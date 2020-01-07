from Prepare_Multi_Span import speakers

import json
import csv
import codecs


# ----------------------------------------这一块是制作CSV文件------------------------------------------- #
class SentenceAndLabSpeakers(object):
    def __init__(self, speaker_list, progress=0):

        self.progress = progress
        self.speaker_list = speaker_list

        contexts = speaker_list[self.progress]['contexts']
        problem = speaker_list[self.progress]['problem']
        answer = speaker_list[self.progress]['answer']
        pos_istart = speaker_list[self.progress]['pos_istart']
        pos_iend = speaker_list[self.progress]['pos_iend']

        # 这儿重新定义了开始位置，其目的是将开始位置组转化为字符串
        new_pos_istart = ""
        for i in range(len(pos_istart)):
            if i == len(pos_istart)-1:
                new_pos_istart += str(pos_istart[i])
            else:
                new_pos_istart += str(pos_istart[i])+','

        # 这儿重新定义了结束位置，其目的是将结束位置转化为字符串
        new_pos_iend = ""
        for i in range(len(pos_iend)):
            if i == len(pos_iend)-1:
                new_pos_iend += str(pos_iend[i])
            else:
                new_pos_iend += str(pos_iend[i])+','

        row = [self.progress, contexts, problem, answer, new_pos_istart, new_pos_iend]

        # 接下来的if-else是将得到的结果写入csv文件中；其中，if写入的是预测文件，else写入的是训练文件
        if self.progress % 10 == 0:
            with open('Intermediate_results/prediction.csv', 'a', encoding='utf-8', newline='') as csvfile2:
                csv.register_dialect('pipes', delimiter='|')
                spamwriter1 = csv.writer(csvfile2, 'pipes', quoting=csv.QUOTE_MINIMAL)
                spamwriter1.writerow(row)
        else:
            with open('Intermediate_results/training.csv', 'a', encoding='utf-8', newline='') as csvfile2:
                csv.register_dialect('pipes', delimiter='|')
                spamwriter1 = csv.writer(csvfile2, 'pipes', quoting=csv.QUOTE_MINIMAL)
                spamwriter1.writerow(row)


# ----------------------------------------------------------------------------------------- #
# 这个方法是对某条语料进行处理
def split(row):
    tokens = row.split('|')
    contexts = tokens[1]
    problem = tokens[2]
    answer = tokens[3]
    pos_istart = tokens[4]
    pos_iend = tokens[5]

    return [contexts, problem, answer, pos_istart, pos_iend]


# 这是制作一个语料集
def read_samples(result_file, title="English"):

    res = dict()
    res["title"] = title
    res["paragraphs"] = []

    with open(result_file, "r", encoding='utf-8') as fin:
        lines = fin.readlines()
        labels = [split(line) for line in lines]

    for i in range(len(labels)):
        para_entry = dict()
        para_entry["uid"] = i
        para_entry["contexts"] = labels[i][0].strip()
        para_entry["problem"] = labels[i][1].strip()
        para_entry["answer"] = labels[i][2].strip()
        para_entry["pos_istart"] = labels[i][3].strip().split(',')
        para_entry["pos_iend"] = labels[i][4].strip().rstrip("\n").split(',')

        res["paragraphs"].append(para_entry)
    return res


def training_example():
    res = read_samples("Intermediate_results/training.csv")
    out = {"data":[res], "version":"English_squad_v1.0"}
    with open("Intermediate_results/train.json", "w", encoding='utf-8') as fout:
        fout.write(json.dumps(out, ensure_ascii=False))


def prediction_example():
    res = read_samples("Intermediate_results/prediction.csv")
    out = {"data":[res], "version":"English_squad_v1.0"}
    with open("Intermediate_results/prediction.json", "w", encoding='utf-8') as fout:
        fout.write(json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    for i in range(len(speakers)):
        SentenceAndLabSpeakers(speakers, progress=i)

    training_example()
    prediction_example()



