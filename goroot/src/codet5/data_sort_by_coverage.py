import cal_coverage
import os
import shutil
from tqdm import tqdm
import re
import operator

class GoSortByCoverage:
    def __init__(self,srcPath,dstPath):
        self.data_map = {}
        self.src=srcPath
        self.dst=dstPath
        self.sorted_map = {}

        # 初始覆盖率情况和最终覆盖率情况

        self.origin_average = 0
        self.origin_max_value = 0
        self.final_average = 0
        self.final_max_value = 0

    # 对初始数据进行初始化，即初始化sorted_map
    def CovergaeInit(self):
        # 读取origin_data.json文件
        with open(self.src, "r") as file:
            data = file.readlines()

        # 遍历每一条数据，并作为参数调用脚本
        for line in tqdm(data):
            line = line.strip()  # 去除行首行尾的空白字符
            self.data_map[line]=cal_coverage.CalCoverage().cal_coverage(line)
        

        # 按值对字典进行排序
        self.sorted_map = dict(sorted(self.data_map.items(), key=operator.itemgetter(1), reverse=True))

        # 检查目标路径是否存在，如果存在则删除重建
        if os.path.exists(self.dst):
            os.remove(self.dst)
        

        # 将Map中的string逐个写入目标文件，每两个字符串之间用换行符分隔
        with open(self.dst, 'w') as file:
            strings = list(self.sorted_map.keys())
            for i, string in enumerate(strings):
                file.write(string)
                if i < len(strings) - 1:
                    file.write('\n')

    def Sort(self):
        print("\nBegin calculate coverage of origin data:\n")
        self.CovergaeInit()
        # 计算平均值
        values = self.sorted_map.values()
        total = sum(values)
        average = total / len(values)
        self.origin_average_value = total / len(values)
        # 获取最高值
        self.origin_max_value =  max(values)

        print(f"\nFinish calculate coverage of origin data.\nThe origin max coverage: {self.origin_max_value}\nThe origin average coverage: {self.origin_average_value}\n\n")
        
        # 初始化计数器和总和
        count = 0
        total = 0

        # 遍历已排序的字典条目
        for key, value in self.sorted_map.items():
            if value != 0:
            # 计算条目总数和总和
                count += 1
                total += value

        # 计算均值
        if count > 0:
            average = total / count
        else:
            average = 0

        # 打印结果
        print("条目个数:", count)
        print("总和:", total)
        print("均值:", average)


        return self.sorted_map

