from cloud_components.common.enums.available_cloud import AvailableCloud


def test_enum_values():
    """Verify that enum members expose correct values."""
    assert AvailableCloud.AWS.value == "AWS"
    assert AvailableCloud.GCP.value == "GCP"
