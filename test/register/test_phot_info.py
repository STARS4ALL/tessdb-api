import logging
from datetime import datetime, timezone

from tessdbdao import PhotometerModel
from tessdbapi.model import PhotometerInfo


log = logging.getLogger(__name__.split(".")[-1])


def test_valid_tstamp_missing():
    msg = PhotometerInfo(
        name="stars1",
        mac_address="AA:BB:CC:DD:EE:FF",
        model=PhotometerModel.TESSW,
        zp1=20.50,
        filter1="UV/IR-740",
        offset1=0,
    )
    log.info("%s", msg.tstamp)


def test_valid_tstamp_none():
    msg = PhotometerInfo(
        tstamp=None,
        name="stars1",
        mac_address="AA:BB:CC:DD:EE:FF",
        model=PhotometerModel.TESSW,
        zp1=20.50,
        filter1="UV/IR-740",
        offset1=0,
    )
    log.info("%s", msg.tstamp)


def test_valid_tstamp_datetime_obj():
    msg = PhotometerInfo(
        tstamp=datetime.now(timezone.utc),
        name="stars1",
        mac_address="AA:BB:CC:DD:EE:FF",
        model=PhotometerModel.TESSW,
        zp1=20.50,
        filter1="UV/IR-740",
        offset1=0,
    )
    log.info("%s", msg.tstamp)


def test_valid_tstamp_datetime_str():
    msg = PhotometerInfo(
        tstamp="2025-09-08 09:40:09",
        name="stars1",
        mac_address="AA:BB:CC:DD:EE:FF",
        model=PhotometerModel.TESSW,
        zp1=20.50,
        filter1="UV/IR-740",
        offset1=0,
    )
    log.info("%s", msg.tstamp)


def test_valid_tstamp_datetime_str_tzone():
    value = "2025-09-08 09:40:09:+02:00"
    msg = PhotometerInfo(
        tstamp=value,
        name="stars1",
        mac_address="AA:BB:CC:DD:EE:FF",
        model=PhotometerModel.TESSW,
        zp1=20.50,
        filter1="UV/IR-740",
        offset1=0,
    )
    expected = datetime.strptime(value, "%Y-%m-%d %H:%M:%S:%z").astimezone(timezone.utc)
    log.info("Before: %s", value)
    log.info("After: %s, tzinfo is %s", expected, expected.tzinfo)
    log.info("Msg: %s", msg.tstamp)
    assert msg.tstamp == expected
   
def test_valid_tstamp_datetime_str_z():
    value = "2025-09-08 09:40:09Z"
    msg = PhotometerInfo(
        tstamp=value,
        name="stars1",
        mac_address="AA:BB:CC:DD:EE:FF",
        model=PhotometerModel.TESSW,
        zp1=20.50,
        filter1="UV/IR-740",
        offset1=0,
    )
    expected = datetime.strptime(value, "%Y-%m-%d %H:%M:%SZ").replace(tzinfo=timezone.utc)
    log.info("Before: %s", value)
    log.info("After: %s, tzinfo is %s", expected, expected.tzinfo)
    log.info("Msg: %s", msg.tstamp)
    assert msg.tstamp == expected
  