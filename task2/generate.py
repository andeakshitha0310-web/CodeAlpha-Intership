import numpy as np
import pickle

from tensorflow.keras.models import load_model
from music21 import stream, note, chord

# Load trained model
model = load_model("models/music_model.h5")

# Load notes
notes = pickle.load(open("notes.pkl", "rb"))

# Get unique notes
pitchnames = sorted(set(notes))

print("Sample Notes:")
print(pitchnames[:20])

# Create mappings
note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

# Select random starting point
start = np.random.randint(0, len(notes) - 100)

pattern = [note_to_int[n] for n in notes[start:start + 100]]

prediction_output = []

# Generate 200 notes
for note_index in range(200):

    prediction_input = np.reshape(
        pattern,
        (1, len(pattern), 1)
    )

    prediction_input = prediction_input / float(len(pitchnames))

    prediction = model.predict(
        prediction_input,
        verbose=0
    )

    index = np.argmax(prediction)

    result = int_to_note[index]

    prediction_output.append(result)

    pattern.append(index)

    pattern = pattern[1:]

print("\nGenerated Notes:")
print(prediction_output)

# Convert generated notes to MIDI
output_notes = []

for pattern in prediction_output:

    try:

        if '.' in str(pattern):

            notes_in_chord = pattern.split('.')

            chord_notes = []

            for current_note in notes_in_chord:

                try:
                    new_note = note.Note(int(current_note))
                    chord_notes.append(new_note)
                except:
                    pass

            if len(chord_notes) > 0:
                new_chord = chord.Chord(chord_notes)
                output_notes.append(new_chord)

        else:

            try:
                new_note = note.Note(pattern)
            except:
                # fallback note
                new_note = note.Note("C4")

            output_notes.append(new_note)

    except:
        output_notes.append(note.Note("C4"))

# Create MIDI stream
midi_stream = stream.Stream(output_notes)

# Save MIDI file
midi_stream.write(
    'midi',
    fp='generated_music/output.mid'
)

print("\nMusic Generated Successfully!")
print("Saved at: generated_music/output.mid")