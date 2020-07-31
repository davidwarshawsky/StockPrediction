from main import ModelPredictorSP500
class TestReadInvalidSymbols(object):
    def test_len_symbols(self):
        expected_length = 2
        invalid_symbols = ModelPredictorSP500.read_invalid_symbols()
        actual_length = len(invalid_symbols)
        message = "Expected length: <{}> Actual length <{}>".format(expected_length,actual_length)
        assert actual_length == expected_length,message

    def test_type(self):
        expected_type = list
        actual_type   = type(ModelPredictorSP500.read_invalid_symbols())
        message = "Expected type <{}> Actual type <{}>".format(expected_type,actual_type)
        assert actual_type == expected_type,message

class TestReadSP500Symbols(object):
    def test_len_symbols(self):
        expected_length = 503
        symbols = ModelPredictorSP500.read_SP500_symbols()
        actual_length = len(symbols)
        message = "Expected length: <{}> Actual length <{}>".format(expected_length, actual_length)
        assert actual_length == expected_length, message

    def test_type(self):
        expected_type = list
        actual_type = type(ModelPredictorSP500.read_SP500_symbols())
        message = "Expected type <{}> Actual type <{}>".format(expected_type, actual_type)
        assert actual_type == expected_type, message
