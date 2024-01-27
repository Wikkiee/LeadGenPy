import pytest


@pytest.fixture()
def list_of_required_data_from_google_map():
    return ['business_name', 'business_category', 'business_email', 'business_name', 'google_map_url', 'mobile_number',
            'personalized_email_content', 'personalized_email_subject', 'ratings', 'review_counts', 'status',
            'top_review_1', 'top_review_2', 'top_review_3', 'website_url']
