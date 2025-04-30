import os
import librosa
import json
import numpy as np
from pathlib import Path

# --- CONFIGURATION ---
INPUT_BIDS_PATH = Path("F:/BIDS_Feature_Extractor/input")
DERIV_PATH = Path("F:/BIDS_Feature_Extractor/extractrd_feature")

# --- SCAN FOR AUDIO FILES ---
audio_files = list(INPUT_BIDS_PATH.rglob("*_audio.wav"))
print(f" Found {len(audio_files)} audio file(s)")

for wav_file in audio_files:
    parts = wav_file.parts

    # Extract subject and session info dynamically
    sub = next((p for p in parts if p.startswith("sub-")), None)
    ses = next((p for p in parts if p.startswith("ses-")), None)

    if not sub:
        print(f" Could not determine subject in: {wav_file}")
        continue

    # Prepare output directory
    out_dir = DERIV_PATH / sub
    if ses:
        out_dir = out_dir / ses
    out_dir = out_dir / "audioFeatures"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Load audio and extract features
        y, sr = librosa.load(wav_file, sr=None)

        features = {
            "Tempo": float(librosa.beat.tempo(y=y, sr=sr)[0]),
            "SpectralCentroid": float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))),
            "ZeroCrossingRate": float(np.mean(librosa.feature.zero_crossing_rate(y))),
            "MFCC": librosa.feature.mfcc(y=y, sr=sr).mean(axis=1).tolist(),
            "Software": "librosa",
            "Version": librosa.__version__
        }

        # Create output filename
        json_name = wav_file.stem.replace("_audio", "_audioFeatures.json")
        json_out = out_dir / json_name

        with open(json_out, "w") as f:
            json.dump(features, f, indent=4)

        print(f" Extracted features for: {wav_file.name}")

    except Exception as e:
        print(f" Failed to process {wav_file.name}: {e}")

