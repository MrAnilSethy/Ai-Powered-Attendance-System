from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st
import traceback


# -------------------------
# Load Voice Encoder
# -------------------------
@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


# -------------------------
# Generate Voice Embedding
# -------------------------
def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        wav = preprocess_wav(audio)

        if len(wav) == 0:
            return None

        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:
        st.error(f"Voice Recognition Error:\n{e}")
        st.text(traceback.format_exc())
        return None


# -------------------------
# Speaker Identification
# -------------------------
def identify_speaker(new_embedding, candidates_dict, threshold=0.65):

    if new_embedding is None or len(candidates_dict) == 0:
        return None, 0.0

    new_embedding = np.asarray(new_embedding)

    best_sid = None
    best_score = -1.0

    for s_id, stored_embedding in candidates_dict.items():

        if stored_embedding is None or len(stored_embedding) == 0:
            continue

        stored_embedding = np.asarray(stored_embedding)

        similarity = np.dot(
            new_embedding,
            stored_embedding
        ) / (
            np.linalg.norm(new_embedding)
            * np.linalg.norm(stored_embedding)
        )

        if similarity > best_score:
            best_score = similarity
            best_sid = s_id

    if best_score >= threshold:
        return best_sid, float(best_score)

    return None, float(best_score)


# -------------------------
# Process Bulk Audio
# -------------------------
def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):

    try:

        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        # Detect speech regions
        segments = librosa.effects.split(
            audio,
            top_db=25
        )

        identify_results = {}

        for start, end in segments:

            # Ignore very short segments (<1 second)
            if (end - start) < sr:
                continue

            segment_audio = audio[start:end]

            wav = preprocess_wav(segment_audio)

            if len(wav) == 0:
                continue

            embedding = encoder.embed_utterance(wav)

            s_id, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            if s_id is None:
                continue

            if (
                s_id not in identify_results
                or score > identify_results[s_id]
            ):
                identify_results[s_id] = float(score)

        return identify_results

    except Exception as e:

        st.error(f"Bulk Process Error:\n{e}")
        st.text(traceback.format_exc())

        return {}