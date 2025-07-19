import pytest
from src.query_quantity_calculator.parser import DatalogParser


class TestDatalogParser:
    def setup_method(self):
        self.parser = DatalogParser()

    def test_parse_single_relation(self):
        query = "R(a, b)"
        result = self.parser.parse_query(query)
        assert result == [("R", ["a", "b"])]

    def test_parse_multiple_relations(self):
        query = "R(a, b)\nS(b, c)\nT(a, c)"
        result = self.parser.parse_query(query)
        expected = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        assert result == expected

    def test_parse_relation_with_spaces(self):
        query = "R( a , b )"
        result = self.parser.parse_query(query)
        assert result == [("R", ["a", "b"])]

    def test_parse_relation_with_underscore(self):
        query = "R_1(a, b)"
        result = self.parser.parse_query(query)
        assert result == [("R_1", ["a", "b"])]

    def test_parse_relation_with_numbers(self):
        query = "R123(a, b)"
        result = self.parser.parse_query(query)
        assert result == [("R123", ["a", "b"])]

    def test_parse_large_arity(self):
        query = "R(a, b, c, d, e)"
        result = self.parser.parse_query(query)
        assert result == [("R", ["a", "b", "c", "d", "e"])]

    def test_parse_empty_lines(self):
        query = "R(a, b)\n\nS(b, c)\n\nT(a, c)"
        result = self.parser.parse_query(query)
        expected = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        assert result == expected

    def test_get_all_variables_simple(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"])]
        result = self.parser.get_all_variables(relations)
        assert result == {"a", "b", "c"}

    def test_get_all_variables_overlap(self):
        relations = [("R", ["a", "b"]), ("S", ["b", "c"]), ("T", ["a", "c"])]
        result = self.parser.get_all_variables(relations)
        assert result == {"a", "b", "c"}

    def test_parse_invalid_format_no_parentheses(self):
        query = "R a b"
        with pytest.raises(ValueError, match="Invalid relation format"):
            self.parser.parse_query(query)

    def test_parse_invalid_format_no_relation_name(self):
        query = "(a, b)"
        with pytest.raises(ValueError, match="Invalid relation format"):
            self.parser.parse_query(query)

    def test_parse_invalid_format_unclosed_parentheses(self):
        query = "R(a, b"
        with pytest.raises(ValueError, match="Invalid relation format"):
            self.parser.parse_query(query)

    def test_parse_invalid_format_empty_parentheses(self):
        query = "R()"
        with pytest.raises(ValueError, match="Invalid relation format"):
            self.parser.parse_query(query)

    def test_parse_invalid_relation_name_start_with_number(self):
        query = "123R(a, b)"
        with pytest.raises(ValueError, match="Invalid relation format"):
            self.parser.parse_query(query)

    def test_parse_invalid_relation_name_special_chars(self):
        query = "R@(a, b)"
        with pytest.raises(ValueError, match="Invalid relation format"):
            self.parser.parse_query(query)

    def test_parse_empty_query(self):
        query = ""
        result = self.parser.parse_query(query)
        assert result == []

    def test_parse_whitespace_only_query(self):
        query = "   \n  \n   "
        result = self.parser.parse_query(query)
        assert result == []

    def test_get_all_variables_empty_relations(self):
        relations = []
        result = self.parser.get_all_variables(relations)
        assert result == set()