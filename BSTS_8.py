"""
BSTS_8 – analiza różnicowej ekspresji genów w GEO2R (GSE53697)

To zadanie wymaga skorzystania z serwisu GEO (Gene Expression Omnibus) oraz
interaktywnego narzędzia GEO2R w przeglądarce, nie z poziomu Pythona.
Poniżej znajduje się instrukcja krok po kroku, którą możesz wykorzystać
podczas wykonywania analizy.

1. Otwórz stronę GEO
   - Uruchom przeglądarkę internetową.
   - Wejdź na stronę: https://www.ncbi.nlm.nih.gov/geo/

2. Wyszukaj badanie "GSE53697"
   - W polu wyszukiwania na górze strony wpisz: GSE53697
   - Zatwierdź wyszukiwanie (Enter).
   - Na liście wyników kliknij odnośnik do serii GSE53697
     (Series: GSE53697).

3. Zapoznaj się z opisem badania
   - Na stronie GSE53697 przeczytaj opis (Summary, Overall design), aby
     potwierdzić, że:
     * badanie dotyczy próbek RNA-Seq od pacjentów z zaawansowaną chorobą
       Alzheimera oraz próbek kontrolnych,
     * celem jest monitorowanie zmian poziomów RNA podczas progresji choroby.

4. Uruchom narzędzie GEO2R
   - Na stronie serii GSE53697 (Series) znajdź przycisk "Analyze with GEO2R".
   - Kliknij ten przycisk – otworzy się interfejs GEO2R.

5. Zdefiniuj grupy w GEO2R (Define groups)
   - W lewym panelu zobaczysz listę wszystkich próbek (Sample list) wraz z
     ich oznaczeniami.
   - Kliknij przycisk "Define groups".
   - Utwórz co najmniej dwie grupy (np. Group 1, Group 2):
     * Group 1 – próbki kontrolne (zdrowe / control),
     * Group 2 – próbki pacjentów z zaawansowaną chorobą Alzheimera.
   - Przypisz odpowiednie próbki do grupy kontrolnej i eksperymentalnej
     na podstawie ich opisów (Title / Characteristics), np.:
     * kontrolne: próbki oznaczone jako "control", "non-demented" itp.,
     * eksperymentalne: próbki z opisaną chorobą Alzheimera.
   - Zatwierdź przypisanie próbek do grup.

6. Ustawienia analizy (opcjonalnie)
   - W razie potrzeby możesz zmienić domyślne ustawienia GEO2R (np. metoda
     normalizacji, korekcję wielokrotnego testowania), ale do podstawowej
     analizy zwykle wystarczają ustawienia domyślne.

7. Uruchom analizę
   - Upewnij się, że grupy są poprawnie zdefiniowane.
   - Kliknij przycisk "Analyze".
   - GEO2R wykona analizę różnicowej ekspresji genów między grupą kontrolną
     i eksperymentalną (np. przy użyciu pakietu limma w R).

8. Obejrzyj wygenerowane wykresy
   Po zakończeniu analizy GEO2R zazwyczaj udostępnia kilka typów wykresów,
   np.:
   - Boxplot dla próbek przed i po normalizacji,
   - Histogramy / density plot rozkładu wartości,
   - Volcano plot (log2FC vs. -log10(p-value)),
   - Wykresy MA itp.

   Aby pobrać wykresy:
   - Pod każdym wykresem zwykle znajduje się link lub przycisk "Save" / "Download".
   - Kliknij go i zapisz wykres jako plik (np. PNG, PDF) na swoim komputerze.

9. Pobierz tabelę z wynikami analizy
   - W części "Top genes" lub podobnej GEO2R wyświetla tabelę z wynikami
     analizy różnicowej ekspresji (ID genu, log2FC, p-value, adj. p-value, itp.).
   - Aby pobrać pełną tabelę wyników:
     * poszukaj linku typu "Save all results", "Download full table" lub
       ikony pobierania;
     * wybierz format wyjściowy (np. TXT, CSV, Excel),
     * zapisz plik na dysku.

10. Dokumentacja / raport
   - W raporcie z zadania możesz umieścić:
     * krótkie streszczenie badania GSE53697 (czego dotyczy, jakie próbki,
       jaki cel),
     * zrzuty ekranu lub zapisane pliki wykresów z GEO2R,
     * tabelę wyników (lub jej fragment) z zaznaczonymi genami o istotnie
       zmienionej ekspresji (np. adj. p-value < 0.05, |log2FC| > 1),
     * krótki opis interpretacji uzyskanych wyników.

Uwaga: Powyższe kroki opisują ręczne korzystanie z GEO2R w przeglądarce.
Analiza jest wykonywana po stronie serwera GEO i nie można jej w pełni
zautomatyzować w tym prostym skrypcie Pythona.
"""

if __name__ == "__main__":
    print("To zadanie wymaga pracy w przeglądarce z użyciem GEO2R.")
    print("Przeczytaj instrukcję w docstringu pliku BSTS_8.py i wykonaj kroki ręcznie.")
