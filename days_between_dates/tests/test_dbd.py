from dbd import main

def test_main():
    assert main("2012-01-10", "2012-01-11") == 0
    assert main("2012-01-01", "2012-01-10") == 8
    assert main("1801-06-13", "1801-11-11") == 150
    assert main("2021-12-01", "2017-12-14") == 1447