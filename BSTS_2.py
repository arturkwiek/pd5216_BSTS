import numpy as np
import pandas as pd

# parametry rozkładu i liczba obserwacji
mu = 10
sigma = 2
N = 30

# generowanie danych z rozkładu normalnego N(mu, sigma)
# (losowanie za każdym uruchomieniem programu)
s = np.random.normal(loc=mu, scale=sigma, size=N)

# średnia i mediana (jak w BSTS_1)
srednia = np.mean(s)
mediana = np.median(s)

# dominanta z użyciem pandas
serie = pd.Series(s)
dominanta = serie.mode()

# miary rozproszenia (z próby)
odchylenie_std = np.std(s, ddof=1)  # odchylenie standardowe z próby
wariancja = np.var(s, ddof=1)      # wariancja z próby
rozstep = np.max(s) - np.min(s)    # rozstęp

print("Wygenerowane dane:")
print(s)

print("\nŚrednia:", srednia)
print("Mediana:", mediana)
print("Dominanta(y):", dominanta.values)

print("\nMiary rozproszenia (z próby):")
print("Odchylenie standardowe:", odchylenie_std)
print("Wariancja:", wariancja)
print("Rozstęp:", rozstep)
