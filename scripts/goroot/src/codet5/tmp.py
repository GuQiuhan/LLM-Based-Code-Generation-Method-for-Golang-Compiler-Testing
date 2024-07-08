total = 0

with open('profile.txt', 'r') as file:
    lines = file.readlines()[1:]  # 除去第一行
    for line in lines:
        values = line.split(' ')
        last_integer = int(values[-1])
        total += last_integer

print(total)

