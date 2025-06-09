from cloud_components.common.enums.available_cloud import AvailableCloud


def test_available_cloud_enum_values():
    """AvailableCloud should expose AWS and GCP values"""
    assert AvailableCloud.AWS.value == "AWS"
    assert AvailableCloud.GCP.value == "GCP"
