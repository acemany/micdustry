from datetime import datetime
a=int(input())
with open("out.txt","a")as file:
    while True:
        b=f"{datetime.now()}\n{a} {input()}\n"
        file.write(b)
        print(b)
        a+=1