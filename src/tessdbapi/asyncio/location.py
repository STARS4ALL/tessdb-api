# ----------------------------------------------------------------------
# Copyright (c) 2024 Rafael Gonzalez.
#
# See the LICENSE file for details
# ----------------------------------------------------------------------

# --------------------
# System wide imports
# -------------------

import asyncio
import logging

from typing import Optional

# -------------------
# Third party imports
# -------------------


from sqlalchemy import select

from tessdbdao.asyncio import Location

# --------------
# local imports
# -------------

from ..util import Session
from ..model import LocationInfo, GEO_COORD_EPSILON as EPSILON
from ..location_common import geolocate

# ----------------
# Global variables
# ----------------


log = logging.getLogger(__name__.split(".")[-1])

# -------------
# API functions
# -------------

async def location_lookup(session: Session, candidate: LocationInfo) -> Optional[Location]:
    query = select(Location).where(
        Location.longitude.between(candidate.longitude - EPSILON, candidate.longitude + EPSILON),
        Location.latitude.between(candidate.latitude - EPSILON, candidate.latitude + EPSILON),
    )
    return (await session.scalars(query)).one_or_none()


async def location_create(
    session: Session,
    candidate: LocationInfo,
    dry_run: bool = False,
) -> None:
    location = await location_lookup(session, candidate)
    if location:
        log.warning("Location already exists")
        return
    geolocated = await asyncio.to_thread(geolocate, candidate.longitude, candidate.latitude)
    location = Location(
        longitude=candidate.longitude,
        latitude=candidate.latitude,
        elevation=candidate.height,
        place=candidate.place,
        town=candidate.town or geolocated["town"],
        sub_region=candidate.sub_region or geolocated["sub_region"],
        region=candidate.region or geolocated["region"],
        country=candidate.country or geolocated["country"],
        timezone=candidate.timezone or geolocated["timezone"],
    )
    session.add(location)
    if dry_run:
        log.warning("Dry run mode. Database not written")
        await session.rollback()


async def location_update(
    session: Session,
    candidate: LocationInfo,
    dry_run: bool = False,
) -> None:
    location = await location_lookup(session, candidate)
    if not location:
        log.info(
            "Location not found using coodinates Long=%s, Lat=%s",
            candidate.longitude,
            candidate.latitude,
        )
        return
    location.elevation = candidate.height or location.elevation
    location.place = candidate.place or location.place
    location.town = candidate.town or location.town
    location.sub_region = candidate.sub_region or location.sub_region
    location.region = candidate.region or location.region
    location.country = candidate.country or location.country
    location.timezone = candidate.timezone or location.timezone
    session.add(location)
    if dry_run:
        log.warning("Dry run mode. Database not written")
        await session.rollback()
