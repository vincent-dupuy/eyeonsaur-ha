"""Tests for the EyeOnSaur recorder."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from homeassistant.const import UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import as_local

from custom_components.eyeonsaur import recorder as recorder_mod
from custom_components.eyeonsaur.recorder import (
    SaurRecorder,
    statistic_metadata,
)


@pytest.fixture(autouse=True)
def mock_recorder_module():
    """Mock the recorder module."""
    with (
        patch("custom_components.eyeonsaur.recorder.async_import_statistics"),
        patch(
            "custom_components.eyeonsaur.recorder.StatisticData",
            new_callable=Mock,
        ),
    ):
        yield


@pytest.mark.asyncio
async def test_async_inject_historical_data(hass: HomeAssistant) -> None:
    """Les stats importées portent mean_type et unit_class si dispo."""
    saur_recorder = SaurRecorder(hass)
    entity_id = "sensor.compteur_test_panneau_energie"
    date = as_local(datetime(2024, 1, 10))
    value = 100.5

    await saur_recorder.async_inject_historical_data(entity_id, date, value)

    recorder_mod.async_import_statistics.assert_called_once()
    metadata = recorder_mod.async_import_statistics.call_args.args[1]
    assert metadata["has_mean"] is False
    assert metadata["has_sum"] is True
    assert metadata["source"] == "recorder"
    assert metadata["statistic_id"] == entity_id
    assert metadata["unit_of_measurement"] == UnitOfVolume.CUBIC_METERS
    if recorder_mod.StatisticMeanType is None:
        assert "mean_type" not in metadata
        assert "unit_class" not in metadata
    else:
        assert metadata["mean_type"] is recorder_mod.StatisticMeanType.NONE
        assert metadata["unit_class"] == recorder_mod._VOLUME_UNIT_CLASS


def test_statistic_metadata_on_ha_2026_11(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """HA 2026.11 : somme seule, sans moyenne, unité volume."""

    class _MeanType:
        NONE = 0

    monkeypatch.setattr(recorder_mod, "StatisticMeanType", _MeanType)
    monkeypatch.setattr(recorder_mod, "_VOLUME_UNIT_CLASS", "volume")

    metadata = statistic_metadata("sensor.compteur_test_panneau_energie")

    assert metadata["mean_type"] == 0
    assert metadata["unit_class"] == "volume"
    assert metadata["has_mean"] is False
    assert metadata["has_sum"] is True


def test_statistic_metadata_on_older_ha(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Avant StatisticMeanType, on n'envoie pas les clés inconnues."""
    monkeypatch.setattr(recorder_mod, "StatisticMeanType", None)

    metadata = statistic_metadata("sensor.compteur_test_panneau_energie")

    assert "mean_type" not in metadata
    assert "unit_class" not in metadata
    assert metadata["has_mean"] is False
    assert metadata["has_sum"] is True
