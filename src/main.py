import os
from datetime import date

GENERATION_DIR = "generations/"

#Next takes one and only part of iterator we care about
#[1] is the dir names
# print(len(next(os.walk(GENERATION_DIR))[1]))

length = 0
for _, dirnames, _ in os.walk(GENERATION_DIR):
    length = len(dirnames)

    #Only care about first
    break

# print(length)

name = GENERATION_DIR + str(date.today()) + " G" + str(length)
os.mkdir(name)
