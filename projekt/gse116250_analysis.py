import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "GEO"

EXPRESSION_FILE = DATA_DIR / "GSE116250_rpkm.txt.gz"
METADATA_FILE = BASE_DIR / "GSE116250_metadata.csv"
OUTPUT_DE = BASE_DIR / "GSE116250_DE_results_python.tsv"
VOLCANO_PNG = BASE_DIR / "GSE116250_volcano.png"
LOG2FC_HIST_PNG = BASE_DIR / "GSE116250_log2fc_hist.png"


def load_data(expr_path: Path = EXPRESSION_FILE, meta_path: Path = METADATA_FILE):
    expr = pd.read_csv(expr_path, sep="\t", index_col=0)
    meta = pd.read_csv(meta_path)

    required_cols = {"sample_id", "group"}
    if not required_cols.issubset(meta.columns):
        raise ValueError("Metadata file must contain columns: sample_id, group")

    meta = meta[meta["group"].isin(["NF", "DCM"])].copy()

    missing = set(meta["sample_id"]) - set(expr.columns)
    if missing:
        raise ValueError(f"Samples from metadata not found in expression matrix: {sorted(missing)}")

    expr = expr.loc[:, meta["sample_id"]]
    return expr, meta


def differential_expression(expr: pd.DataFrame, meta: pd.DataFrame, pseudocount: float = 1e-3) -> pd.DataFrame:
    groups = meta.set_index("sample_id")["group"]
    nf_samples = groups[groups == "NF"].index
    dcm_samples = groups[groups == "DCM"].index

    nf_expr = expr[nf_samples]
    dcm_expr = expr[dcm_samples]

    mean_nf = nf_expr.mean(axis=1)
    mean_dcm = dcm_expr.mean(axis=1)
    log2fc = np.log2(mean_dcm + pseudocount) - np.log2(mean_nf + pseudocount)

    t_stat, p_values = stats.ttest_ind(
        dcm_expr.T,
        nf_expr.T,
        equal_var=False,
        nan_policy="omit",
    )

    result = pd.DataFrame(
        {
            "gene": expr.index,
            "log2FC": log2fc.values,
            "pvalue": p_values,
        }
    ).set_index("gene")

    result["padj"] = multipletests(result["pvalue"], method="fdr_bh")[1]
    result = result.sort_values("padj")
    return result


def make_volcano(result: pd.DataFrame, output_path: Path = VOLCANO_PNG, alpha: float = 0.05, lfc_threshold: float = 1.0):
    df = result.dropna(subset=["log2FC", "pvalue"]).copy()
    df["neg_log10_p"] = -np.log10(df["pvalue"])
    df["significant"] = (df["padj"] < alpha) & (df["log2FC"].abs() >= lfc_threshold)
    # usuwamy ewentualne duplikaty indeksu, żeby seaborn/pandas nie miały problemu z reindexing
    df = df.reset_index(drop=True)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df,
        x="log2FC",
        y="neg_log10_p",
        hue="significant",
        palette={False: "grey", True: "red"},
        edgecolor=None,
        s=10,
        alpha=0.7,
        legend=False,
    )
    plt.axvline(x=lfc_threshold, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=-lfc_threshold, color="black", linestyle="--", linewidth=1)
    plt.axhline(y=-np.log10(alpha), color="black", linestyle="--", linewidth=1)
    plt.xlabel("log2(DCM / NF)")
    plt.ylabel("-log10(p-value)")
    plt.title("GSE116250: Volcano plot (DCM vs NF)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def make_log2fc_hist(result: pd.DataFrame, output_path: Path = LOG2FC_HIST_PNG, bins: int = 60):
    plt.figure(figsize=(8, 6))
    sns.histplot(result["log2FC"].dropna(), bins=bins, kde=False)
    plt.xlabel("log2FC (DCM vs NF)")
    plt.ylabel("Number of genes")
    plt.title("GSE116250: Distribution of log2FC")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    expr, meta = load_data()
    de = differential_expression(expr, meta)
    de.to_csv(OUTPUT_DE, sep="\t")
    make_volcano(de)
    make_log2fc_hist(de)
    print(f"Differential expression results written to {OUTPUT_DE.name}")
    print(f"Volcano plot saved to {VOLCANO_PNG.name}")
    print(f"log2FC histogram saved to {LOG2FC_HIST_PNG.name}")


if __name__ == "__main__":
    main()
