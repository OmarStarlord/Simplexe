import tkinter as tk
from tkinter import messagebox

class SimplexInterface:
    def __init__(self, master):
        self.master = master
        master.title("Simplex Solver")

        self.label = tk.Label(master, text="Entrez les informations du problème:")
        self.label.grid(row=0, columnspan=2, padx=10, pady=10)

        self.variable_label = tk.Label(master, text="Nombre de variables:")
        self.variable_label.grid(row=1, column=0, padx=10, pady=10)
        self.variable_entry = tk.Entry(master)
        self.variable_entry.grid(row=1, column=1, padx=10, pady=10)

        self.constraint_label = tk.Label(master, text="Nombre de contraintes:")
        self.constraint_label.grid(row=2, column=0, padx=10, pady=10)
        self.constraint_entry = tk.Entry(master)
        self.constraint_entry.grid(row=2, column=1, padx=10, pady=10)

        self.solve_button = tk.Button(master, text="Résoudre", command=self.solve_simplex)
        self.solve_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def solve_simplex(self):
        try:
            num_vars = int(self.variable_entry.get())
            num_constraints = int(self.constraint_entry.get())
            input_window = tk.Toplevel(self.master)
            input_window.title("Entrez les coefficients et les contraintes")

            self.coefficient_entries = []
            self.constraint_entries = []
            self.rhs_entries = []

            for i in range(num_vars):
                label = tk.Label(input_window, text=f"Coefficient de X{i+1}:")
                label.grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(input_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.coefficient_entries.append(entry)

            for i in range(num_constraints):
                constraint_label = tk.Label(input_window, text=f"Contrainte {i+1}:")
                constraint_label.grid(row=i, column=2, padx=10, pady=5)
                constraint_entries = []
                for j in range(num_vars):
                    entry = tk.Entry(input_window)
                    entry.grid(row=i, column=j+3, padx=10, pady=5)
                    constraint_entries.append(entry)
                self.constraint_entries.append(constraint_entries)

                rhs_label = tk.Label(input_window, text="RHS:")
                rhs_label.grid(row=i, column=num_vars+3, padx=10, pady=5)
                rhs_entry = tk.Entry(input_window)
                rhs_entry.grid(row=i, column=num_vars+4, padx=10, pady=5)
                self.rhs_entries.append(rhs_entry)

            solve_button = tk.Button(input_window, text="Résoudre", command=lambda: self.solve_problem(input_window))
            solve_button.grid(row=num_constraints+1, columnspan=num_vars+5, padx=10, pady=10)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

    def solve_problem(self, input_window):
        try:
            num_vars = len(self.coefficient_entries)
            num_constraints = len(self.constraint_entries)
            
            table = []
            table.append([1] + [-float(entry.get()) for entry in self.coefficient_entries] + [0] * num_constraints + [0])

            for i in range(num_constraints):
                row = [0] * (num_vars + num_constraints + 2)
                row[num_vars + i + 1] = 1
                for j in range(num_vars):
                    row[j + 1] = float(self.constraint_entries[i][j].get())
                row[-1] = float(self.rhs_entries[i].get())
                table.append(row)

            result_window = tk.Toplevel(self.master)
            result_window.title("Résultats")

            result_label = tk.Label(result_window, text="Tableau final après les itérations Simplex:")
            result_label.pack(padx=10, pady=10)

            table_text = tk.Text(result_window, width=50, height=10)
            table_text.pack(padx=10, pady=10)

            for row in table:
                table_text.insert(tk.END, ' '.join(map(str, row)) + '\n')

            # Afficher les solutions
            solutions_label = tk.Label(result_window, text="Solutions:")
            solutions_label.pack(padx=10, pady=5)

            for i in range(1, len(table)):
                solution_label = tk.Label(result_window, text=f"X{i} = {table[i][-1]}")
                solution_label.pack(padx=10, pady=5)
            
            messagebox.showinfo("Résultat", "Problème résolu avec succès !")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
        finally:
            input_window.destroy()

root = tk.Tk()
app = SimplexInterface(root)
root.mainloop()
