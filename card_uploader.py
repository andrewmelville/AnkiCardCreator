""" This is a module that creates formatted anki cards from a csv file of words.
    An example csv file is in the data folder, called "word_translations.csv"
"""
import pandas as pd
import os
import sys
from anki_utils import add_card_to_deck, create_pronunciation_file


if __name__ == "__main__":

    print(
        f"Creating cards from {sys.argv[1]}"
        )
    print(
        f"and adding them to {sys.argv[2]}"
        )

    print("Loading in words...")
    cards_csv = pd.read_csv(
        f"data/{sys.argv[1]}",
        index_col=False
    )
    print("Words loaded!")

    # Shuffle the DataFrame rows
    cards_csv = cards_csv.sample(frac=1).reset_index(drop=True)
    for IDX, row in cards_csv.iterrows():

        # try:
            
        english_word = str(row["ENGLISH"])
        french_word = str(row["FRENCH"])
        pronunciation = str(row["PRONUNCIATION"])
        # print(pronunciation)
        word_type = str(row["WORD_TYPE"])
        extra_info = str(row["EXTRA_HELP"])


        print(f"Creating and adding {english_word.upper()} / {french_word.upper()} cards")

        print(f"Creating pronunciation sound file for {french_word.upper()}")

        sound_file_path = create_pronunciation_file(french_word)

        # Example usage
        add_card_to_deck(
            deck_name = sys.argv[2],
            front = english_word,
            back = french_word,
            pronunciation = pronunciation,
            sound_file_path = sound_file_path,
            )
        # Example usage
        add_card_to_deck(
            deck_name = sys.argv[2],
            front = french_word,
            back = english_word,
            pronunciation = pronunciation,
            sound_file_path=sound_file_path
            )
        # except:
            
        #     print(f"Failed to create card for {english_word.upper()} / {french_word.upper()} pair")
