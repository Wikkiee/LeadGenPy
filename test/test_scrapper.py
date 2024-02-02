from web_scrapper.scrapper import scrape_data_from_google_map


def test_get_data_from_google_map(list_of_required_data_from_google_map):
    result = scrape_data_from_google_map('Restaurants', 'Sweden', 1)
    print(result)
    assert isinstance(result[0], dict)

    for key in list_of_required_data_from_google_map:
        assert key in result[0].keys()
    assert True
