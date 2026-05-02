import re
txt=input()
p=re.findall('^a.*b$',txt)
if p:
    print("Match")
else:
    print("Not Match")