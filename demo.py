
import tqdm

# 这个方法是对某条语料进行处理
def split(row):
    tokens = row.split('|')
    answer = tokens[3]
    return answer


# 这是制作一个语料集
def read_samples(result_file, title="English"):

    res = []

    with open(result_file, "r", encoding='utf-8') as fin:
        lines = fin.readlines()
        labels = [split(line) for line in lines]

    for i in range(len(labels)):
        para_entry = ''
        para_entry = labels[i]
        res.append(para_entry)

    print(res)
    file_handle = open("Intermediate_results/answer.txt", mode='w', encoding='utf-8')
    for item in res:
        file_handle.write(item.__repr__())
        file_handle.write('\n')



def prediction_example():
    read_samples("Intermediate_results/prediction.csv")
    # file_handle = open("Intermediate_results/2.txt", mode='w', encoding='utf-8')
    # for item in tqdm(res):
    #     file_handle.write(item.__repr__())
    #     file_handle.write('\n')


if __name__ == '__main__':
    prediction_example()