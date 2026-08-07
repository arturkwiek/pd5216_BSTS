from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
GEO_PATH = BASE_DIR / "GEO" / "GSE116250.top.table.tsv"
PYTHON_DE_PATH = BASE_DIR / "GSE116250_DE_results_python.tsv"
ANNOT_PATH = BASE_DIR / "GEO" / "Human.GRCh38.p13.annot.tsv.gz"
MERGED_OUT = BASE_DIR / "GSE116250_geo_vs_python.tsv"


def main() -> None:
	if not GEO_PATH.exists():
		raise FileNotFoundError(f"Nie znaleziono pliku GEO2R: {GEO_PATH}")
	if not PYTHON_DE_PATH.exists():
		raise FileNotFoundError(
			f"Nie znaleziono pliku z wynikami Pythona: {PYTHON_DE_PATH}. \n"
			"Najpierw uruchom skrypt analizy różnicowej ekspresji, żeby go wygenerować."
		)
	if not ANNOT_PATH.exists():
		raise FileNotFoundError(f"Nie znaleziono pliku anotacji: {ANNOT_PATH}")

	geo = pd.read_csv(GEO_PATH, sep="\t")
	py = pd.read_csv(PYTHON_DE_PATH, sep="\t")
	annot = pd.read_csv(
		ANNOT_PATH,
		sep="\t",
		compression="gzip",
		usecols=["GeneID", "EnsemblGeneID", "Symbol"],
	)

	# Wynik Pythona: index to EnsemblGeneID (kolumna "gene") + log2FC, padj
	if "gene" not in py.columns:
		py = py.reset_index().rename(columns={"index": "gene"})

	# Dołącz mapowanie Ensembl -> GeneID, Symbol
	py_annot = pd.merge(
		py,
		annot,
		left_on="gene",
		right_on="EnsemblGeneID",
		how="inner",
	)

	# wybierz tylko potrzebne kolumny
	geo_sel = geo[["GeneID", "log2FoldChange", "padj", "Symbol"]].rename(
		columns={"log2FoldChange": "log2FC_geo", "padj": "padj_geo", "Symbol": "Symbol_geo"}
	)
	py_sel = py_annot[["GeneID", "log2FC", "padj", "Symbol"]].rename(
		columns={"padj": "padj_py", "Symbol": "Symbol_py"}
	)

	merged = pd.merge(geo_sel, py_sel, on="GeneID", how="inner", suffixes=("_geo", "_py"))

	# proste podsumowanie zgodności
	corr = merged["log2FC_geo"].corr(merged["log2FC"])
	n_geo_sig = (merged["padj_geo"] < 0.05).sum()
	n_py_sig = (merged["padj_py"] < 0.05).sum()
	n_both_sig = ((merged["padj_geo"] < 0.05) & (merged["padj_py"] < 0.05)).sum()

	merged.to_csv(MERGED_OUT, sep="\t", index=False)

	print(f"Zapisano tabelę połączonych wyników do: {MERGED_OUT.name}")
	print(f"Korelacja log2FC GEO2R vs Python: {corr:.3f}")
	print(f"Liczba genów istotnych w GEO2R (padj<0.05): {n_geo_sig}")
	print(f"Liczba genów istotnych w Pythonie (padj<0.05): {n_py_sig}")
	print(f"Liczba genów istotnych w obu analizach: {n_both_sig}")


if __name__ == "__main__":
	main()