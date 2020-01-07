#!/usr/bin/env python
# 这是做数据增强的
import ast
import re
from tqdm import tqdm_notebook


def kmp(mom_string, son_string):
    # 传入一个母串和一个子串
    # 返回子串匹配上的第一个位置，若没有匹配上返回-1
    test = ''
    if type(mom_string) != type(test) or type(son_string) != type(test):
        return -1
    if len(son_string) == 0:
        return 0
    if len(mom_string) == 0:
        return -1
    # 求next数组
    next = [-1] * len(son_string)
    if len(son_string) > 1:  # 这里加if是怕列表越界
        next[1] = 0
        i, j = 1, 0
        while i < len(son_string) - 1:  # 这里一定要-1，不然会像例子中出现next[8]会越界的
            if j == -1 or son_string[i] == son_string[j]:
                i += 1
                j += 1
                next[i] = j
            else:
                j = next[j]

    # kmp框架
    m = s = 0  # 母指针和子指针初始化为0
    while (s < len(son_string) and m < len(mom_string)):
        # 匹配成功,或者遍历完母串匹配失败退出
        if s == -1 or mom_string[m] == son_string[s]:
            m += 1
            s += 1
        else:
            s = next[s]

    if s == len(son_string):  # 匹配成功
        return m - s
    # 匹配失败
    return -1


# 通过竖杠划分的片段个数来判断语句是否完整，从而进行语料的筛选清洗   --Designed by William Baker
def data_augmentation(saved_file="Intermediate_results/1.txt"):

    combined_res = []
    uid = 0

    with open(saved_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()  # 去除首尾空格    --Noted by William Baker
            line = line.lower()  # 转换字符串中所有大写字符为小写  --Noted by William Baker

            # line = line.strip()  # 首先去除首尾的空格  --Noted by William Baker
            tokens = line.split('|')
            if len(tokens) == 0:
                continue
            elif len(tokens) == 1:
                continue
            elif len(tokens) == 2:
                continue
            elif len(tokens) == 3:
                # 得到文本、问题以及答案
                context = tokens[0].strip()   # strip()用于去除首尾的空格   --Noted by William Baker
                question = tokens[1].strip()
                answer = tokens[2].strip()

                # 对文本进行处理
                context = list(context)
                context = ["," if x == "，" else x for x in context]
                context = ["." if x == "。" else x for x in context]
                context = ["?" if x == "？" else x for x in context]
                context = [";" if x == "；" else x for x in context]
                context = ''.join(context)
                context = context.strip()
                context = context.replace("\"", "")
                context = context.replace("\\", "")
                context = context.replace("\'", " ")
                # context = context.replace("(", " ")
                # context = context.replace(")", " ")
                # context = context.replace("（", " ")
                # context = context.replace("）", " ")

                # 对问题的最后一个字符做处理，即将最后一个字符变为英文?
                end_char = len(question)
                char_question_end = question[end_char - 1]
                a = re.match("[A-Z]", char_question_end)
                b = re.match("[a-z]", char_question_end)
                c = re.match("[0-9]", char_question_end)

                if ((a != None) or (b != None) or (c != None)):
                    question = question + '?'
                else:
                    question = list(question)
                    question[end_char - 1] = '?'
                    question = ''.join(question)

                question = question.strip()
                question = question.replace("\"", "")
                question = question.replace("\\", "")
                question = question.replace("\'", " ")
                # question = question.replace("(", " ")
                # question = question.replace(")", " ")
                # question = question.replace("（", " ")
                # question = question.replace("）", " ")

                # 这儿是对答案进行处理
                answer = list(answer)
                answer = ["," if x == "，" else x for x in answer]
                answer = ["." if x == "。" else x for x in answer]
                answer = ["?" if x == "？" else x for x in answer]
                answer = [";" if x == "；" else x for x in answer]
                answer = ''.join(answer)
                answer = answer.replace("\"", "")
                answer = answer.replace("\\", "")
                answer = answer.replace("\'", " ")
                # answer = answer.replace("(", " ")
                # answer = answer.replace(")", " ")
                # answer = answer.replace("（", " ")
                # answer = answer.replace("）", " ")
                answer = answer.split(';')

                # 接下来调用大神KMP算法进行切分
                start_position = []
                end_position = []
                new_answer = ""
                k = 0
                for i in answer:
                    Fragment = i.strip()
                    position = kmp(context, Fragment)

                    if position in start_position:
                        continue
                    elif len(Fragment)<=2:
                        continue
                    else:
                        start_position.append(position)
                        end_position.append(position + len(Fragment) - 1)

                        if k == 0:
                            new_answer = Fragment
                            k = k + 1
                        else:
                            new_answer = new_answer + ";" + Fragment
                            k = k + 1

                # 保存一下
                if -1 in start_position:
                    continue
                elif len(start_position) == 0:
                    continue
                else:
                    try:
                        res = {
                            'uid': uid,
                            'contexts': context,
                            'problem': question,
                            'answer': new_answer,
                            'pos_istart': start_position,
                            'pos_iend': end_position
                        }
                        combined_res.append(res)
                        uid = uid + 1
                    except:
                        continue

    return combined_res


if __name__ == '__main__':
    augmented_data = data_augmentation()
    with open("Prepare_Multi_Span.py", "w", encoding='utf-8') as fout:
        fout.write("speakers=[")
        for item in tqdm_notebook(augmented_data):
            fout.write(item.__repr__())
            fout.write(',\n')
        fout.write(']')



