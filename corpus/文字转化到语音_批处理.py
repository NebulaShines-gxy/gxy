# -*- coding: utf-8 -*-
import os
from pypinyin import pinyin

filepath = r'F:\My_Work\大创\corpus.txt'

with open(filepath, 'r', encoding='utf-8') as inputfile, open(r'C:\Users\Nebula shines\Desktop\trans(1).txt', 'w', encoding='utf-8') as output_file:
    for line in inputfile:
        # 使用pinyin函数将每一行的汉字转换为拼音
        if line.strip():
            pinyin_lines = pinyin(line, heteronym=False)

            # 将拼音列表转换为字符串
            pinyin_line = ' '.join([' '.join(word) for word in pinyin_lines])
            output_file.write(pinyin_line )
            output_file.write(line)   # 写入新文件并添加换行符



