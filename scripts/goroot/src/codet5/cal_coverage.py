import json
import subprocess
import shlex
import os
import shutil
from tqdm import tqdm
import re
import operator


class CalCoverage:
    # 将每一条数据写入test.go
    def create_test_go(self, input_string):
        # 解析字符串为字典
        try:
            data = json.loads(input_string)
        except (json.JSONDecodeError, TypeError):
            data=input_string

       # data = json.loads(input_string)

        # 提取代码1和代码2
        code1 = data['input'].strip()
        code2 = data['output'].strip()

        # 拼接代码1和代码2
        result = code1 + code2

        # 将结果写入文件
        with open('test.go', 'w') as f:
            f.write(result)

        # 定义要替换的包名
        new_package_name = 'main'

        # 读取 test.go 文件内容
        with open('test.go', 'r') as file:
            content = file.read()

        # 使用正则表达式匹配并替换包名
        pattern = r'package\s+\w+'
        content = re.sub(pattern, f'package {new_package_name}', content)

        # 将替换后的内容写入 test.go 文件
        with open('test.go', 'w') as file:
            file.write(content)

    # 删除所有文件以便下一个数据开始处理
    def clear(self):
        # 检查并删除 test.go 文件
        if os.path.isfile('test.go'):
            os.remove('test.go')
            # print("已删除 test.go 文件")

        # 检查并删除 pkgs.txt 文件
        if os.path.isfile('pkgs.txt'):
            os.remove('pkgs.txt')
            # print("已删除 pkgs.txt 文件。")

        # 检查并删除 myprogram.exe 文件
        if os.path.isfile('myprogram.exe'):
            os.remove('myprogram.exe')
            # print("已删除 myprogram.exe 文件。")

        # 检查并删除result.txt 文件
        if os.path.isfile('result.txt'):
            os.remove('result.txt')
             #print("已删除 result.txt 文件。")

        # 检查并删除 somedata 目录
        if os.path.isdir('somedata'):
            shutil.rmtree('somedata')
           # print("已删除 somedata 目录。")

        if os.path.isfile('hello.go'):
            os.remove('hello.go')

    def cal_result(self):
        # 读取 result.txt 文件
        with open('result.txt', 'r') as file:
            lines = file.readlines()

        # 计算百分比总和
        percentage_sum = 0.0
        for line in lines:
            match = re.search(r'coverage:\s*([\d.]+)%', line)
            if match:
                percentage = float(match.group(1))
                percentage_sum += percentage

        return percentage_sum

    # 计算覆盖率
    def cal_coverage(self,line):
        # 清理旧文件
        self.clear()

        # 创建 hello.go 文件并写入指定代码
        hello_code = "package main\n\nfunc main(){}"
        with open('hello.go', 'w') as file:
            file.write(hello_code)

        # 创建test.go文件
        self.create_test_go(line)
        if not os.path.isfile('test.go'):
            #print("test.go 文件不存在。")
            return 0

        # 执行 go list 命令并将结果写入 pkgs.txt 文件
        command = "exec 2>/dev/null &&  go list -f '{{.ImportPath}}' -deps . | paste -sd ',' > pkgs.txt"
        subprocess.run(command, shell=True)

        # 检查 pkgs.txt 文件是否存在
        if not os.path.isfile('pkgs.txt'):
            #print(" pkgs.txt文件不存在。")
            return 0

        # 检查 hello.go 文件是否存在
        if not os.path.isfile('hello.go'):
            #print("hello.go 文件不存在。")
            return 0

        # 执行 go build 命令并指定 -coverpkg 参数
        coverpkg = "`cat pkgs.txt`"
        build_command = f"exec 2>/dev/null &&  go build -o myprogram.exe -coverpkg={coverpkg} ."
        subprocess.run(build_command, shell=True)

        # 检查 myprogram.exe 文件是否存在
        if not os.path.isfile('myprogram.exe'):
            #print("myprogram.exe 文件不存在。")
            return 0

        # 创建 somedata 目录
        os.mkdir('somedata')

        # 执行 myprogram.exe 命令
        subprocess.run('exec 2>/dev/null && GOCOVERDIR=somedata ./myprogram.exe', shell=True)

        # 执行 go tool covdata 命令并将结果写入 result.txt 文件
        subprocess.run('exec 2>/dev/null && go tool covdata percent -i=somedata > result.txt', shell=True)
       
        # 合并到merged目录里
        subprocess.run('go tool covdata merge -i=somedata -o merged', shell=True)

        # 检查 result.txt 文件是否存在
        if not os.path.isfile('result.txt'):
            #print("result.txt 文件不存在。")
            return 0
            # 执行 cal.py 脚本
            # subprocess.run('python cal.py', shell=True)
        percentage_sum = self.cal_result()
  
        #print(percentage_sum)
        #print("ok")
        # 清理旧文件
        self.clear()

        return percentage_sum


