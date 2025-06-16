import tempfile
import pytest
from datetime import datetime

from utils.log_parser import LogParser


def test_parse_valid_log():
    log_content = "12:00:00,job 001,START,123\n12:05:00,job 001,END,123\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(log_content)
        f.flush()
        result = LogParser.parse(f.name)

    assert "123" in result
    assert "START" in result["123"]
    assert result["123"]["START"] == datetime.strptime("12:00:00", "%H:%M:%S")


def test_parse_malformed_log():
    log_content = "not-a-time,job,START,123\n12:00:00,job,START,124\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(log_content)
        f.flush()
        result = LogParser.parse(f.name)

    assert "124" in result
    assert "START" in result["124"]

def test_missing_end_entry():
    log_content = "12:00:00,job A,START,001\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(log_content)
        f.flush()
        result = LogParser.parse(f.name)

    assert "001" in result
    assert "START" in result["001"]
    assert "END" not in result["001"]\

def test_duplicate_entries():
    log_content = (
        "12:00:00,job B,START,002\n"
        "12:01:00,job B,START,002\n"
        "12:05:00,job B,END,002\n"
    )
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(log_content)
        f.flush()
        result = LogParser.parse(f.name)

    assert "002" in result
    assert result["002"]["START"] == datetime.strptime("12:01:00", "%H:%M:%S")

def test_empty_lines():
    log_content = "\n12:00:00,job X,START,321\n\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(log_content)
        f.flush()
        result = LogParser.parse(f.name)

    assert "321" in result
    assert "START" in result["321"]

def test_extra_columns():
    log_content = "12:00:00,job Y,START,999,extra_column\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(log_content)
        f.flush()
        result = LogParser.parse(f.name)

    assert "999" not in result  # Line should be skipped

def test_wrong_time_format():
    log_content = "12-00-00,job Z,START,888\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(log_content)
        f.flush()
        result = LogParser.parse(f.name)

    assert "888" not in result  # Should be skipped
