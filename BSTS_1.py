import numpy as np
import pandas as pd

# dane
s = np.array([14.1, 9.3, 14.5, 11.8, 12.0,
              11.1, 7.4, 11.0, 13.9, 11.1,
              11.7, 12.4, 9.4, 5.2, 10.0])

# średnia (mean)
srednia = np.mean(s)

# mediana (median)
mediana = np.median(s)

# dominanta (mode) – z użyciem pandas
serie = pd.Series(s)
dominanta = serie.mode()   # może zwrócić więcej niż jedną wartość

print("Średnia:", srednia)
print("Mediana:", mediana)
print("Dominanta(y):")
print(dominanta.values)