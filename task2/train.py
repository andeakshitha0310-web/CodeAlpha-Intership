import numpy as np
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

sequence_length = 100

notes = pickle.load(
    open("notes.pkl", "rb")
)

pitchnames = sorted(set(notes))

note_to_int = dict(
    (note, number)
    for number, note
    in enumerate(pitchnames)
)

network_input = []
network_output = []

for i in range(
        0,
        len(notes)-sequence_length):

    sequence_in = notes[
        i:i+sequence_length
    ]

    sequence_out = notes[
        i+sequence_length
    ]

    network_input.append(
        [note_to_int[char]
         for char in sequence_in]
    )

    network_output.append(
        note_to_int[sequence_out]
    )

n_patterns = len(network_input)

network_input = np.reshape(
    network_input,
    (n_patterns,
     sequence_length,
     1)
)

network_input = network_input / float(
    len(pitchnames)
)

model = Sequential()

model.add(
    LSTM(
        256,
        input_shape=(
            network_input.shape[1],
            network_input.shape[2]
        )
    )
)

model.add(Dropout(0.3))

model.add(Dense(
    len(pitchnames),
    activation='softmax'
))

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam'
)

model.fit(
    network_input,
    np.array(network_output),
    epochs=50,
    batch_size=64
)

model.save(
    "models/music_model.h5"
)

print("Model Saved")