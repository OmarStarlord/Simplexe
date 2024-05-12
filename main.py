def input_simplex_problem():
    num_variables = int(input("Entrez nombre de variables: "))
    num_constraints = int(input("Entrer nombre de contraintes: "))

    
    table = [[0] * (num_variables + num_constraints + 2) for _ in range(num_constraints + 1)]

    
    for i in range(num_constraints + 1):
        if i == 0:
            table[i][0] = 1  # ajout 1 dans la premiere ligne
        else:
            table[i][0] = 0  #  ajout 0 dans les autres lignes

    # entrez variables de fonctions de maximisation
    print("Entrez les coef de la fonction a maximiser:")
    for i in range(num_variables):
        coefficient = int(input(f"Enter coefficient for variable {i+1}: "))
        table[0][i+1] = -coefficient  # Shift by 1 because of the added column

    print("Entrez les coef des contraintes:")
    for i in range(1, num_constraints + 1):
        print(f"For constraint {i}:")
        for j in range(num_variables):
            coefficient = int(input(f"Enter coefficient for variable {j+1}: "))
            table[i][j+1] = coefficient  

        table[i][num_variables + i] = 1  
        rhs = int(input("Enter the right-hand side of the constraint: "))
        table[i][-1] = rhs

    print("\nTable:")
    for row in table:
        print(row)

    return table

#Trouver la colonne pivot c-a-d la colonne qui contient le plus grand nombre negatif
def trouver_colonne_pivot(table):
    premier_ligne = table[0][:-1]
    
    min_value = min(premier_ligne)
    pivot_col = premier_ligne.index(min_value)
    
    print(f"La colonne pivot est: {pivot_col + 1}")
    print(f"La colonne du pivot est: {[row[pivot_col] for row in table]}")
    
    return pivot_col

#Trouver la colonne pivot c-a-d la colonne qui contient le petit ration positif 
def trouver_ligne_pivot(table, pivot_col):
    ratios = []
    for i in range(1, len(table)):
        if table[i][pivot_col] <= 0:
            continue
        else:
            ratio = table[i][-1] / table[i][pivot_col]
            ratios.append((ratio, i))
    
    if not ratios:
        
        return None
    
   
    pivot_row = min(ratios)[1]  
    print(f"La ligne pivot est: {pivot_row+1}")
    print(f"La ligne du pivot est: {table[pivot_row+1]}") 
    return pivot_row


#changer la ligne pivot en ligne pivot / pivot
def update_pivot_row(table, pivot_row, pivot_col):
    pivot_element = table[pivot_row][pivot_col]
    updated_pivot_row = [element / pivot_element for element in table[pivot_row]]
    table[pivot_row] = updated_pivot_row
    print("Table after updating pivot row:")
    print(f"La ligne du pivot est: {table[pivot_row]}")  
    return table


# changer les autres lignes en ligne - (multiplier * pivot_row)
def update_other_rows(table, pivot_row, pivot_col):
    num_rows = len(table)
    num_cols = len(table[0])

    for i in range(num_rows):
        if i == pivot_row:
            continue  
        else:
            multiplier = table[i][pivot_col]
            for j in range(num_cols):
                table[i][j] -= multiplier * table[pivot_row][j]
    
    print("Table after updating other rows:")
    for row in table:
        print(row)
    return table



t = input_simplex_problem()
print("Table:")
for row in t:
    print(row)


while True:
    cp = trouver_colonne_pivot(t)
    lp = trouver_ligne_pivot(t, cp)

    if lp is not None:
        t = update_pivot_row(t, lp, cp)
        t = update_other_rows(t, lp, cp)
    else:
        print("Aucune ligne pivot trouvée. Le tableau est optimal.")
        break

    
    if any(value < 0 for value in t[0][1:-1]):
        print("Il reste des valeurs négatives dans la 1ère ligne. Réitération du simplex.")
    else:
        print("Plus de valeurs négatives dans la 1ère ligne. Le tableau est optimal.")
        break

print("\nFinal Table after simplex iterations:")
for row in t:
    print(row)
    
    

print("\nSolutions:")
for i in range(1, len(t)):
    print(f"X{i} = {t[i][-1]}")