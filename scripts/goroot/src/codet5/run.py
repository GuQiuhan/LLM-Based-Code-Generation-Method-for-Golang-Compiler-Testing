import sys

import os

import torch
from transformers import RobertaTokenizer

from go_generate.go_generator import GoGenerator
from go_generate.test_case_maker import TestCaseMaker
import data_sort_by_coverage

MODEL_PATH = "intm/codet5-small-go_generation"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CACHE_DIR = None

go_generator = GoGenerator(MODEL_PATH, DEVICE)

tokenizer = RobertaTokenizer.from_pretrained(MODEL_PATH, cache_dir=CACHE_DIR)

DATA_COUNT = 71421

# 添加一个按照覆盖率排序函数
SRC_PATH=f"./data/origin_data.json"
SRC_SORTED_PATH = f"./data/origin_sorted_data.json"

data_sort_by_coverage.GoSortByCoverage(SRC_PATH,SRC_SORTED_PATH).Sort()

DST_PATH = f"./data/output_data.json"

if os.path.isfile(DST_PATH):
    os.remove(DST_PATH)

test_case_maker = TestCaseMaker(SRC_SORTED_PATH, DST_PATH, go_generator, tokenizer)

total_test_case_count = test_case_maker.make_test_case_loop(1000)

print(f"{total_test_case_count}")
