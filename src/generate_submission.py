"""generate_submission.py — Submission CSV pro hackathon (513 test zón).

Predikuje:
  1. estimated_ev_count_2030_synthetic (demand)
  2. target_recommended_solution_synthetic (station type)

Výstup: submissions/sample_submission.csv

    python src/generate_submission.py
"""
from __future__ import annotations

import pathlib
import pickle
import polars as pl

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "participants"
SUB = pathlib.Path(__file__).resolve().parent.parent / "submissions"
MODEL_PATH = SUB / "lgbm_model.pkl"
SOLUTIONS_PATH = DATA / "candidate_solutions.csv"


def load_model_and_data() -> tuple:
    """Load trained model, features, and test data."""
    if not MODEL_PATH.exists():
        print(f"⚠ Model {MODEL_PATH} not found. Using fallback predictions.")
        return None, None, None

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    # Load validation set as test (since no explicit test set provided)
    test_df = pl.read_csv(DATA / "zones_validation.csv")
    solutions = pl.read_csv(SOLUTIONS_PATH)

    return model, test_df, solutions


def map_ev_count_to_solution(ev_count: float) -> str:
    """Map predicted EV count to recommended solution type."""
    if ev_count < 50:
        return "none_monitor"
    elif ev_count < 200:
        return "residential_ac_small"
    elif ev_count < 500:
        return "residential_ac_medium"
    elif ev_count < 1500:
        return "destination_dc50"
    elif ev_count < 3000:
        return "fast_hub_150"
    else:
        return "mixed_mobility_hub"


def generate_submission() -> None:
    """Generate submission CSV for test zones."""
    print("=" * 70)
    print("VoltPlán — Submission Generation")
    print("=" * 70)

    model, test_df, solutions = load_model_and_data()

    if model is None or test_df is None:
        print("\n⚠ Using fallback dummy predictions...")
        # Fallback: use validation set with simple heuristics
        test_df = pl.read_csv(DATA / "zones_validation.csv")

    # Features (must match training)
    exclude_cols = {
        "grid_zone_id",
        "transformer_station_id_real",
        "parent_substation_id_real",
        "split",
        "estimated_ev_count_2030_synthetic",
        "target_daily_charging_kwh_2030_synthetic",
        "target_peak_charging_kw_2030_synthetic",
        "target_overload_probability_2030_synthetic",
        "target_recommended_solution_synthetic",
        "target_recommended_ports_synthetic",
        "target_recommended_total_kw_synthetic",
    }
    features = [c for c in test_df.columns if c not in exclude_cols]

    # Prepare test features
    X_test = test_df.select(features).to_numpy(allow_null=True)

    # Predict EV count
    if model:
        ev_predictions = model.predict(X_test)
    else:
        # Fallback: use population as proxy
        ev_predictions = (
            test_df.select("population_census_2021_real")
            .to_numpy()
            .flatten()
            / 10.0
        )

    # Ensure non-negative
    ev_predictions = [max(0, x) for x in ev_predictions]

    # Map to solution types
    solution_types = [
        map_ev_count_to_solution(ev) for ev in ev_predictions
    ]

    # Load solution specs for ports/power
    solution_specs = {
        row["solution_type"]: row
        for row in solutions.to_dicts()
    }

    # Build output
    output = test_df.select("grid_zone_id").with_columns(
        pl.Series(
            "estimated_ev_count_2030_synthetic",
            ev_predictions,
        ),
        pl.Series(
            "target_recommended_solution_synthetic",
            solution_types,
        ),
    )

    # Add ports + power from solution specs
    ports = [
        solution_specs[st].get("ports", 0)
        for st in solution_types
    ]
    power = [
        solution_specs[st].get("total_power_kw", 0)
        for st in solution_types
    ]

    output = output.with_columns(
        pl.Series("target_recommended_ports_synthetic", ports),
        pl.Series("target_recommended_total_kw_synthetic", power),
    )

    # Write submission
    SUB.mkdir(exist_ok=True)
    output.write_csv(SUB / "sample_submission.csv")

    print(f"\n>>> Submission CSV generated:")
    print(f"    Zones: {len(output)}")
    print(f"    Columns: {output.columns}")
    print(f"    Output: {SUB / 'sample_submission.csv'}")

    print(f"\n>>> Samplení prvních 10 zón:")
    print(output.head(10))

    print("\n" + "=" * 70)
    print("✅ READY FOR HACKATHON SUBMISSION")
    print("=" * 70)


if __name__ == "__main__":
    generate_submission()
