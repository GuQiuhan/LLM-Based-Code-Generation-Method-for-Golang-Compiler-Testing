import sys

import os

import data_sort_by_coverage

# 添加一个按照覆盖率排序函数
SRC_PATH=f"./data/gofuzz_rst.json"
SRC_SORTED_PATH = f"./data/gofuzz_rst_sort.json"

data_sort_by_coverage.GoSortByCoverage(SRC_PATH,SRC_SORTED_PATH).Sort()
