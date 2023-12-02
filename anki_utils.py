import requests
import json

from gtts import gTTS
import os

def invoke(action, **params):

    request_json = json.dumps(
        {
            'action': action,
            'params': params,
            'version': 6
        }   
    )

    response = requests.post(
        'http://localhost:8765',
         data=request_json
        )
    
    # print(response.content)

    return json.loads(response.content)


def create_pronunciation_file(word_string):

    gTTS(word_string, lang="fr").save(f"C:/Users/User/AppData/Roaming/Anki2/User 1/{word_string}.mp3")

    return f"C:/Users/andre/AppData/Roaming/Anki2/User 1/collection.media/{word_string}.mp3"


# Function to add a new card to an existing deck
def add_card_to_deck(deck_name, front, back, pronunciation=False, sound_file_path=False):
    # HTML formatting for the Front field
    front_formatted = f"""
    <div style="font-family: Arial; font-size: 20px; text-align: center;">
        <strong>{front}</strong>
    </div>
    """
    if pronunciation and sound_file_path:
        # HTML formatting for the Back field
        back_formatted = f"""
        <div style="font-family: Arial; font-size: 18px;">
            <strong>Translation:</strong> {back}
            <hr>
            <strong>Pronunciation:</strong> <span style="color: blue;">{pronunciation}</span>
            <hr>
            <strong>Audio:</strong> [sound:{sound_file_path.split("/")[-1]}]
            <hr>
            <em style="font-size: 14px;">(noun  )</em>
        </div>
        """

    else:
        # HTML formatting for the Back field
        back_formatted = f"""
        <div style="font-family: Arial; font-size: 18px;">
            <strong>Translation:</strong> {back}
            <em style="font-size: 14px;">(noun)</em>
        </div>
        """
    
    invoke(
        'addNote',
        note={
            'deckName': deck_name,
            'modelName': 'Basic',
            'fields': {
                'Front': front_formatted,
                'Back': back_formatted
            }
        }
    )


# Find and delete a card by its front field
def delete_card_by_front(deck_name, front):
    note_ids = invoke('findNotes', query=f'deck:"{deck_name}" Front:"{front}"')
    if note_ids:
        invoke('deleteNotes', notes=note_ids)


def get_card_by_front(deck_name, front):
    # Find the note IDs that match the query
    response = invoke('findNotes', query=f'deck:"{deck_name}" Front:"{front}"')
    note_ids = response.get('result')
    print(note_ids)

    if not note_ids:
        return None

    # Fetch detailed information about these notes
    notes_info = invoke('notesInfo', notes=note_ids)
    return notes_info

# Function to get all cards in a specified deck
def get_all_cards_in_deck(deck_name):
    # Find the note IDs that match the query for the specific deck
    response = invoke('findNotes', query=f'deck:"{deck_name}"')
    note_ids = response.get('result')

    if not note_ids:
        return None

    # Fetch detailed information about these notes
    notes_info = invoke('notesInfo', notes=note_ids)
    return notes_info.get('result')
