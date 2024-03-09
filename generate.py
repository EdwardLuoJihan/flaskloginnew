import random
import names
import json

COLORS = [
    ['#DF7FD7', '#f2a9ec', '#591854'],
    ['#E3CAC8', '#DF8A82', '#5E3A37'],
    ['#E6845E', '#E05118', '#61230B'],
    ['#E0B050', '#E6CB97', '#614C23'],
    ['#9878AD', '#492661', '#C59BE0'],
    ['#787BAD', '#141961', '#9B9FE0'],
    ['#78A2AD', '#104F61', '#9BD1E0'],
    ['#78AD8A', '#0A6129', '#9BE0B3'],
    ['#AD8621', '#6B5621', '#E0AD2B'],
    ['#2effbd', '#00e69d', '#12946b'],
]

subject_colors = {
    "Math": "#99caff",
    "Social": "#ffc099",
    "Science": "#bbff99",
    "Language Arts": "#ff9999",
    "Other": "#e699ff",
}

subjects = ["Math", "Social", "Science", "Language Arts", "Other"]

for i in range(int(input())):
  f = open('generate.json')
  users = json.load(f)
  username = names.get_full_name()
  name = username
  p = username
  c = random.choice(COLORS)
  t = random.choice(["Tutor", "Student"])
  tags = [[i, subject_colors[i]] for i in list(set(random.choices(subjects, k=random.choice([0,1,2,3,4,5]))))]
  grade = random.randint(1, 30)
  users[username] = {'name': name, 'p': p, 'c':  c, 't': t, "tags": tags, "grade": grade}
  with open('generate.json', 'w') as f:
      json.dump(users, f)