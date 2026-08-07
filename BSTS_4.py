## Tak, rozumiem Pani rozczarowanie. Z premedytacją używam modeli AI, bo to już niestety będą narzędzia przyszłości.
# Opieranie się temu, to tak jakby kilkanaście lat temu przyjmować postawę: 

# "Nie będę korzystał z edytorów podpowiadających składnię języka i strukturę projektu, danych i klas, bo to pójście na łatwiznę."

# Ale faktem jest, że nie zerknięcie na wyniki wypluwane przez te automaty to z mojej strony całkowite niechlujstwo.
# Mam nadzieję, że nie poczuła się Pani zlekceważona lub coś w tym rodzaju.
# Złożyłem w zeszłym roku podania na trzy podyplomówki, z obawy, że z braku chętnych nie otworzą tych kierunków i teraz z Githubem copilotem i ChatGPT ogarniamy te trzy kierunki. Właściwie tylko dwa, ale to zawsze dwa razy tyle co jeden :)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

"""
Analiza PCA mikrobiomu z trzech srodowisk (gleba, woda, jelita).
- Wiersze: próbki
- Kolumny 1..n-1: udziały gatunków
- Ostatnia kolumna: typ srodowiska

OPCJA A: wartości to już procenty
OPCJA B: wartości to liczby odczytów → konwersja na procenty

Kroki: standaryzacja → PCA (2 składowe) → wykres
"""

# Ścieżka do pliku CSV
CSV_PATH = "mikrobiom.csv"  # np. "mikrobiom.csv" lub inna nazwa

# Wybierz tryb: False -> OPCJA A (procenty), True -> OPCJA B (liczebności -> procenty)
OPTION_B_COUNTS = False


def load_and_prepare_data(csv_path: str, option_b_counts: bool = False):
    """Wczytuje dane z CSV i przygotowuje macierz cech oraz etykiety srodowisk.

    Zwraca:
    - X_scaled: standaryzowana macierz cech (próbki x gatunki),
    - env: wektor etykiet srodowisk,
    - pca: dopasowany obiekt PCA (2 składowe).
    """
    # Plik mikrobiom.csv jest zapisany z separatorami tabulacji, więc ustawiamy sep="\t".
    df = pd.read_csv(csv_path, sep="\t")

    # Zakładamy, że ostatnia kolumna to "srodowisko"
    if "srodowisko" not in df.columns:
        raise ValueError("Oczekiwano kolumny 'srodowisko' jako ostatniej kolumny w pliku CSV.")

    feature_cols = [c for c in df.columns if c != "srodowisko"]

    X_raw = df[feature_cols].values.astype(float)
    env = df["srodowisko"].values

    # OPCJA A vs OPCJA B
    if option_b_counts:
        # Traktujemy wartości jako liczby odczytów i przeliczamy na procenty.
        row_sums = X_raw.sum(axis=1, keepdims=True)
        # Zabezpieczenie przed dzieleniem przez zero
        row_sums[row_sums == 0] = 1.0
        X_pct = X_raw / row_sums * 100.0
    else:
        # Zakładamy, że wartości są już procentami (lub udziałami porównywalnymi między próbkami)
        X_pct = X_raw

    # Standaryzacja cech przed PCA
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_pct)

    # PCA do 2 składowych
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    return X_pca, env, pca


def plot_pca(X_pca: np.ndarray, env: np.ndarray, pca: PCA):
    """Rysuje wykres 2D PCA z próbkami pokolorowanymi wg srodowiska."""
    pc1 = X_pca[:, 0]
    pc2 = X_pca[:, 1]

    unique_envs = np.unique(env)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_envs)))

    plt.figure(figsize=(8, 6))

    for e, col in zip(unique_envs, colors):
        mask = env == e
        plt.scatter(pc1[mask], pc2[mask], color=col, label=e, alpha=0.8, edgecolors="k")

    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0] * 100:.1f}% wariancji)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1] * 100:.1f}% wariancji)")
    plt.title("PCA mikrobiomu (2 główne składowe)")
    plt.legend(title="srodowisko")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Wczytanie danych i PCA
    try:
        X_pca, env, pca = load_and_prepare_data(CSV_PATH, OPTION_B_COUNTS)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {CSV_PATH}. Upewnij się, że ścieżka jest poprawna.")
    except ValueError as e:
        print("Błąd w danych:", e)
    else:
        print("Udział wariancji wyjaśnionej przez PC1 i PC2:")
        print(f"PC1: {pca.explained_variance_ratio_[0] * 100:.2f}%")
        print(f"PC2: {pca.explained_variance_ratio_[1] * 100:.2f}%")
        print("Suma (PC1 + PC2):", f"{pca.explained_variance_ratio_[:2].sum() * 100:.2f}%")

        print("\nInterpretacja (ogólne wskazówki):")
        print("- Na wykresie sprawdź, czy próbki z tego samego srodowiska tworzą skupiska.")
        print("- Jeśli punkty z gleby, wody i jelit wyraźnie się rozdzielają, oznacza to, że główne składowe")
        print("  dobrze odzwierciedlają różnice między srodowiskami.")
        print("- Jeśli klastry mocno się nachodzą, różnice między srodowiskami są słabiej zaznaczone w przestrzeni PCA.")

        # Rysowanie wykresu PCA
        plot_pca(X_pca, env, pca)
