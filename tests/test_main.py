from app.main import check_disk_space, is_disk_usage_critical


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


def test_disk_usage_below_threshold_is_not_critical():
    assert not is_disk_usage_critical(79.9, 80)


def test_disk_usage_at_threshold_is_critical():
    assert is_disk_usage_critical(80, 80)


def test_disk_usage_above_threshold_is_critical():
    assert is_disk_usage_critical(85, 80)


def test_default_threshold_is_90_percent():
    assert is_disk_usage_critical(90)
    assert not is_disk_usage_critical(89.9)
