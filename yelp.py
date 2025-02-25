"""
Module for retrieving and processing restaurant data using the Yelp API.

This module defines the Food class, which aggregates restaurant information for
specified locations and cuisines, processes review data, and filters results based on quality.
"""

import numpy as np
from yelpapi import YelpAPI
import pandas as pd
import json

api_key = 'L1nkRAIb3KHHHTNHKSwHTeLS778qy2cNhUbzUGDlr6VzO4Na_mgRfbQeLaRoNRgObFcQmzaRT-' \
          'izM6BsRFCRVroPg2FbB9J52QWC8vKFOzs3mpKts3_b6BTPWrfpY3Yx'
yelp_api = YelpAPI(api_key)


class Food:
    """
    Class to aggregate and filter restaurant data from Yelp based on locations and cuisines.

    This class queries the Yelp API for each location and cuisine type, aggregates review data,
    and filters restaurants based on review counts and ratings.
    """
    def __init__(self, locations, food_arr):
        """
        Initialize a Food instance.

        Args:
            locations (list): List of location names or identifiers.
            food_arr (list): List of cuisine types to search for.
        """
        self.cuisines = food_arr
        self.locations = locations
        # Build a dictionary mapping each location to its corresponding restaurant data.
        self.dict = self.create_trip_dict()

    def create_trip_dict(self):
        """
        Create a nested dictionary mapping locations to their respective cuisine restaurant data.

        Returns:
            dict: A dictionary where each key is a location and each value is another dictionary
                  mapping cuisine types to restaurant information.
        """
        return_dict = {}
        for l in self.locations:
            cuisines_dict = {}
            for type in self.cuisines:
                cuisines_dict[type] = self.return_restaurants(type, l)
            return_dict[l] = cuisines_dict
        return return_dict

    def return_restaurants(self, type, location):
        """
        Retrieve and process restaurant data for a specific cuisine type at a given location.

        This method queries the Yelp API, normalizes the response data into DataFrames,
        aggregates review data, filters out lower-rated restaurants, and creates a dictionary of results.

        Args:
            type (str): The cuisine type or search term.
            location (str): The location to search for restaurants.

        Returns:
            dict: A dictionary mapping restaurant names to their display addresses.
        """
        food_df = yelp_api.search_query(term=type, location=location)
        food_df = pd.json_normalize(food_df['businesses'])
        food_df_v1 = food_df[['id', 'alias', 'name', 'review_count', 'rating']]
        location_df_v2 = food_df[['id', 'location.display_address']]

        # Aggregate review data for each restaurant.
        new_df = self.aggregate_data(food_df_v1)
        # Filter the aggregated data based on review criteria.
        still_good_df = self.narrow_down(new_df)
        # Create and return a dictionary mapping restaurant names to addresses.
        restaurants_dict = self.create_dict(still_good_df, location_df_v2)
        return restaurants_dict

    def aggregate_data(self, df):
        """
        Aggregate review data for each restaurant by retrieving individual reviews from Yelp.

        For each restaurant in the DataFrame, this method fetches reviews and computes the mean rating.

        Args:
            df (DataFrame): DataFrame containing restaurant details.

        Returns:
            DataFrame: Merged DataFrame including a mean rating for each restaurant.
        """
        food_reviews_df = pd.DataFrame()
        # Iterate over each restaurant entry to fetch its reviews.
        for i in range(len(df)):
            reviews = yelp_api.reviews_query(df['id'][i])
            reviews_df = pd.json_normalize(reviews, record_path='reviews')
            reviews_df['location_id'] = df['id'][i]
            food_reviews_df = food_reviews_df._append(reviews_df)

        food_reviews_df = food_reviews_df[['id', 'rating', 'location_id']]
        # Group by restaurant and compute the average rating.
        latest_reviews_agg = food_reviews_df.groupby('location_id', as_index=False).agg({'rating': ['mean']})
        latest_reviews_agg.columns = ['location_id', 'mean_rating']
        # Merge the aggregated review data with the original restaurant details.
        finished_df = df.merge(latest_reviews_agg, left_on='id', right_on='location_id', how='left')
        return finished_df

    def narrow_down(self, df):
        """
        Filter restaurants to retain only those with consistently high ratings.

        This method flags restaurants where the mean rating is at least as high as the original rating,
        and then further filters by review count and a minimum rating threshold.

        Args:
            df (DataFrame): DataFrame containing aggregated restaurant review data.

        Returns:
            DataFrame: Filtered DataFrame of restaurants meeting quality criteria.
        """
        # Flag restaurants as 'yes' if the mean rating is greater than or equal to the original rating.
        df['still_good'] = np.where((df['mean_rating'] >= df['rating']), 'yes', 'no')
        # Filter for restaurants flagged as 'still good'.
        higher_review_df = df[df['still_good'] == 'yes']
        # Further filter to include only restaurants with a sufficient number of reviews and high ratings.
        higher_review_df = higher_review_df[higher_review_df['review_count'] > 100]
        higher_review_df = higher_review_df[higher_review_df['rating'] >= 4.0]
        return higher_review_df

    def create_dict(self, df, location_df):
        """
        Create a dictionary mapping restaurant names to their display addresses.

        Args:
            df (DataFrame): DataFrame of filtered restaurant data.
            location_df (DataFrame): DataFrame containing restaurant location information.

        Returns:
            dict: A dictionary with restaurant names as keys and their display addresses as values.
        """
        result_dict = {}
        for i in df.index:
            # Retrieve the display address for the restaurant.
            value = location_df.loc[location_df['id'] == df['id'][i]]
            result_dict[df['name'][i]] = value.iloc[0][1]
        return result_dict





