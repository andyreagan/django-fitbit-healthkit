from datetime import date
from typing import Dict

from .models import FitbitUser

DAILY_ACTIVITY_SUMMARY_URL = (
    "https://api.fitbit.com/1/user/-/activities/date/{date}.json"
)
SLEEP_LOG_BY_DATE_URL = "https://api.fitbit.com/1.2/user/-/sleep/date/{date}.json"
SLEEP_LOG_BY_DATE_RANGE_URL = (
    "https://api.fitbit.com/1.2/user/-/sleep/date/{start_date}/{end_date}.json"
)
ACTIVITY_INTRADAY_BY_DATE_URL = "https://api.fitbit.com/1/user/-/activities/{activity}/date/{date}/1d/{interval}.json"
ACTIVITY_TIMESERIES_BY_DATE_URL = (
    "https://api.fitbit.com/1/user/-/activities/{resource}/date/{date}/{period}.json"
)
ACTIVITY_TIMESERIES_BY_DATE_RANGE_URL = "https://api.fitbit.com/1/user/-/activities/{resource}/date/{start_date}/{end_date}.json"


def daily_activity_summary(fitbitUser: FitbitUser, d: date) -> Dict:
    """
    ref: https://dev.fitbit.com/build/reference/web-api/activity/get-daily-activity-summary/
    format: /1/user/[user-id]/activities/date/[date].json
    """
    url = DAILY_ACTIVITY_SUMMARY_URL.format(date=d.isoformat())
    response, err = fitbitUser.make_request("get", url)
    print(response, err)
    if err is None:
        return response.json()
    return {}


def sleep_log_by_date(fitbitUser: FitbitUser, d: date) -> Dict:
    """
    ref: https://dev.fitbit.com/build/reference/web-api/sleep/get-sleep-log-by-date/
    format: /1.2/user/[user-id]/sleep/date/[date].json
    """
    url = SLEEP_LOG_BY_DATE_URL.format(date=d.isoformat())
    response, err = fitbitUser.make_request("get", url)
    print(response, err)
    if err is None:
        return response.json()
    return {}


def sleep_log_by_date_range(
    fitbitUser: FitbitUser, start_date: date, end_date: date
) -> Dict:
    """
    ref: https://dev.fitbit.com/build/reference/web-api/sleep/get-sleep-log-by-date-range/
    format: /1.2/user/[user-id]/sleep/date/[startDate]/[endDate].json

    note maximum range: 100 days
    """
    # check max range
    if (end_date - start_date).days > 100:
        print("Date range is too long, won't try to fetch data.")
        return {}
    url = SLEEP_LOG_BY_DATE_RANGE_URL.format(
        start_date=start_date.isoformat(), end_date=end_date.isoformat()
    )
    response, err = fitbitUser.make_request("get", url)
    print(response, err)
    if err is None:
        return response.json()
    return {}


def activity_intraday_by_date(
    fitbitUser: FitbitUser, activity: str, d: date, interval: str
) -> Dict:
    """
    ref: https://dev.fitbit.com/build/reference/web-api/intraday/get-activity-intraday-by-date/
    format:
    * /1/user/[user-id]/activities/[resource]/date/[date]/1d/[detail-level].json
    * /1/user/[user-id]/activities/[resource]/date/[date]/1d/[detail-level]/time/[start-time]/[end-time].json
    """
    # calories | distance | elevation | floors | steps
    if activity not in ["calories", "distance", "elevation", "floors", "steps"]:
        print(f"Invalid activity {activity}, won't try to fetch data.")
        return {}
    # 1min | 5min | 15min
    if interval not in ["1min", "5min", "15min"]:
        print(f"Invalid interval {interval}, won't try to fetch data.")
        return {}
    url = ACTIVITY_INTRADAY_BY_DATE_URL.format(
        activity=activity, date=d, interval=interval
    )
    print(url)
    response, err = fitbitUser.make_request("get", url)
    print(response, err)
    if err is None:
        return response.json()
    return {}


def activity_timeseries_by_date(
    fitbitUser: FitbitUser, resource: str, d: date, period: str
) -> Dict:
    """
    ref: https://dev.fitbit.com/build/reference/web-api/activity-timeseries/get-activity-timeseries-by-date/
    format: /1/user/[user-id]/activities/[resource-path]/date/[date]/[period].json
    """
    all_activity_resources = [
        "activityCalories",
        "calories",
        "caloriesBMR",
        "distance",
        "elevation",
        "floors",
        "minutesSedentary",
        "minutesLightlyActive",
        "minutesFairlyActive",
        "minutesVeryActive",
        "steps",
    ]
    tracker_only_resources = [
        "tracker/activityCalories",
        "tracker/calories",
        "tracker/distance",
        "tracker/elevation",
        "tracker/floors",
        "tracker/minutesSedentary",
        "tracker/minutesLightlyActive",
        "tracker/minutesFairlyActive",
        "tracker/minutesVeryActive",
        "tracker/steps",
    ]
    if resource not in all_activity_resources + tracker_only_resources:
        print(f"Invalid resource {resource}, won't try to fetch data.")
        return {}
    if period not in ["1d", "7d", "30d", "1w", "1m", "3m", "6m", "1y"]:
        print(f"Invalid period {period}, won't try to fetch data.")
        return {}
    url = ACTIVITY_TIMESERIES_BY_DATE_URL.format(
        resource=resource, date=d, period=period
    )
    print(url)
    response, err = fitbitUser.make_request("get", url)
    print(response, err)
    if err is None:
        return response.json()
    return {}


def activity_timeseries_by_date_range(
    fitbitUser: FitbitUser, resource: str, start_date: date, end_date: date
) -> Dict:
    """
    ref: https://dev.fitbit.com/build/reference/web-api/activity-timeseries/get-activity-timeseries-by-date-range/
    format: /1/user/[user-id]/activities/[resource-path]/date/[start-date]/[end-date].json

    note maximum range: 30 days for calories, 1095 days for everything else
    """
    # check max range
    if (
        resource in {"activityCalories", "tracker/activityCalories"}
        and (end_date - start_date).days > 30
    ):
        print("Date range is too long, won't try to fetch data.")
        return {}
    elif (end_date - start_date).days > 1095:
        print("Date range is too long, won't try to fetch data.")
        return {}
    all_activity_resources = [
        "activityCalories",
        "calories",
        "caloriesBMR",
        "distance",
        "elevation",
        "floors",
        "minutesSedentary",
        "minutesLightlyActive",
        "minutesFairlyActive",
        "minutesVeryActive",
        "steps",
    ]
    tracker_only_resources = [
        "tracker/activityCalories",
        "tracker/calories",
        "tracker/distance",
        "tracker/elevation",
        "tracker/floors",
        "tracker/minutesSedentary",
        "tracker/minutesLightlyActive",
        "tracker/minutesFairlyActive",
        "tracker/minutesVeryActive",
        "tracker/steps",
    ]
    if resource not in all_activity_resources + tracker_only_resources:
        print(f"Invalid resource {resource}, won't try to fetch data.")
        return {}
    url = ACTIVITY_TIMESERIES_BY_DATE_RANGE_URL.format(
        resource=resource,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
    )
    print(url)
    response, err = fitbitUser.make_request("get", url)
    print(response, err)
    if err is None:
        return response.json()
    return {}
