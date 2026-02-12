import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
BSTS_7 – wizualizacja poziomu glukozy przed i po terapii

Zadanie:
- Wczytanie danych dla dwóch grup (przed i po terapii),
- Wykres pudełkowy (boxplot),
- Histogram (porównanie rozkładów),
- Wykres słupkowy z paskami błędów (średnia ± przedział ufności / odchylenie),
- Krótki komentarz, która wizualizacja najlepiej pokazuje różnice między grupami.
"""

# Dane (mg/dL)
przed = np.array([98, 110, 104, 100, 108, 112, 105, 107, 102, 110,
                  115, 109, 106, 103, 101])
po = np.array([88, 90, 92, 91, 87, 93, 89, 90, 92, 91,
               86, 88, 89, 90, 87])

# Przygotowanie ramki danych do seaborn
wartosci = np.concatenate([przed, po])

grupy = (['Przed terapią'] * len(przed)) + (['Po terapii'] * len(po))

df = pd.DataFrame({
    'Poziom glukozy [mg/dL]': wartosci,
    'Grupa': grupy
})

# Podstawowe statystyki opisowe
print("Statystyki opisowe:\n")
print(df.groupby('Grupa')['Poziom glukozy [mg/dL]'].describe(), "\n")

sns.set(style="whitegrid", palette="Set2")

# 1. Wykres pudełkowy (boxplot)
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x='Grupa', y='Poziom glukozy [mg/dL]')
plt.title('Poziom glukozy – wykres pudełkowy')
plt.tight_layout()

# 2. Histogram (porównanie rozkładów)
plt.figure(figsize=(6, 4))
# Dwa histogramy na jednym wykresie z przezroczystością
plt.hist(przed, bins=8, alpha=0.6, label='Przed terapią', color='tab:blue', edgecolor='black')
plt.hist(po, bins=8, alpha=0.6, label='Po terapii', color='tab:orange', edgecolor='black')
plt.xlabel('Poziom glukozy [mg/dL]')
plt.ylabel('Liczba pacjentów')
plt.title('Poziom glukozy – histogramy dla obu grup')
plt.legend()
plt.tight_layout()

# 3. Wykres słupkowy z paskami błędów (barplot)
plt.figure(figsize=(6, 4))
# seaborn.barplot domyślnie rysuje średnią i przedziały ufności
sns.barplot(data=df, x='Grupa', y='Poziom glukozy [mg/dL]', ci='sd', capsize=0.15)
plt.title('Poziom glukozy – średnia ± SD')
plt.tight_layout()

plt.show()

# Komentarz porównawczy (wypisany w konsoli)
print("Interpretacja wizualizacji:\n")
print("1. Wykres pudełkowy bardzo dobrze pokazuje różnice w medianie, rozrzut danych")
print("   oraz ewentualne wartości odstające – jest czytelny przy porównaniu dwóch grup.")
print("2. Histogramy pokazują kształt rozkładu w każdej grupie, ale przy małej liczbie")
print("   pacjentów mogą być mniej stabilne (wynik zależy np. od liczby przedziałów).")
print("3. Wykres słupkowy z paskami błędów dobrze podkreśla różnicę w średnich oraz")
print("   pozwala oszacować zmienność (np. SD). Jest bardzo intuicyjny dla szybkiego")
print("   porównania poziomów glukozy między grupami.")
print("\nW tym przykładzie zarówno boxplot, jak i wykres słupkowy z paskami błędów")
print("najlepiej i najbardziej czytelnie ukazują różnice między grupą 'Przed terapią'")
print("a grupą 'Po terapii'. Histogram jest pomocny do oceny pełnego rozkładu, ale")
print("mniej przejrzysty przy tak małej próbie.")
