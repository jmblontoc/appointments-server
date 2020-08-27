from datetime import datetime, timedelta

format = "%Y-%m-%dT%H:%M"


def is_conflict(item1, item2):

    # UTC+8 hours offset
    # Asia/Manila Timezone
    UTC_OFFSET = 8

    from2_date = item2.from_date.date()
    from2_time = item2.from_date.time()

    to2_date = item2.to_date.date()
    to2_time = item2.to_date.time()

    from1 = datetime.strptime(item1['from_date'], format)
    to1 = datetime.strptime(item1['to_date'], format)
    from2 = datetime.combine(from2_date, from2_time) + \
        timedelta(hours=UTC_OFFSET)
    to2 = datetime.combine(to2_date, to2_time) + timedelta(hours=UTC_OFFSET)

    return from1 <= to2 and from2 <= to1


def is_valid_appointment_date(data):
    from_date = datetime.strptime(data['from_date'], format)
    to_date = datetime.strptime(data['to_date'], format)

    if from_date.weekday() == 6 or to_date.weekday() == 6:
        return False

    if (from_date.hour < 9 or from_date.hour > 17 or to_date.hour < 9 or to_date.hour > 17):
        return False

    return True
