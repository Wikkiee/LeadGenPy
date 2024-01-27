import pytest

from src.web_scrapper.scrapper import get_data_from_google_map



def test_get_data_from_google_map(list_of_required_data_from_google_map):
    result = get_data_from_google_map('Restaurants','Sweden')
    assert isinstance(result,dict)

    for key in list_of_required_data_from_google_map:
        assert key in result.keys()
    assert True
