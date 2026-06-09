"""generate_submission.py — DEPRECATED.

Stará "513 test zón / sample_submission" logika (Kaggle styl) je nahrazena reálným
suitability scoringem. Použij místo toho:

    python src/generate_scores.py

Ten vyrobí `submissions/app_zone_scores.csv` (kontrakt pro appku: suitability_score +
grid_headroom + coverage_gap + equity + doporučený typ + "proč") a zpětně kompatibilní
`submissions/sample_submission.csv` pro starší appky.
"""
import sys

if __name__ == "__main__":
    sys.exit(
        "generate_submission.py je DEPRECATED — spusť `python src/generate_scores.py` "
        "(vyrábí submissions/app_zone_scores.csv + sample_submission.csv)."
    )
