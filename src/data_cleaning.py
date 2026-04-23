import pandas as pd

DATA_PATH = "data/Music_Info.csv"

def clean_data(data):
    """
    1. Removes duplicate rows based on "spotify_id" column
    2. Drops the "genre" and "spotify_id" column
    3. Fill missing values in the "tags" column with the string "no tags"
    4. Conver the "name","artist" and "tags" columns to lowercase

    Parameters :
    data (pd.DataFrame) : The input DataFrame containing the data to be cleaned.

    Returns:
    pd.DataFrame : The cleaned DataFrame
    """
    return (
        data
        .drop_duplicates(subset="spotify_id")
        .drop(columns=['genre','spotify_id'])
        .fillna({'tags':"no_tags"})
        .assign(
            name = lambda x : x["name"].str.lower(),
            artist = lambda x : x["artist"].str.lower(),
            tags = lambda x : x["tags"].str.lower()
        )
        .reset_index(drop=True)
    )


def data_for_content_filtering(data):
    """
    Cleans the input DataFrame by dropping specific columns.

    This function takes a DataFrame and removes the columns "track_id", "name",
    and "spotify_preview_url". It is intended to prepare the data for content based
    filtering by removing unnecessary features.

    Parameters:
    data (pandas.DataFrame): The input DataFrame containing songs information.

    Returns:
    pandas.DataFrame: A DataFrame with the specified columns removed.
    """

    return (
        data
        .drop(columns=["track_id","name","spotify_preview_url"])
    )



def main(data_path):
    """
    Main function to load, clean and save data.
    Parameters :
    data_path (str) : The file path to the raw data csv file.

    Returns :
    None
    """

    # load the data
    data = pd.read_csv(data_path)

    # perform data cleaning
    cleaned_data = clean_data(data)

    # saving clean data
    cleaned_data.to_csv("data/cleaned_music_data.csv",index=False)



if __name__ == "__main__":
    main(DATA_PATH)

