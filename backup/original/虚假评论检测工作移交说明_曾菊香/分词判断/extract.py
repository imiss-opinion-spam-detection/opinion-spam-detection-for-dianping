n=0
with open('12452310859.txt', 'r') as f1, open('a.txt', 'w') as f2:
    for line in f1.readlines():
        line = line.strip()
        if "content " in line:
            n=n+1
            f2.write(str(n)+' '+line + '\n')
            f2.close()
