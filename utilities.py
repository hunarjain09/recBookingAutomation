import bisect
from datetime import datetime, timedelta

# reserved_time_ranges_outside = [['2:00 PM', '3:00 PM'], ['6:00 PM', '7:00 PM'], ['10:00 PM', '11:00 PM']]
# predefined_range_outside = ['5:00 PM', '9:00 PM']
# curr_time_outside = '1:00 PM'


def convert_to_datetime(time):
    return datetime.strptime(time, '%I:%M %p')


def get_start_end_time_range(predefined_range, curr_time):
    predefined_range[0] = max(predefined_range[0], curr_time)
    predefined_range[1] = max(predefined_range[1], curr_time)
    if predefined_range[0] != predefined_range[1]:
        start_time_range = [predefined_range[0], predefined_range[0]]
        end_time_range = [predefined_range[1], predefined_range[1]]
        return (start_time_range, end_time_range)

    return None


def datetime_to_string(datetime_obj: datetime):
    return datetime_obj.strftime('%I:%M %p')


def check_and_insert_time_range(reserved_time_ranges, time_range_to_insert):
    start_time = time_range_to_insert[0]
    end_time = time_range_to_insert[1]

    for i in range(len(reserved_time_ranges)):
        if start_time <= reserved_time_ranges[i][0] <= end_time or start_time <= reserved_time_ranges[i][
            1] <= end_time or (reserved_time_ranges[i][0] <= start_time and reserved_time_ranges[i][1] >= end_time):
            # print(datetime_to_string(start_time),datetime_to_string(end_time),datetime_to_string(reserved_time[0]),datetime_to_string(reserved_time[1]))
            return i

    insert_index = bisect.bisect_left(reserved_time_ranges, time_range_to_insert, lo=0, hi=len(reserved_time_ranges))
    reserved_time_ranges.insert(insert_index, time_range_to_insert)

    return insert_index


def print_reserved_time_ranges(reserved_time_ranges):
    for reserved_time_range in reserved_time_ranges:
        print(datetime_to_string(reserved_time_range[0]) + '-' + datetime_to_string(reserved_time_range[1]))


def get_available_slot(reserved_time_ranges, predefined_range, curr_time, first_available=True):
    for i in range(len(reserved_time_ranges)):
        for j in range(len(reserved_time_ranges[i])):
            reserved_time_ranges[i][j] = convert_to_datetime(reserved_time_ranges[i][j])
    reserved_time_ranges = sorted(reserved_time_ranges,key=lambda time_range:time_range[0])
    curr_time = convert_to_datetime(curr_time)
    predefined_range[0] = convert_to_datetime(predefined_range[0])
    predefined_range[1] = convert_to_datetime(predefined_range[1])

    time_ranges_to_insert = get_start_end_time_range(predefined_range, curr_time)

    if time_ranges_to_insert:
        start_time_range = time_ranges_to_insert[0]
        end_time_range = time_ranges_to_insert[1]

        if not reserved_time_ranges:
            return [{
                'start_time': f'{datetime_to_string(predefined_range[0])}',
                'end_time': f'{datetime_to_string(predefined_range[0] + timedelta(hours=1))}'
            }]

        index_to_start_from = check_and_insert_time_range(reserved_time_ranges, start_time_range)

        index_to_end_at = check_and_insert_time_range(reserved_time_ranges, end_time_range)

        reserved_time_ranges = reserved_time_ranges[index_to_start_from:index_to_end_at + 1]

        available_slots = []
        prev_end_time = reserved_time_ranges[0][1]
        print_reserved_time_ranges(reserved_time_ranges)
        for i in range(1, len(reserved_time_ranges)):
            curr_start_time = reserved_time_ranges[i][0]
            time_diff = curr_start_time - prev_end_time
            if time_diff.seconds >= 3600:
                available_slots.append([prev_end_time, prev_end_time + timedelta(hours=1)])
            prev_end_time = reserved_time_ranges[i][1]

        if available_slots:
            if first_available:
                return [{
                    'start_time': f'{datetime_to_string(available_slots[0][0])}',
                    'end_time': f'{datetime_to_string(available_slots[0][0] + timedelta(hours=1))}'
                }]
            else:
                # Converting list of lists to list of dict
                for i in range(len(available_slots)):
                    available_slots[i] = {
                        'start_time': f'{datetime_to_string(available_slots[i][0])}',
                        'end_time': f'{datetime_to_string(available_slots[i][0] + timedelta(hours=1))}'
                    }
                return available_slots

    return []


# print(get_available_slot(reserved_time_ranges_outside, predefined_range_outside, curr_time_outside))



