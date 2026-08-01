import streamlit as st
import pandas as pd
from datetime import datetime

from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio
from src.components.dialog_attendance_results import show_attendance_result


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    st.write(
        "🎤 Record classroom audio of students saying 'I am present'. "
        "The AI will identify the speakers automatically."
    )

    audio_data = st.audio_input("Record Classroom Audio")

    if st.button(
        "Analyze Audio",
        type="primary",
        width="stretch"
    ):

        # Check if audio is recorded
        if audio_data is None:
            st.warning("Please record audio first.")
            return

        with st.spinner("Processing classroom audio..."):

            # Get enrolled students
            enrolled_res = (
                supabase.table("subject_students")
                .select("*, students(*)")
                .eq("subject_id", selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this subject.")
                return

            # Build candidate voice embeddings
            candidates_dict = {
                int(node["students"]["student_id"]): node["students"]["voice_embedding"]
                for node in enrolled_students
                if node["students"].get("voice_embedding")
            }

            if not candidates_dict:
                st.error("No enrolled students have registered voice profiles.")
                return

            # Read recorded audio
            audio_bytes = audio_data.read()

            # Identify speakers
            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict,
                threshold=0.65
            )

            results = []
            attendance_to_log = []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            # Generate attendance
            for node in enrolled_students:

                student = node["students"]
                student_id = int(student["student_id"])

                score = detected_scores.get(student_id, 0.0)
                is_present = score >= 0.65

                results.append({
                    "Name": student["name"],
                    "ID": student_id,
                    "Source": f"Voice ({score:.2f})" if is_present else "_",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    "student_id": student_id,
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": is_present
                })

            # Save results
            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_to_log
            )

    # Show results
    results_data = st.session_state.get("voice_attendance_results")

    if results_data is not None:
        st.divider()
        df_results, logs = results_data
        show_attendance_result(df_results, logs)