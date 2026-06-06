import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.research_parser.text_parser import (
    extract_abstract,
    extract_keywords,
    extract_algorithms,
    extract_metrics,
    extract_title,
)


def test_extract_title_from_metadata():
    result = extract_title("some body text here", "My Paper Title")
    assert result == "My Paper Title"
    print("✅ test_extract_title_from_metadata passed")


def test_extract_title_from_text():
    text = "Deep Learning for Image Classification\nAuthor Name\nAbstract..."
    result = extract_title(text, "")
    assert len(result) > 5
    print("✅ test_extract_title_from_text passed")


def test_extract_abstract():
    text = """
    Introduction blah blah
    Abstract
    This paper proposes a new method for solving complex problems using neural networks.
    Introduction
    More text here
    """
    result = extract_abstract(text)
    assert len(result) > 10
    print("✅ test_extract_abstract passed")


def test_extract_keywords():
    text = "Keywords: machine learning, neural networks, deep learning, classification"
    result = extract_keywords(text)
    assert len(result) > 0
    assert any("machine learning" in k.lower() for k in result)
    print("✅ test_extract_keywords passed")


def test_extract_algorithms():
    text = "we used random forest and xgboost for classification. also tested svm."
    result = extract_algorithms(text)
    assert len(result) > 0
    print(f"✅ test_extract_algorithms passed — found: {result}")


def test_extract_metrics():
    text = "the model achieved 95% accuracy with an f1 score of 0.94 and auc of 0.97"
    result = extract_metrics(text)
    assert len(result) > 0
    print(f"✅ test_extract_metrics passed — found: {result}")


def test_no_false_algorithms():
    text = "this paper is about cooking recipes and food preparation"
    result = extract_algorithms(text)
    assert "Random Forest" not in result
    print("✅ test_no_false_algorithms passed")


if __name__ == "__main__":
    print("running parser tests...\n")
    test_extract_title_from_metadata()
    test_extract_title_from_text()
    test_extract_abstract()
    test_extract_keywords()
    test_extract_algorithms()
    test_extract_metrics()
    test_no_false_algorithms()
    print("\nall parser tests passed ✅")