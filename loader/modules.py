import os
import json

def load_theory_modules(path_template="theory_module_{}.txt", count=8):
    modules = {}
    for i in range(1, count + 1):
        path = path_template.format(i)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                modules[i] = [b.strip() for b in f.read().split("\n\n") if b.strip()]
    return modules

def load_practice_modules(path_template="module_{}_quest.json", count=8):
    modules = {}
    for i in range(1, count + 1):
        path = path_template.format(i)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                modules[i] = json.load(f)
    return modules

def load_tutorial(path="tutorial.txt"):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    return ""
