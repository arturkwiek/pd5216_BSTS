import numpy as np
from scipy import stats

# Analiza: wpływ nowego leku na poziom ekspresji genu X.
# Grupy niezależne → test t-Studenta dla prób niezależnych
# Sprawdzamy normalność (Shapiro-Wilk) i równość wariancji (Levene)

alpha = 0.05

control = np.array([14.8, 10.9, 13.5, 13.2, 10.7, 13.3, 13.8, 13.8, 12.0, 12.6])
experimental = np.array([14.6, 14.7, 13.6, 13.0, 14.7, 13.9, 13.6, 14.8, 12.9, 14.8])

print("Dane wejściowe:")
print("Grupa kontrolna:", control)
print("Grupa eksperymentalna:", experimental)
print()

# Testy normalności (Shapiro-Wilk)
shapiro_control = stats.shapiro(control)
shapiro_experimental = stats.shapiro(experimental)

print("Test normalności Shapiro-Wilka:")
print(f"Kontrolna: stat={shapiro_control.statistic:.4f}, p={shapiro_control.pvalue:.4f}")
print(f"Eksperymentalna: stat={shapiro_experimental.statistic:.4f}, p={shapiro_experimental.pvalue:.4f}")
if shapiro_control.pvalue > alpha and shapiro_experimental.pvalue > alpha:
    print(f"W obu grupach brak podstaw do odrzucenia normalności (p > {alpha}).")
else:
    print(f"W co najmniej jednej grupie możliwe odchylenia od normalności (p <= {alpha}).")
print()

# Test równości wariancji (Levene)
levene_res = stats.levene(control, experimental)
print("Test równości wariancji (Levene):")
print(f"stat={levene_res.statistic:.4f}, p={levene_res.pvalue:.4f}")
if levene_res.pvalue > alpha:
    print(f"Brak podstaw do odrzucenia hipotezy o równości wariancji (p > {alpha}).")
    equal_var = True
else:
    print(f"Można podejrzewać różne wariancje (p <= {alpha}), zastosujemy test Welcha.")
    equal_var = False
print()

# Test t-Studenta dla prób niezależnych
# H0: średni poziom ekspresji jest taki sam w obu grupach
# H1: średni poziom ekspresji różni się między grupami

res_t = stats.ttest_ind(control, experimental, equal_var=equal_var)

mean_control = control.mean()
mean_experimental = experimental.mean()

print("Test t-Studenta dla prób niezależnych:")
print(f"Średnia kontrolna = {mean_control:.3f}")
print(f"Średnia eksperymentalna = {mean_experimental:.3f}")
print(f"t = {res_t.statistic:.4f}, p = {res_t.pvalue:.4f}")

if res_t.pvalue < alpha:
    print(f"Ponieważ p < {alpha}, odrzucamy H0.")
    print("Wynik: różnice średnich poziomów ekspresji są statystycznie istotne.")
else:
    print(f"Ponieważ p >= {alpha}, brak podstaw do odrzucenia H0.")
    print("Wynik: brak statystycznie istotnych różnic średnich poziomów ekspresji między grupami.")

print("\nUwaga do założeń:")
print("- Jeśli rozkład byłby wyraźnie nienormalny lub liczebności bardzo małe, można rozważyć test nieparametryczny (np. test Manna-Whitneya).")
