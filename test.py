
n = 5

grille = []
for i in range(n):
    l = []
    for j in range(n):
        if i == 2 and j == 2:
            l.append(None)
        else:
            l.append(1)
    grille.append(l)
print(grille)