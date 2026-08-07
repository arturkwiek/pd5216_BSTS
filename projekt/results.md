# Wyniki analizy RNA-seq – GSE116250

## 1. Wstęp

Celem analizy było porównanie wyników różnicowej ekspresji genów uzyskanych przy pomocy narzędzia GEO2R z wynikami własnej analizy przeprowadzonej w Pythonie dla badania GSE116250 (RNA-seq lewych komór serca). Badanie obejmuje 64 próbki: 14 serc dawców bez niewydolności (non-failing, NF), 37 przypadków kardiomiopatii rozstrzeniowej (dilated cardiomyopathy, DCM) oraz 13 przypadków kardiomiopatii niedokrwiennej (ischemic cardiomyopathy, ICM).

Własna analiza w Pythonie została ograniczona do kontrastu NF vs DCM, zgodnie z konfiguracją używaną w GEO2R.

## 2. Dane i przygotowanie

### 2.1. Źródła danych

- Dane z GEO (GSE116250):
  - plik z wynikami GEO2R: `projekt/GEO/GSE116250.top.table.tsv`
  - pliki pomocnicze GEO: `projekt/GEO/GSE116250_series_matrix.txt.gz`, `projekt/GEO/GSE116250_rpkm.txt.gz`, pliki zliczeń RAW/TPM/FPKM oraz anotacje `projekt/GEO/Human.GRCh38.p13.annot.tsv.gz`
  - wykresy wygenerowane przez GEO2R: `projekt/GEO/GSE116250_GEO_plot1.jpg` – `GSE116250_GEO_plot7.jpg`

- Własna analiza w Pythonie:
  - macierz ekspresji RPKM: `projekt/GEO/GSE116250_rpkm.txt.gz`
  - metadane próbek: `projekt/GSE116250_metadata.csv` (kolumny `sample_id`, `group`, gdzie `group ∈ {NF, DCM, ICM}`)

### 2.2. Grupy porównawcze

Na podstawie pliku `GSE116250_series_matrix.txt.gz` określono typ choroby dla każdej próbki. Dla analizy różnicowej ekspresji zdefiniowano grupy:

- **NF (non-failing)** – zdrowe serca dawców, próbki: `NF1, NF2, …, NF15` (14 próbek)
- **DCM (dilated cardiomyopathy)** – kardiomiopatia rozstrzeniowa, próbki: `DCM2, DCM3, …, DCM78` (37 próbek)

Próbki ICM (`ICM47, …, ICM64`) zostały oznaczone w metadanych, ale nie były wykorzystywane w głównym teście NF vs DCM.

## 3. Analiza w GEO2R

Analiza GEO2R została przeprowadzona w interfejsie WWW GEO dla serii GSE116250 z następującą konfiguracją:

- grupa kontrolna: próbki NF
- grupa badana: próbki DCM
- metoda statystyczna: domyślny pipeline GEO2R (limma/voom, korekcja FDR Benjamini–Hochberg)

Wyniki GEO2R zostały wyeksportowane do pliku `projekt/GEO/GSE116250.top.table.tsv`, zawierającego m.in. kolumny:

- `GeneID` – identyfikator genu z NCBI
- `log2FoldChange` – log2(DCM/NF)
- `pvalue`, `padj` – wartość p i wartość skorygowana (FDR)
- `baseMean` – średnia ekspresja
- `Symbol`, `Description` – symbol i opis genu

Przykładowe wizualizacje wygenerowane przez GEO2R (boxplot rozkładu ekspresji, wykres MA/volcano, histogram p-value itd.) zostały zapisane jako pliki `projekt/GEO/GSE116250_GEO_plot1.jpg` – `GSE116250_GEO_plot7.jpg`.

## 4. Własna analiza w Pythonie

### 4.1. Skrypt i biblioteki

Analiza została zaimplementowana w skrypcie `projekt/gse116250_analysis.py` z użyciem następujących pakietów:

- `pandas`, `numpy` – wczytywanie i przetwarzanie danych
- `scipy.stats` – test t-Studenta (wariant Welcha)
- `statsmodels.stats.multitest` – korekcja FDR (metoda Benjamini–Hochberg)
- `matplotlib`, `seaborn` – wizualizacje (volcano plot, histogram log2FC)

### 4.2. Metodyka

1. Wczytanie macierzy ekspresji RPKM z pliku `GSE116250_rpkm.txt.gz` (wiersze = geny, kolumny = próbki NF/DCM/ICM).
2. Wczytanie metadanych `GSE116250_metadata.csv` i ograniczenie analizy do próbek, dla których `group ∈ {NF, DCM}`.
3. Podział macierzy na dwie podmacierze: NF oraz DCM.
4. Obliczenie średniej ekspresji w NF i DCM dla każdego genu oraz log2FC:

   $$\text{log2FC} = \log_2(\text{mean}_{\text{DCM}} + c) - \log_2(\text{mean}_{\text{NF}} + c),$$

   gdzie $c = 10^{-3}$ jest małym pseudolicznikiem zabezpieczającym przed zerami.

5. Dla każdego genu wykonano test t-Studenta (Welcha) porównujący rozkład ekspresji w grupach DCM i NF.
6. Otrzymane wartości p skorygowano metodą Benjamini–Hochberg (FDR), uzyskując kolumnę `padj`.
7. Wyniki zapisano do pliku `projekt/GSE116250_DE_results_python.tsv` z kolumnami:
   - `gene` (EnsemblGeneID), `log2FC`, `pvalue`, `padj`.

