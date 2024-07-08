total = 709107 # go编译器源码总的语句数
Sum=0 # 执行到的语句数

with open('profile.txt', 'r') as file:
    lines = file.readlines()[1:]  # 除去第一行
    for line in lines:
        values = line.split(' ')
        last_integer = int(values[-1])
        Sum += last_integer

print(Sum/total)

