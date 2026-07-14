from resemblyzer import VoiceEncoder,preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st 

#load voice recognition model
@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

#get voice embedding
def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio,sr = librosa.load(io.BytesIO(audio_bytes),sr=16000) #sr->sample rate
        wave = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wave)
        return embedding.tolist() #256 D unique number
    except Exception:
        st.error('Voice recog error')
        return None
    
#speaker identify
def identify_speaker(new_embedding,candidates_dict,threshold=0.65):
    if not new_embedding or not candidates_dict:
        return None,0.0
    best_sid = None
    best_score = -1
    
    for s_id,stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding,stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = s_id
        if best_score >= threshold:
            return best_sid,best_score
            
    return best_sid,best_score
    
#for bulk audio
def process_bulk_audio(audio_bytes,candidates_dict,threshold=0.65):
    try:
        encoder = load_voice_encoder()
        audio,sr = librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments = librosa.effects.split(audio,top_db=30)
        identify_results = {}
        
        for start,end in segments:
            if (end-start) < sr*0.5:
                continue
            segment_audio = audio[start-end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)
            
            s_id,score = identify_speaker(embedding,candidates_dict,threshold)
            
            if s_id not in identify_speaker or score > identify_results[s_id]:
                identify_results[s_id] = score
        return identify_results
    except Exception as e:
        st.error('Bulk process error')
        return {}
                 