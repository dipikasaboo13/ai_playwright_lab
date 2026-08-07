"""
AI Data Loader Utility.
Loads and filters test datasets from data/ai_generated_dataset.json for Pytest parameterization.
"""

import json
from typing import List, Dict, Optional
from config import DATA_DIR


def load_ai_dataset(category: Optional[str] = None) -> List[Dict]:
    """
    Load test cases from ai_generated_dataset.json.
    Optionally filter by category ('positive', 'negative', 'boundary', 'exception').
    """
    dataset_path = DATA_DIR / "ai_generated_dataset.json"
    if not dataset_path.exists():
        raise FileNotFoundError(f"AI dataset file not found at: {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases = data.get("test_cases", [])
    if category:
        test_cases = [tc for tc in test_cases if tc.get("category") == category]

    return test_cases


def filter_dataset_by_feature(feature: str, category: Optional[str] = None) -> List[Dict]:
    """Filter dataset cases by target feature area and optional category."""
    test_cases = load_ai_dataset(category=category)
    return [tc for tc in test_cases if tc.get("feature") == feature]
