#!/bin/bash

# 使go命令生效
source ~/.profile

# merged目录存放合并的覆盖率文件，profile.txt存放textfmt格式的merged文件
if [ -d "merged" ]; then
    rm -rf merged
fi
if [ -f "profile.txt" ]; then
    rm profile.txt
fi
mkdir merged

# 跑数据的覆盖率，结果存在merged目录中。数据循环生成，共1000轮
python run.py

# 解析合并的merged目录到profile.txt中
go tool covdata textfmt -i=merged -o profile.txt

# 计算总的覆盖率
python cal_cov_frac_result.py

