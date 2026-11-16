import time
import random


with open("widgets/textarea.py", "r") as f:
    text = "".join(f.readlines())

pos = random.randint(10, len(text)-10)

for i in range(1000):
    start = time.time()
    text2 = text[:pos] + "sss" + text[pos:]
    end = time.time()
    print("time:", end - start, "fps:", round((end - start) / 1000))