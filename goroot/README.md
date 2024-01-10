# Go Compiler Testing

Go is an open source programming language that makes it easy to build simple,
reliable, and efficient software.

![Gopher image](https://golang.org/doc/gopher/fiveyears.jpg)
*Gopher image by [Renee French][rf], licensed under [Creative Commons 4.0 Attributions license][cc4-by].*


### Introduction

A seed scheduling algorithm for testing Go language compilers based on coverage

### File Structure

- Go compiler source code
	- src
		- goroot
			- codet5
				- run.py # 种子调度脚本
				- origin_data.json # 初始测试样例
				- data.json # 排序后的种子样例
### Update
- 6.3 完成每一条数据的计算覆盖率部分
- 6.4 完成调度算法
