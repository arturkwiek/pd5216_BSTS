import numpy as np
from scipy import stats

"""
BSTS_5 – projekt eksperymentu + przykładowe dane

Pytanie: Czy nowy lek przeciwzapalny zmniejsza ekspresję genu IL6?

Hipoteza zerowa (H0): Średnia ekspresja IL6 jest taka sama w obu grupach.
Hipoteza alternatywna (H1): Średnia ekspresja IL6 różni się między grupami.

Plan: Dwie grupy – kontrolna (rozpuszczalnik) i eksperymentalna (lek).
Pomiar: Względna ekspresja IL6 metodą RT-qPCR po stymulacji cytokiną IL-1β.

Metoda analizy: Test t-Studenta dla prób niezależnych (dane ciągłe, dwie grupy).
"""


alpha = 0.05
np.random.seed(42)  # dla powtarzalności

n_control = 10
n_treated = 10

# Generowanie danych (rozkład normalny)
control = np.random.normal(loc=1.0, scale=0.15, size=n_control)
treated = np.random.normal(loc=0.6, scale=0.15, size=n_treated)

print("Przykładowe dane (względna ekspresja IL6):")
print("Grupa kontrolna:", np.round(control, 3))
print("Grupa z lekiem:", np.round(treated, 3))
print()

mean_control = control.mean()
mean_treated = treated.mean()
std_control = control.std(ddof=1)
std_treated = treated.std(ddof=1)

print("Statystyki opisowe:")
print(f"Kontrola: n={n_control}, średnia={mean_control:.3f}, SD={std_control:.3f}")
print(f"Lek:      n={n_treated}, średnia={mean_treated:.3f}, SD={std_treated:.3f}")
print()

# Test t-Studenta dla prób niezależnych (Welch)
res_t = stats.ttest_ind(control, treated, equal_var=False)

print("Test t-Studenta (Welch) dla prób niezależnych:")
print(f"t = {res_t.statistic:.4f}, p = {res_t.pvalue:.4e}")

if res_t.pvalue < alpha:
    print(f"Ponieważ p < {alpha}, odrzucamy hipotezę zerową (H0).")
    print("Wniosek: przykładowe dane sugerują istotne obniżenie ekspresji IL6 przez lek.")
else:
    print(f"Ponieważ p >= {alpha}, brak podstaw do odrzucenia H0.")
    print("Wniosek: na podstawie tych danych nie możemy stwierdzić istotnego wpływu leku.")

print("\n7. PRZEWIDYWANE WYNIKI I INTERPRETACJA")
print("W zaprojektowanym eksperymencie spodziewamy się, że:")
print("- Średnia ekspresja IL6 w grupie z lekiem będzie istotnie niższa niż w kontroli,")
print("- Test t-Studenta da istotny wynik (p < 0.05), co pozwoli odrzucić H0,")
print("- Otrzymamy tym samym statystyczne wsparcie dla hipotezy, że nowy lek")
print("  obniża ekspresję genu prozapalnego IL6 po stymulacji.")
