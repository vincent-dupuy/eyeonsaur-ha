"""Module d'injection de données historiques dans le recorder."""

# pylint: disable=E0401

import logging
from datetime import datetime, timedelta
from typing import Any, cast

from homeassistant.components.recorder.models import (
    StatisticData,
    StatisticMetaData,
)
from homeassistant.components.recorder.statistics import (
    async_import_statistics,
)
from homeassistant.const import UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import as_local

try:
    # Présent à partir de HA 2025.11, obligatoire en 2026.11.
    from homeassistant.components.recorder.models import StatisticMeanType
except ImportError:  # HA <= 2025.10
    StatisticMeanType = None  # type: ignore[misc, assignment]

try:
    from homeassistant.util.unit_conversion import VolumeConverter

    _VOLUME_UNIT_CLASS: str | None = VolumeConverter.UNIT_CLASS
except (ImportError, AttributeError):  # HA très ancien
    _VOLUME_UNIT_CLASS = "volume"

_LOGGER = logging.getLogger(__name__)


def statistic_metadata(statistic_id: str) -> StatisticMetaData:
    """Métadonnées d'une statistique de somme (volume, sans moyenne).

    `mean_type` et `unit_class` sont exigés par `async_import_statistics`
    à partir de Home Assistant 2026.11. Les cores plus anciens rejettent
    ces clés dans `StatisticsMeta.from_meta` : on ne les ajoute que si
    `StatisticMeanType` est importable.
    """
    metadata: dict[str, Any] = {
        "has_mean": False,
        "has_sum": True,
        "name": f"EyeOnSaur Consumption of {statistic_id}",
        "source": "recorder",
        "statistic_id": statistic_id,
        "unit_of_measurement": UnitOfVolume.CUBIC_METERS,
    }
    if StatisticMeanType is not None:
        metadata["mean_type"] = StatisticMeanType.NONE
        metadata["unit_class"] = _VOLUME_UNIT_CLASS
    return cast("StatisticMetaData", metadata)


class SaurRecorder:
    """Service pour injecter des données.

    Service d'injection historiques dans le
    recorder de Home Assistant."""

    __skip__ = True  # Alternative pour ignorer le warning

    def __init__(self, hass: HomeAssistant):
        """Initialiser le service."""
        self.hass = hass

    async def async_inject_historical_data(
        self,
        entity_id: str,
        date: datetime,
        value: float,
    ) -> None:
        """Injecte des données historiques pour un capteur spécifique."""
        _LOGGER.debug(
            "Injecting historical data for {%s} at {%s} with value {%s}",
            entity_id,
            date,
            value,
        )

        # statistic_id = "sensor.compteur_saur_" + entity_id
        statistic_id = entity_id
        epoch = datetime(1970, 1, 1, 0, 0, 0)
        epoch = as_local(epoch)
        start_of_day = datetime(date.year, date.month, date.day, 1, 0, 0)
        start_of_day = as_local(start_of_day)
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        end_of_day = as_local(end_of_day)

        metadata = statistic_metadata(statistic_id)

        interval = timedelta(hours=1)
        stats: list[StatisticData] = []
        current_time = start_of_day + 0 * interval
        _LOGGER.debug(
            " 📜 for %s at %s with value %s",
            statistic_id,
            current_time,
            value,
        )
        stats.append(
            StatisticData(
                start=current_time,
                last_reset=epoch,
                sum=value,
            ),
        )

        async_import_statistics(self.hass, metadata, stats)

        _LOGGER.debug(
            "Injected historical data for %s at %s with value %s",
            statistic_id,
            date,
            value,
        )
