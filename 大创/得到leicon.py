import phkit
import re

# 打开要读取的文件
with open('f:\My_Work\words.txt', 'r', encoding='utf-8') as input_file:
    # 打开要写入的文件
    with open('../lexicon.txt', 'w', encoding='utf-8') as output_file:
        # 逐行读取输入文件
        for line in input_file:
            result = phkit.text2phoneme(line)
            result_cleaned = [re.sub(r'[^a-zA-Z0-9]', '', item) for item in result]
            result_cleaned = [item for item in result_cleaned if item != '']
            result_concatenated = []
            print(result_cleaned)
            for i, item in enumerate(result_cleaned):
                # 如果当前项是数字且不是第一项，则将其与前一项连接起来
                if item.isnumeric() and i > 0:
                    result_concatenated[-1] += item
                else:
                    result_concatenated.append(item)
            result_str = ' '.join(result_concatenated)
            output_file.write(line.strip() + ' ' + result_str + '\n')


