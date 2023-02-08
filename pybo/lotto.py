"""
파일명 : lotto.py
설 명 : 
생성일 : 2023-02-07
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""

import random


def main():
    for i in range(5):
        balls = [i for i in range(1, 46)]
        picked = []

        while len(picked) < 6:
            pick = random.randint(1, 45)
            if pick in balls:
                picked.append(pick)
                balls.remove(pick)
        print(picked)


main()
