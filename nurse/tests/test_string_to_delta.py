from nurse import string_to_delta
import datetime
import pytest 

def test_string_to_delta(mocker):

    # calculate the number of seconds in the day until now
    assert datetime.timedelta(days=-1, seconds=(24 - 2 ) * 3600) == string_to_delta("2 hour ago")
    assert datetime.timedelta(days=-1, seconds=24 * 3600 - 60) == string_to_delta("1 minute ago")
    assert datetime.timedelta(days=-1, seconds=(24 - 1) * 3600) == string_to_delta("60 minutes ago")

    # compare between equal times
    assert string_to_delta("60 minutes ago") == string_to_delta("1 hour ago")
    assert string_to_delta("24 hour ago") == string_to_delta("1 day ago")
    assert string_to_delta("48 hour ago") == string_to_delta("2 days ago")
    assert string_to_delta("1 hour ago") == string_to_delta("3600 seconds ago")

    with pytest.raises(Exception) as e_info:
        string_to_delta("1 huor ago")
    
    with pytest.raises(Exception) as e_info:
        string_to_delta("1 m ago")

    with pytest.raises(Exception) as e_info:
        string_to_delta("1m ago")

    assert string_to_delta("1 minute") == string_to_delta("1 minute ago")