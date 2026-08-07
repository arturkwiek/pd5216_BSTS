# pd5216_BSTS — statystyka w bioinformatyce

Osiem ćwiczeń (`BSTS_1` … `BSTS_8`), każde z **własnym logiem przebiegu**, plus projekt
zaliczeniowy na rzeczywistych danych ekspresyjnych.

## Układ

| Element | Co to |
|---|---|
| `BSTS_1.py` … `BSTS_8.py` | Kolejne ćwiczenia |
| `bsts_1_log.txt` … `bsts_8_log.txt` | Zapis wyjścia z każdego uruchomienia — dzięki temu widać wynik bez ponownego odpalania skryptu |
| `Boxplot.png`, `Dispersion.png`, `BSTS_4.png` | Wykresy wygenerowane przez ćwiczenia |
| `BSTS_8 raport.docx` | Raport końcowy z ostatniego ćwiczenia |
| `genes.tsv`, `mikrobiom.csv` | Dane wejściowe |
| `Wyniki analizy RNA.pdf` | Opracowanie wyników |
| `projekt/` | Projekt zaliczeniowy — patrz niżej |

## Projekt

`projekt/GEO/` zawiera dane z **GEO GSE116250**:

- `GSE116250_rpkm.txt.gz` (7,1 MB) — macierz ekspresji w RPKM,
- `GSE116250_norm_counts_TPM_GRCh38.p13_NCBI.tsv.gz` — zliczenia znormalizowane TPM,
- `GSE116250_norm_counts_FPKM_GRCh38.p13_NCBI.tsv.gz` — to samo w FPKM,
- `GSE116250.top.table.tsv` — tabela wyników analizy różnicowej,
- pliki `genes*.tsv` — adnotacje.

Trzy różne normalizacje (RPKM / TPM / FPKM) tej samej macierzy leżą obok siebie celowo —
to materiał do porównania, jak wybór normalizacji wpływa na wynik.

Łącznie ~30 MB danych trzymanych w repozytorium, żeby projekt był odtwarzalny bez ponownego
pobierania z GEO.

## Uruchomienie

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy matplotlib scipy    # zależnie od ćwiczenia
python BSTS_4.py
```

Zanim uruchomisz ćwiczenie od nowa, zajrzyj do odpowiadającego mu `bsts_*_log.txt` —
zwykle wystarczy, żeby przypomnieć sobie, co dane ćwiczenie robi i jaki dało wynik.

## Status

⚪ **Zamknięty** — zajęcia zaliczone. Submoduł repozytorium `PJWSTK`.
