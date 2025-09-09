import pytest
import time
import logging
from argparse import Namespace
from typing import Optional, Sequence
from datetime import datetime, timezone

from sqlalchemy import func, select

from lica.sqlalchemy import sqa_logging

from tessdbdao import ObserverType, ValidState, RegisterState

from tessdbdao.noasync import Tess

from tessdbapi.model import PhotometerInfo
from tessdbapi.noasync.photometer.register import (
    observer_id_lookup,
    location_id_lookup,
    photometer_register,
)

from . import engine, Session

from ... import DbSize, copy_file

log = logging.getLogger(__name__.split(".")[-1])


# -------------------------------
# helper functions for test cases
# -------------------------------


def photometer_lookup_current(session: Session, candidate: PhotometerInfo) -> Optional[Tess]:
    query = select(Tess).where(
        func.lower(Tess.mac_address) == candidate.mac_address.lower(),
        Tess.valid_state == ValidState.CURRENT,
    )
    return session.scalars(query).one_or_none()


def photometer_lookup_history(session: Session, candidate: PhotometerInfo) -> Sequence[Tess]:
    query = (
        select(Tess)
        .where(
            func.lower(Tess.mac_address) == candidate.mac_address.lower(),
        )
        .order_by(Tess.valid_since.asc())
    )
    return session.scalars(query).all()


def photometer_lookup_history_current(
    session: Session, candidate: PhotometerInfo
) -> Sequence[Tess]:
    query = (
        select(Tess)
        .where(
            func.lower(Tess.mac_address) == candidate.mac_address.lower(),
            Tess.valid_state == ValidState.CURRENT,
        )
        .order_by(Tess.valid_since.asc())
    )
    return session.scalars(query).all()


# ------------------
# Convenient fixtures
# -------------------


@pytest.fixture(scope="function", params=[DbSize.SMALL])
def database(request):
    args = Namespace(verbose=False)
    sqa_logging(args)
    copy_file(f"tess.{request.param}.db", "tess.db")
    yield Session()
    log.info("Teardown code disposes the engine")
    engine.dispose()


def test_register_tessw_complex(database, stars8000, stars8000rep, stars8000rep2):
    assert stars8000.tstamp is not None
    with database.begin():
        photometer_register(
            session=database,
            candidate=stars8000,
        )
        photometer_register(
            session=database,
            candidate=stars8000rep,
        )
        photometer_register(
            session=database,
            candidate=stars8000rep2,
        )
        photometers = photometer_lookup_history(database, candidate=stars8000)
        assert len(photometers) == 2
        photometers = photometer_lookup_history_current(database, candidate=stars8000)
        assert len(photometers) == 2
