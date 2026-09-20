#!/usr/bin/env python3
"""Sanity-check day-boundary and streak math used by the tracker."""
from datetime import datetime, timedelta


def local_key(d: datetime) -> str:
    return d.strftime("%Y-%m-%d")


def habit_date(d: datetime, start_hour: int = 4) -> datetime:
    return d - timedelta(hours=start_hour)


def today_key(d: datetime, start_hour: int = 4) -> str:
    return local_key(habit_date(d, start_hour))


def shift_key(key: str, days: int) -> str:
    d = datetime.strptime(key, "%Y-%m-%d")
    return local_key(d + timedelta(days=days))


def is_done(log, key, habit_id):
    return habit_id in log.get(key, [])


def current_streak(log, habit_id, t):
    start = t
    if not is_done(log, t, habit_id):
        start = shift_key(t, -1)
        if not is_done(log, start, habit_id):
            return 0
    n = 0
    k = start
    while is_done(log, k, habit_id):
        n += 1
        k = shift_key(k, -1)
    return n


def best_streak(log, habit_id):
    dates = sorted(k for k, ids in log.items() if habit_id in ids)
    if not dates:
        return 0
    best = run = 1
    for i in range(1, len(dates)):
        if shift_key(dates[i - 1], 1) == dates[i]:
            run += 1
            best = max(best, run)
        else:
            run = 1
    return best


def assert_eq(actual, expected, msg):
    if actual != expected:
        raise SystemExit(f"FAIL {msg}: got {actual!r}, expected {expected!r}")
    print("ok", msg)


def main():
    # 3:59am Monday is still Sunday; 4:00am is Monday
    mon_359 = datetime(2026, 9, 21, 3, 59)
    mon_400 = datetime(2026, 9, 21, 4, 0)
    assert_eq(today_key(mon_359), "2026-09-20", "3:59am stays previous day")
    assert_eq(today_key(mon_400), "2026-09-21", "4:00am rolls to new day")
    assert_eq(today_key(datetime(2026, 9, 20, 23, 10)), "2026-09-20", "11:10pm is still that calendar day")

    log = {
        "2026-09-17": ["gym"],
        "2026-09-18": ["gym"],
        "2026-09-19": ["gym"],
        "2026-09-20": ["gym"],
    }
    # Today not checked: streak still counts through yesterday
    assert_eq(current_streak(log, "gym", "2026-09-21"), 4, "open streak while today is empty")
    log["2026-09-21"] = ["gym"]
    assert_eq(current_streak(log, "gym", "2026-09-21"), 5, "checking today extends streak")
    assert_eq(current_streak(log, "read", "2026-09-21"), 0, "other habit has no streak")

    log["2026-09-10"] = ["gym"]
    log["2026-09-11"] = ["gym"]
    log["2026-09-12"] = ["gym"]
    assert_eq(best_streak(log, "gym"), 5, "best is the longer current run")
    # Break yesterday
    del log["2026-09-20"]
    del log["2026-09-21"]
    assert_eq(current_streak(log, "gym", "2026-09-21"), 0, "missed yesterday resets current")
    assert_eq(best_streak(log, "gym"), 3, "best still remembers the earlier run")
    print("all checks passed")


if __name__ == "__main__":
    main()
