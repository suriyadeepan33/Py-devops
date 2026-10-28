
from app.main import check_disk_space


def test_disk_space_returns_expected_fields():
    result = check_disk_space("/")

    assert result["path"] == "/"
    assert result["total_gb"] > 0
    assert result["used_gb"] >= 0
    assert result["free_gb"] >= 0
    assert 0 <= result["usage_percent"] <= 100


def test_disk_space_values_are_rounded():
    result = check_disk_space("/")

    assert isinstance(result["total_gb"], float)
    assert isinstance(result["used_gb"], float)
    assert isinstance(result["free_gb"], float)
    assert isinstance(result["usage_percent"], float)
