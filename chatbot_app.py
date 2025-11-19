import streamlit as st
import pickle
import numpy as np

# -------------- SAFE SESSION STATE --------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------- LOAD MODEL SAFELY --------------
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# -------------- UI DESIGN --------------
st.set_page_config(page_title="EV Range Chatbot", layout="wide")

st.markdown("""
<style>
.user-bubble {
    background-color: #1e3a8a;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0px;
    width: fit-content;
    max-width: 70%;
}

.bot-bubble {
    background-color: #e5e7eb;
    color: #111827;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0px;
    width: fit-content;
    max-width: 70%;
}

</style>
""", unsafe_allow_html=True)

st.title("⚡ EV Range Prediction Chatbot")
st.write("Ask me anything about Electric Vehicles or request a range prediction!")

# -------------- DISPLAY CHAT --------------
def display_message(role, text):
    if role == "user":
        st.markdown(f"<div class='user-bubble'>You: {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>Bot: {text}</div>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if isinstance(msg, dict) and "role" in msg and "text" in msg:
        display_message(msg["role"], msg["text"])

# -------------- BOT INTELLIGENCE --------------
def bot_reply(user_text):
    user_text_lower = user_text.lower()

    # Predict command
    if any(word in user_text_lower for word in ["predict", "range"]):
        return "Sure! Please enter values in the box below:\nBattery, Torque, Efficiency"

    # Basic EV questions
    if "ev" in user_text_lower and "what" in user_text_lower:
        return "An EV (Electric Vehicle) uses electricity stored in batteries instead of fuel."

    if "battery" in user_text_lower:
        return "Battery capacity (kWh) tells how much energy the EV can store."

    if "torque" in user_text_lower:
        return "Torque (Nm) represents how powerful the EV motor is."

    if "efficiency" in user_text_lower:
        return "Efficiency (Wh/km) tells how many watt-hours are consumed per km."

    # Default
    return "I'm here to help! Ask me about EVs or say **predict range for battery torque efficiency**."

# -------------- USER INPUT FIELD --------------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    bot_response = bot_reply(user_input)
    st.session_state.messages.append({"role": "bot", "text": bot_response})
    st.rerun()

# -------------- RANGE PREDICTION BOX --------------
st.subheader("🔋 Enter Values for Range Prediction")

battery = st.number_input("Battery Capacity (kWh):", min_value=10.0, max_value=200.0, step=1.0)
torque = st.number_input("Torque (Nm):", min_value=50.0, max_value=2000.0, step=10.0)
efficiency = st.number_input("Efficiency (Wh/km):", min_value=50.0, max_value=300.0, step=1.0)

if st.button("Predict Range"):
    user_data = np.array([[battery, torque, efficiency]])
    prediction = model.predict(user_data)[0]
    st.success(f"🚗 Estimated Driving Range: **{prediction:.2f} km**")

    # Save in chat
    st.session_state.messages.append(
        {"role": "bot", "text": f"Your predicted EV range is **{prediction:.2f} km**"}
    )
    st.rerun()

