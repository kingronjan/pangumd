from pathlib import Path


def get_fixture_path(filename: str) -> str:
    fixture_path = Path(__file__).parent / 'fixtures' / filename
    return str(fixture_path)
