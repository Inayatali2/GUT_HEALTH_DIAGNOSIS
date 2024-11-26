import streamlit as st
import pandas as pd
import joblib
import openai

# Load the trained model
model = joblib.load('gut_health_predictor.pkl')  # Ensure this file exists in your directory

# Set up OpenAI API (replace with your API key)
openai.api_key = "your_openai_api_key_here"

# Define expected features
expected_features = [
    "Fiber Intake (g/day)", "Sugar Intake (g/day)", "Protein Intake (g/day)",
    "Processed Food Consumption_Low", "Processed Food Consumption_Moderate", "Processed Food Consumption_High",
    "Bloating_None", "Bloating_Mild", "Bloating_Severe",
    "Abdominal Pain_None", "Abdominal Pain_Mild", "Abdominal Pain_Severe",
    "Diarrhea_None", "Diarrhea_Occasional", "Diarrhea_Frequent"
]

# Function to calculate gut health status and recommend medicines
def calculate_gut_health(symptoms):
    severity_score = 0
    if symptoms["Bloating"] == "Mild":
        severity_score += 1
    elif symptoms["Bloating"] == "Severe":
        severity_score += 2
    
    if symptoms["Abdominal Pain"] == "Mild":
        severity_score += 1
    elif symptoms["Abdominal Pain"] == "Severe":
        severity_score += 2
    
    if symptoms["Diarrhea"] == "Occasional":
        severity_score += 1
    elif symptoms["Diarrhea"] == "Frequent":
        severity_score += 2

    # Suggest medications based on severity
    if severity_score <= 2:
        return "Healthy", "Your gut health looks great! No medications required. Keep maintaining a healthy lifestyle.", []
    elif 3 <= severity_score <= 4:
        meds = ["Probiotics (e.g., Lactobacillus acidophilus)", "Antispasmodics (e.g., Dicyclomine)"]
        return "Moderate", "Your gut health is slightly off balance. Consider reviewing your diet and lifestyle.", meds
    else:
        meds = [
            "Probiotics (e.g., Bifidobacterium bifidum)",
            "Antidiarrheals (e.g., Loperamide for diarrhea)",
            "PPIs (e.g., Omeprazole for acid reflux)"
        ]
        return "Unhealthy", "Your gut health seems poor. It's recommended to seek professional advice.", meds

# App title and navigation
st.title("🌱 Gut Health Management Platform")
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Symptom Tracker", "Microbiome Testing", "Food Journal", "Treatment Plans", "Doctor Consultation", "Gamification"])

# Home Page
if page == "Home":
    st.subheader("Welcome to the Gut Health Management Platform")
    st.markdown("""
        This platform helps you manage your gut health effectively. Features include:
        - AI-Powered Symptom Tracking
        - Microbiome Testing Integration
        - Food and Lifestyle Journaling
        - Personalized Treatment Plans
        - Remote Doctor Consultation
        - Gamification for User Engagement
    """)

# Symptom Tracker
elif page == "Symptom Tracker":
    st.subheader("AI-Powered Symptom Tracker")
    symptom_data = {
        "Date": st.date_input("Date"),
        "Bloating": st.selectbox("Bloating", ["None", "Mild", "Severe"]),
        "Abdominal Pain": st.selectbox("Abdominal Pain", ["None", "Mild", "Severe"]),
        "Diarrhea": st.selectbox("Diarrhea", ["None", "Occasional", "Frequent"])
    }
    if st.button("Log Symptoms"):
        health_status, advice, medications = calculate_gut_health(symptom_data)
        st.success(f"Your Gut Health Status: {health_status}")
        st.info(advice)
        if medications:
            st.subheader("Recommended Medications:")
            for med in medications:
                st.markdown(f"- {med}")
        else:
            st.markdown("No medications required.")
        st.json(symptom_data)

# Microbiome Testing
elif page == "Microbiome Testing":
    st.subheader("Upload Your Microbiome Test Results")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file:
        microbiome_data = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.dataframe(microbiome_data)

# Food and Lifestyle Journal
elif page == "Food Journal":
    st.subheader("Food and Lifestyle Journal")
    journal_entry = {
        "Date": st.date_input("Date"),
        "Food Intake": st.text_area("Describe your meals for the day"),
        "Exercise (minutes)": st.slider("Exercise Duration", 0, 120, 30),
        "Stress Level (1-5)": st.slider("Stress Level", 1, 5, 3),
        "Sleep Hours": st.slider("Sleep Hours", 0, 12, 7)
    }
    if st.button("Log Journal Entry"):
        st.success("Journal entry logged successfully!")
        st.json(journal_entry)

# Personalized Treatment Plans
elif page == "Treatment Plans":
    st.subheader("Personalized Treatment Plans")
    user_query = st.text_area("Describe your current symptoms or issues:")
    if st.button("Get Treatment Plan"):
        if user_query.strip():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a healthcare assistant providing personalized treatment plans for gut health."},
                        {"role": "user", "content": user_query}
                    ]
                )
                st.success("Treatment Plan:")
                st.write(response['choices'][0]['message']['content'])
            except Exception:
                st.error("OpenAI API is unavailable. Here's some general advice:")
                st.markdown("""
                    - **Stay Hydrated:** Drink plenty of water.
                    - **Improve Diet:** Avoid processed foods and focus on whole foods.
                    - **Stress Management:** Practice relaxation techniques like yoga or meditation.
                """)

# Remote Doctor Consultation
elif page == "Doctor Consultation":
    st.subheader("Remote Doctor Consultation")
    consultation_query = st.text_area("Ask a question about your gut health:")
    if st.button("Ask Doctor"):
        if consultation_query.strip():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a virtual doctor specializing in gut health."},
                        {"role": "user", "content": consultation_query}
                    ]
                )
                st.success("Doctor's Response:")
                st.write(response['choices'][0]['message']['content'])
            except Exception:
                st.error("OpenAI API is unavailable. Here's some advice:")
                st.markdown("""
                    - **Monitor Symptoms:** Track any changes in your gut health.
                    - **See a Professional:** Seek medical help if symptoms persist.
                """)

# Gamification
elif page == "Gamification":
    st.subheader("Gamification")
    st.markdown("""
        Earn points for:
        - Logging symptoms
        - Logging food and lifestyle journals
        - Following treatment plans
    """)
    points = st.number_input("Enter points earned (example: 10)", min_value=0)
    if st.button("Redeem Points"):
        st.success(f"Points redeemed successfully! You have {points} points remaining.")
