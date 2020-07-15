from src.data.tradier import *
import pytest

class TestGetOptionExpirations(object):
    def test_normal_one(self):
        symbol = "AAPL"
        dates, strikes = get_option_expirations(symbol)
        date_len = len(dates)
        strikes_len = len(strikes)
        message = "{} Length of dates: {} Length of strikes: {}".format(symbol,date_len,strikes_len)
        assert date_len == strikes_len, message

    def test_normal_two(self):
        symbol = "GOOG"
        dates, strikes = get_option_expirations(symbol)
        date_len = len(dates)
        strikes_len = len(strikes)
        message = "{} Length of dates: {} Length of strikes: {}".format(symbol,date_len,strikes_len)
        assert date_len == strikes_len, message

    def test_bad_argument(self):
        symbol = "BADARGUMENT"
        with pytest.raises(ValueError) as exception_info:
            dates, strikes = get_option_expirations(symbol)
        expected_message = "Check symbol and api key, got symbol: <{}> and api_key <{}>".format(symbol,api_keys[0])
        message = "Actual exception message {}\nExpected exception message: '{}'".format(exception_info,expected_message)
        assert exception_info.match(expected_message), message

class TestGetStrikes(object):
    def test_normal_one(self):
        symbol = 'AMZN'
        dates, strikes = get_option_expirations(symbol)
        for date,strike in zip(dates,strikes):
            one_day_strikes = get_strikes(symbol, date)
            get_strikes_len = len(one_day_strikes)
            actual_strike_len = len(strike)
            message = "For {} on {} Expected length of the strikes: {} Actual length of the strikes {}".format(
                symbol,
                date,
                actual_strike_len,
                get_strikes_len
            )
            assert actual_strike_len == get_strikes_len, message

    def test_normal_two(self):
        symbol = 'A'
        dates, strikes = get_option_expirations(symbol)
        for date, strike in zip(dates, strikes):
            one_day_strikes = get_strikes(symbol, date)
            get_strikes_len = len(one_day_strikes)
            actual_strike_len = len(strike)
            message = "For {} on {} Expected length of the strikes: {} Actual length of the strikes {}".format(
                symbol,
                date,
                actual_strike_len,
                get_strikes_len
            )
            assert actual_strike_len == get_strikes_len, message

    def test_bad_symbol(self):
        symbol = 'BADARGUMENT'
        date = '2019-05-17'
        with pytest.raises(ValueError) as exception_info:
            strikes = get_strikes(symbol,date)
        expected_message = "Check symbol and date, got symbol: <{}> and date <{}>".format(symbol, date)
        message = "{} {} Message and Exception info do not match".format(symbol,date)
        assert exception_info.match(expected_message),message

    def test_bad_date(self):
        symbol = 'GOOG'
        # New Years Day
        date = '2020-01-01'
        with pytest.raises(ValueError) as exception_info:
            strikes = get_strikes(symbol, date)
        expected_message = "Check symbol and date, got symbol: <{}> and date <{}>".format(symbol, date)
        message = "{} {} Message and Exception info do not match".format(symbol, date)
        assert exception_info.match(expected_message), message

    def test_bad_symbol_bad_date(self):
        symbol = 'BADARGUMENT'
        # New Years Day
        date = '2020-01-01'
        with pytest.raises(ValueError) as exception_info:
            strikes = get_strikes(symbol, date)
        expected_message = "Check symbol and date, got symbol: <{}> and date <{}>".format(symbol, date)
        message = "{} {} Message and Exception info do not match".format(symbol, date)
        assert exception_info.match(expected_message), message


