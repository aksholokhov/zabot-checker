import sys
from operator import itemgetter
import numpy as np
from pyparsing import *

file = sys.argv[1]
m = int(sys.argv[2])
n = int(sys.argv[3])

rus_alphas = 'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'

question = Word(rus_alphas + alphas,  alphas + rus_alphas + " .,+-:" + nums)('question')
stars = (OneOrMore("*"))('stars')
mark = (Word("LEARNED ") | Word("LEARN "))('mark')
progress = Word("[", "/"+ nums + "]")
line = stars + Optional(mark) + question + Optional(progress)

with open(file, "r") as o:
    f = o.readlines()
    
questions = {}
marks = [x.strip() for x in f[0].strip().split(":")[1].split("|")]
active_section = "root"
active_num = 1;

for x in f[1:]:
    res = line.parseString(x)
    if len(res.stars) == 1:
        active_section = ("[%03d]")%(active_num) + res.question.strip()
        active_num += 1;
    else:
        if questions.get(active_section, 0) == 0:
            questions[active_section] = []
        mark = res.mark
        if len(mark) == 0: 
            mark = "LEARN "
        #if mark != "LEARNED": 
        questions[active_section].append({"question": res.question.strip(), "mark":mark})

while(True):
    themes = np.random.permutation(list(questions.keys()))[:m]
    asked = []
    for theme in themes:
        list_to_ask = [x for x in questions[theme] if x["mark"].strip() != "LEARNED" ]
        qs = np.random.permutation(list(range(len(list_to_ask))))[:n];
        for q in qs:
            asked.append({"t": theme, "q": list_to_ask[q]})
    
    if len(asked) == 0:
        print("finished!\n")
        break

    curr_theme = ""
    for q in asked:
        if curr_theme != q["t"]:
            curr_theme = q["t"];
            print(curr_theme + ":")
        print("  * " + q["q"]["question"]) 
        
    marks = input()
    if (marks == "end"):
        print("finished!\n")
        break;
    while (len(marks) != len(asked)):
        print("Number of marks don't match with number of questions")
        marks = input()
        
    for mark, q in zip(marks, asked):
        q["q"]["mark"] = "LEARNED " if mark == "+" else "LEARN "     

with open(file, "w") as o:
    o.write(f[0])
    for theme, qs in questions.items():
        c = 0
        for q in qs:
            c += 1 if q["mark"].strip() == "LEARNED" else 0
        o.write("* " + theme.split("]")[1].strip() + " [" + str(c) +"/" + str(len(qs)) + "]\n")
        for q in qs:
            o.write("** " + q["mark"].strip() + " " + q["question"].strip() + "\n")
