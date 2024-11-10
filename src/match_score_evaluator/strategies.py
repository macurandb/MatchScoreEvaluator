from abc import ABC, abstractmethod
from typing import Any, Optional
from rapidfuzz.distance import Levenshtein, JaroWinkler


class SimilarityStrategy(ABC):
    @abstractmethod
    def calculate(self, value1: Any, value2: Any, column_name: Optional[str] = None) -> float:
        pass


class NameSimilarity(SimilarityStrategy):
    def calculate(self, value1: str, value2: str, column_name: Optional[str] = None) -> float:
        value1 = value1 or ""
        value2 = value2 or ""
        return JaroWinkler.similarity(value1, value2)


class EmailSimilarity(SimilarityStrategy):
    def calculate(self, value1: str, value2: str, column_name: Optional[str] = None) -> float:
        value1 = value1 or ""
        value2 = value2 or ""
        return Levenshtein.normalized_similarity(value1, value2)


class ZipCodeSimilarity(SimilarityStrategy):
    def calculate(self, value1: str, value2: str, column_name: Optional[str] = None) -> float:
        if value1 is None or value2 is None:
            return 0.0
        return 1.0 if value1 == value2 else 0.0


class AddressSimilarity(SimilarityStrategy):
    def calculate(self, value1: str, value2: str, column_name: Optional[str] = None) -> float:
        value1 = value1 or ""
        value2 = value2 or ""
        set1, set2 = set(value1.split()), set(value2.split())
        return len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0.0
