import os
import json
import shutil
import soundfile as sf
from pathlib import Path

# --- SETTINGS ---
INPUT_DIR = Path("audio_input")
OUTPUT_DIR = Path("bids_output")
SUBJECT_ID = "sub-01"
SESSION = "ses-01"
TASK = "audio"

# --- CREATE FOLDER STRUCTURE ---
bids_audio_path = OUTPUT_DIR / SUBJECT_ID / SESSION / "audio"
bids_audio_path.mkdir(parents=True, exist_ok=True)

# --- COPY DATASET DESCRIPTION ---
output_description = OUTPUT_DIR / "dataset_description.json"
shutil.copy("templates/dataset_description.json", output_description)

# --- CONVERT AUDIO FILES ---
for i, wav_file in enumerate(INPUT_DIR.glob("*.wav"), start=1):
    # Create BIDS filename
    run = f"run-{i:02}"
    bids_name = f"{SUBJECT_ID}_{SESSION}_task-{TASK}_{run}_audio"
    
    # Copy and rename .wav
    out_wav = bids_audio_path / f"{bids_name}.wav"
    shutil.copy(wav_file, out_wav)

    # Get audio metadata
    f = sf.SoundFile(wav_file)
    metadata = {
        "SamplingFrequency": f.samplerate,
        "AudioChannels": f.channels,
        "AudioDuration": round(len(f) / f.samplerate, 2),
        "RecordingType": "unknown",
        "MicrophoneModel": "unknown"
    }

    # Write sidecar JSON
    out_json = bids_audio_path / f"{bids_name}.json"
    with open(out_json, 'w') as jfile:
        json.dump(metadata, jfile, indent=4)

print(f" Converted {i} audio file(s) into BIDS format at: {OUTPUT_DIR}")