### 4.3. Wizualizacje

Wygenerowano następujące wykresy w katalogu `projekt`:

- `GSE116250_volcano.png` – volcano plot (oś X: log2FC DCM vs NF, oś Y: −log10(p-value), geny istotne FDR < 0,05 i |log2FC| ≥ 1 zaznaczone na czerwono).
- `GSE116250_log2fc_hist.png` – histogram rozkładu log2FC dla wszystkich genów.

## 5. Porównanie wyników GEO2R i Pythona

Do porównania obu analiz użyto skryptu `projekt/analyze.py`, który:

1. Wczytuje wyniki GEO2R (`GSE116250.top.table.tsv`) i własne wyniki Pythona (`GSE116250_DE_results_python.tsv`).
2. Wczytuje plik anotacji `Human.GRCh38.p13.annot.tsv.gz`, zawierający mapowanie między:
   - `GeneID` (NCBI) a `EnsemblGeneID` oraz symbolem genu (`Symbol`).
3. Łączy wyniki Pythona z anotacją po `EnsemblGeneID` (kolumna `gene`) i przypisuje do nich `GeneID`.
4. Łączy następnie tabelę GEO2R i tabelę Pythona po wspólnym `GeneID`.
5. Oblicza współczynnik korelacji Pearsona między log2FC z GEO2R i log2FC z Pythona oraz liczbę genów istotnych w każdej analizie (FDR < 0,05).

Wyniki tego porównania (wypisane w terminalu) były następujące:

- zapisano tabelę połączonych wyników do `projekt/GSE116250_geo_vs_python.tsv`
- korelacja log2FC GEO2R vs Python: około **−0,499**
- liczba genów istotnych w GEO2R (padj < 0,05): **6780**
- liczba genów istotnych w Pythonie (padj < 0,05): **0**
- liczba genów istotnych w obu analizach: **0**

### 5.1. Interpretacja

- Ujemna korelacja (~−0,5) wskazuje, że dla części genów kierunek efektu (up/down) jest przeciwny pomiędzy GEO2R a prostą analizą w Pythonie. Sugeruje to, że zastosowany pipeline w Pythonie (RPKM + test t) nie odtwarza dobrze efektów szacowanych przez limma/voom na znormalizowanych liczbach zliczeń.
- GEO2R, korzystając z pełnego modelu limma/voom i odpowiedniej normalizacji, wykrywa dużą liczbę genów różnicowo eksprymowanych (6780 genów przy FDR < 0,05). W przeciwieństwie do tego, prosty model Pythonowy po korekcji FDR nie wykrył żadnego genu istotnego (0 genów z padj < 0,05), co oznacza znacznie mniejszą czułość.
- Różnice mogą wynikać z:
  - użycia RPKM zamiast surowych zliczeń w analizie Pythonowej,
  - zastosowania prostego testu t (Welcha) zamiast modelu liniowego z shrinkage wariancji (limma),
  - specyfiki korekcji na wielokrotne testowanie przy relatywnie niewielkiej liczbie próbek.

## 6. Dyskusja i wnioski

1. **Porównanie metod** – GEO2R reprezentuje dojrzały pipeline statystyczny (limma/voom), przystosowany do danych RNA-seq i dużej liczby testów jednoczesnych. Własna analiza w Pythonie, oparta na RPKM i prostym teście t, jest bardziej demonstracją podejścia niż pełnowartościową alternatywą metodologiczną.
2. **Czułość i stabilność wyników** – duża liczba genów istotnych w GEO2R (6780) przy braku genów istotnych w Pythonie pokazuje, że właściwy dobór metody i normalizacji ma kluczowe znaczenie dla wykrywania subtelnych zmian ekspresji.
3. **Znaczenie biologiczne** – mimo różnic liczbowych, oba podejścia potwierdzają istnienie szerokich zmian transkrypcyjnych między sercami NF a DCM. Analiza GEO2R lepiej uwzględnia złożoność danych RNA-seq, dlatego powinna być traktowana jako główne źródło wyników biologicznych, natomiast analiza Pythonowa jako ilustracja procesu i możliwości reimplementacji pipeline’u.
4. **Możliwe rozszerzenia** – dalsze prace mogłyby obejmować:
   - użycie surowych zliczeń (`GSE116250_raw_counts_GRCh38.p13_NCBI.tsv.gz`) oraz bibliotek Pythonowych implementujących modele zbliżone do limma/DESeq2,
   - analizę trzech grup jednocześnie (NF, DCM, ICM),
   - integrację z informacją funkcjonalną (GO, KEGG) i analizę wzbogacenia szlaków.

## 7. Wykorzystanie AI

W realizacji projektu wsparto się modelem językowym (ChatGPT, model GPT-5.1), który został użyty do:

- zaproponowania odpowiedniego badania GEO (GSE116250) spełniającego kryteria zadania,
- zaplanowania struktury analizy (GEO2R + Python) oraz doboru bibliotek,
- wygenerowania szkieletu skryptów Pythona (`gse116250_analysis.py`, `analyze.py`) do analizy różnicowej ekspresji i porównania wyników,
- zaproponowania struktury niniejszego raportu i sformułowań opisujących wyniki.

Ostateczne uruchomienie kodu, weryfikacja poprawności działania skryptów oraz interpretacja wyników zostały wykonane lokalnie w środowisku użytkownika.
