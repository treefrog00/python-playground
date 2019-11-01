from journeys import is_journey_valid


def test_empty_command_list():
    input = """
    1 1 E
    
    1 1 E"""

    actual = run_test(input, True)


def test_simple_true_case_with_left():
    input = """
    1 1 E
    FLLFLL
    1 1 E"""

    actual = run_test(input, True)


def test_rotate_left_360():
    input = """
    1 1 E
    LLLL
    1 1 E"""

    actual = run_test(input, True)


def test_rotate_right_360():
    input = """
    1 1 E
    RRRR
    1 1 E"""

    actual = run_test(input, True)


def test_go_for_a_drive_left():
    input = """
    1 1 E
    LFLFLFLF
    1 1 E"""

    actual = run_test(input, True)


def test_go_for_a_drive_right():
    input = """
    1 1 E
    RFRFRFRF
    1 1 E"""

    actual = run_test(input, True)


def test_go_for_a_drive_left_and_right():
    input = """
    1 1 E
    LFRFLLFLFRRR
    1 1 E"""

    actual = run_test(input, True)


def test_simple_false_case():
    input = """
    1 1 E
    F
    1 1 E"""

    actual = run_test(input, False)


def run_test(input, expected_match):
    input_lines = [x.strip() for x in input.strip().split("\n")]
    actual_match, actual_end = is_journey_valid(input_lines)

    assert actual_match == expected_match, actual_end
