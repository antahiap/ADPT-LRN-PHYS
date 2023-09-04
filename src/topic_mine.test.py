import unittest
from topic_mine import TopicMine

class TestExtractData(unittest.TestCase):
    def setUp(self):
        self.data_mine = TopicMine("Data Science")

    def test_parse_answer(self):
        # Test case 1
        input_str = "Temperature: 25 C\nPressure: 1 atm\nVolume: 10 L\n"
        expected_output = ["Temperature: 25 C", "Pressure: 1 Atm", "Volume: 10 L"]
        output = self.data_mine._parse_answer(input_str)
        self.assertEqual(output, expected_output)

    def test_parse_answer_comma(self):
        # Test case 2
        input_str = "Temperature: 25 C, Pressure: 1 atm, Volume: 10 L"
        expected_output = ["Temperature: 25 C", "Pressure: 1 Atm", "Volume: 10 L"]
        output = self.data_mine._parse_answer(input_str)
        self.assertEqual(output, expected_output)

    def test_parse_answer_non_alpha_char(self):
        # Test case 2
        input_str = "----------------,Example,----------"
        expected_output = ["Example"]
        output = self.data_mine._parse_answer(input_str)
        self.assertEqual(output, expected_output)

    def test_parse_answer_indexed_answer(self):
        # Test case 3
        input_str = "1. Example\n2. Example\n3. Example"
        expected_output = ["Example", "Example", "Example"]
        output = self.data_mine._parse_answer(input_str)
        self.assertEqual(output, expected_output)

    def test_parse_answer_dash_answer(self):
        # Test case 4
        input_str = "- Example\n- Example\n- Example"
        expected_output = ["Example", "Example", "Example"]
        output = self.data_mine._parse_answer(input_str)
        self.assertEqual(output, expected_output)

    def test_parse_answer_underscore_answer(self):
        # Test case 4
        input_str = "- Example_one\n- Example_two\n- Example_three"
        expected_output = ["Example One", "Example Two", "Example Three"]
        output = self.data_mine._parse_answer(input_str)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()