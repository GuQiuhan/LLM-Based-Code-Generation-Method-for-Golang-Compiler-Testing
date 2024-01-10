import itertools
import random

from tqdm import tqdm

from data_io.file_io import data_from_jsonl, data_to_jsonl_append
from filter.internal_import_filter import InternalImportFilter
from filter.undefined_behavior_filter import UndefinedBehaviorFilter
from go_tree_sitter.go_parser import GoParser
from go_tree_sitter.go_tree_sitter_tool import GoTreeSitterTool
import cal_coverage

class TestCaseMaker:
    def __init__(self, src_path, dst_path, go_generator, tokenizer, test_case_cache_size=500):
        self.src_path = src_path
        self.dst_path = dst_path

        self.MAX_INPUT_TOKEN_LEN = 512

        self.parser = GoParser()

        self.go_generator = go_generator

        self.tokenizer = tokenizer

        self.origin_data_list = []
        for src_line in data_from_jsonl(self.src_path):
            self.origin_data_list.append(src_line)

        self.test_case_cache_list = []
        self.test_case_cache_size = test_case_cache_size

    def add_data_to_test_case_cache(self, data):
        if len(self.test_case_cache_list) == self.test_case_cache_size:
            self.test_case_cache_list[0] = data
        else:
            self.test_case_cache_list.append(data)

         # 按照覆盖率大小排序
        self.test_case_cache_list.sort(key=lambda x: cal_coverage.CalCoverage().cal_coverage(x), reverse=True)

    def get_top_data_from_test_case_cache(self):
        if len(self.test_case_cache_list) == 0:
            return None
        else:
            data=self.test_case_cache_list.pop(0)

            return data

    def get_top_data_from_origin_data(self):
        if len(self.origin_data_list) == 0:
            return None
        else:
            data=self.origin_data_list.pop(0)
        

            return data

    def build_new_data(self, old_data):
        # get old_data_code and old_data_function_signature and old_data_function_code <- (can be "")
        old_data_line_list = old_data["input"].splitlines()
        old_data_code = ""
        for line in old_data_line_list[:-1]:
            old_data_code += line + "\n"
        old_data_function_signature = old_data_line_list[-1]

        old_data_node = self.parser.parse(old_data_code)
        old_data_function_nodes = GoTreeSitterTool.get_function_declaration(old_data_node)
        if len(old_data_function_nodes) == 0:
            old_data_function_code = ""
        else:
            old_data_function_code = random.choice(old_data_function_nodes).text.decode("utf8")

        # get tool_data_function_code <- (can't be "")
        tool_data_function_code = ""
        while tool_data_function_code == "":
            tool_data = self.get_top_data_from_origin_data()
            if not tool_data:
                return None
            tool_data_code = tool_data["input"] + tool_data["output"]
            tool_data_node = self.parser.parse(tool_data_code)
            tool_data_function_nodes = GoTreeSitterTool.get_function_declaration(tool_data_node)
            if len(tool_data_function_nodes) == 0:
                tool_data_function_code = ""
            else:
                tool_data_function_code = random.choice(tool_data_function_nodes).text.decode("utf8")

        # build new_data in 3 different ways
        new_data_list = []

        # delete old_data_function_code
        if old_data_function_code != "":
            new_input = old_data["input"].replace(old_data_function_code, "")
            new_data = {"input": new_input, "output": old_data["output"]}

            new_data_list.append(new_data)

        # replace old_data_function_code with tool_data_function_code
        if old_data_function_code != "":
            new_input = old_data["input"].replace(old_data_function_code, tool_data_function_code)
            new_data = {"input": new_input, "output": old_data["output"]}

            new_data_list.append(new_data)

        # add tool_data_function_code
        new_input = old_data_function_code + "\n" + tool_data_function_code + "\n\n" + old_data_function_signature
        new_data = {"input": new_input, "output": old_data["output"]}

        new_data_list.append(new_data)

        return new_data_list

    def data_input_do_filter(self, data):
        flag = False
        count = {"has_error": 0, "undefined_behavior": 0}

        input_code = data["input"]
        token_len = len(self.tokenizer(input_code, return_tensors="pt").input_ids[0])

        if token_len > self.MAX_INPUT_TOKEN_LEN:
            flag = True
            return flag, count

        input_node = self.parser.parse(input_code)

        if GoTreeSitterTool.has_error(input_node):
            flag = True
            count["has_error"] += 1
        if UndefinedBehaviorFilter.do_filter(input_node):
            flag = True
            count["undefined_behavior"] += 1

        return flag, count

    def test_case_do_filter(self, test_case):
        flag = False
        count = {"has_error": 0, "undefined_behavior": 0}

        code = test_case["input"] + test_case["output"]
        node = self.parser.parse(code)

        if GoTreeSitterTool.has_error(node):
            flag = True
            count["has_error"] += 1
        if UndefinedBehaviorFilter.do_filter(node):
            flag = True
            count["undefined_behavior"] += 1

        return flag, count

    def generate_test_case(self, data):
        input_text = data["input"]
        output_text = self.go_generator.generate(input_text)
        test_case = {"input": input_text, "output": output_text}
        return test_case

    def make_test_case_loop(self, max_test_case_num=1):
        total_test_case_count = {"total_test_case": 0, "has_error": 0, "undefined_behavior": 0}
        test_case_num = 0
        new_data_list = []
        with tqdm(total=max_test_case_num) as pbar:
            while test_case_num < max_test_case_num:
                if len(new_data_list) != 0:
                    curr_data = new_data_list[0]
                    new_data_list = new_data_list[1:]
                elif len(self.test_case_cache_list) != 0:
                    curr_data = self.get_top_data_from_test_case_cache()
                else:
                    curr_data = self.get_top_data_from_origin_data()
                
                if not curr_data:
                    break

                input_flag, input_count = self.data_input_do_filter(curr_data)
                if not input_flag:
                    test_case = self.generate_test_case(curr_data)
                    total_test_case_count["total_test_case"] += 1

                    test_case_flag, test_case_count = self.test_case_do_filter(test_case)
                    if not test_case_flag:
                        test_case_num += 1
                        pbar.update(1)
                        data_to_jsonl_append(self.dst_path, test_case)

                        self.add_data_to_test_case_cache(test_case)
                        new_data_list += self.build_new_data(test_case)

                        # 按照覆盖率大小排序
                        new_data_list.sort(key=lambda x: cal_coverage.CalCoverage().cal_coverage(x), reverse=True)
                    else:
                        total_test_case_count["has_error"] += test_case_count["has_error"]
                        total_test_case_count["undefined_behavior"] += test_case_count["undefined_behavior"]

        return total_test_case_count
