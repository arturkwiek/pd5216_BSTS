import numpy as np
import matplotlib.pyplot as plt

"""
BSTS_6 – wizualizacja zasymulowanych danych z eksperymentu BSTS_5

Badamy wpływ nowego leku przeciwzapalnego na ekspresję genu IL6.
Porównujemy dwie grupy: kontrolna (DMSO) i z lekiem.

Cel: zasymulować dane i zwizualizować je na boxplocie z naniesionymi punktami,
porównując różne parametry rozkładu (efekt leku, odchylenia standardowe).

Boxplot + punkty pozwala zobaczyć zarówno statystyki (mediana, kwartyle)
jak i faktyczną rozprzestrzeń pomiarów w małych próbach.
"""

np.random.seed(123)


def simulate_data(n_control: int, n_treated: int,
                   mu_control: float, mu_treated: float,
                   sd_control: float, sd_treated: float):
    """Generuje dane z rozkładu normalnego dla dwóch grup."""
    control = np.random.normal(loc=mu_control, scale=sd_control, size=n_control)
    treated = np.random.normal(loc=mu_treated, scale=sd_treated, size=n_treated)
    return control, treated


def plot_box_with_points(control, treated, title: str):
    """Rysuje boxplot z nałożonymi punktami dla dwóch grup."""
    data = [control, treated]
    labels = ["Kontrola", "Lek"]

    fig, ax = plt.subplots(figsize=(6, 5))

    # Boxplot
    bp = ax.boxplot(data, labels=labels, patch_artist=True,
                    boxprops=dict(facecolor="#a6cee3", alpha=0.7),
                    medianprops=dict(color="red", linewidth=2))

    # Dodanie punktów (jitter w poziomie)
    x_positions = [1, 2]
    for x, group in zip(x_positions, data):
        jitter = (np.random.rand(len(group)) - 0.5) * 0.2
        ax.scatter(np.full_like(group, x) + jitter, group,
                   color="black", alpha=0.8, s=35, zorder=3)

    ax.set_ylabel("Względna ekspresja IL6")
    ax.set_title(title)
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    return fig, ax


if __name__ == "__main__":
    n_control = 10
    n_treated = 10

    # SCENARIUSZ 1: silny efekt leku (jak w BSTS_5)
    mu_control_1 = 1.0
    mu_treated_1 = 0.6
    sd_control_1 = 0.15
    sd_treated_1 = 0.15

    control1, treated1 = simulate_data(n_control, n_treated,
                                      mu_control_1, mu_treated_1,
                                      sd_control_1, sd_treated_1)

    fig1, ax1 = plot_box_with_points(control1, treated1,
                                     "Ekspresja IL6 – silny efekt leku")

    # SCENARIUSZ 2: słabszy efekt leku i większe rozproszenie
    mu_control_2 = 1.0
    mu_treated_2 = 0.85  # mniejsza różnica średnich
    sd_control_2 = 0.2
    sd_treated_2 = 0.25  # większa wariancja w grupie z lekiem

    control2, treated2 = simulate_data(n_control, n_treated,
                                      mu_control_2, mu_treated_2,
                                      sd_control_2, sd_treated_2)

    fig2, ax2 = plot_box_with_points(control2, treated2,
                                     "Ekspresja IL6 – słabszy efekt, większa wariancja")

    # Wydruk krótkiej interpretacji
    print("SCENARIUSZ 1 – silny efekt leku:")
    print(f"Średnia kontrola = {control1.mean():.3f}, SD = {control1.std(ddof=1):.3f}")
    print(f"Średnia lek      = {treated1.mean():.3f}, SD = {treated1.std(ddof=1):.3f}")

    print("\nSCENARIUSZ 2 – słabszy efekt, większa wariancja:")
    print(f"Średnia kontrola = {control2.mean():.3f}, SD = {control2.std(ddof=1):.3f}")
    print(f"Średnia lek      = {treated2.mean():.3f}, SD = {treated2.std(ddof=1):.3f}")

    print("\nObserwacje:")
    print("- W scenariuszu 1 pudełka i punkty dwóch grup są wyraźnie rozdzielone –")
    print("  różnica średnich jest duża, a rozproszenie stosunkowo małe.")
    print("- W scenariuszu 2 pudełka silniej się nakładają, a punkty są bardziej")
    print("  rozproszone, co wizualnie odpowiada mniejszemu efektowi leku i większej")
    print("  wariancji – rozróżnienie grup staje się trudniejsze.")

    plt.show()
