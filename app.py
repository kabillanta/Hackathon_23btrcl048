import streamlit as st
import speech_recognition as sr
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 130) 


agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    description="You are a voice AI agent. Keep responses short, clear, and conversational. Always respond very short and in a conversational tone.",
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=False,
)

def listen_to_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Could not request results, please check your internet connection."

def speak(text):
    engine.say(text)
    engine.runAndWait()

st.title("🎙️ Voice AI Assistant")
st.sidebar.title("📝 Conversation History")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("🎤 Speak"):
    command = listen_to_command()
    if command:
        st.write(f"**You:** {command}")
        if "bye" in command:
            response_text = "Goodbye!"
            speak(response_text)
            st.session_state.history.append(("You", command))
            st.session_state.history.append(("AI", response_text))
            st.write(f"**AI:** {response_text}")
        else:
            response = agent.run(command)
            speak(response.content)
            st.session_state.history.append(("You", command))
            st.session_state.history.append(("AI", response.content))
            st.write(f"**AI:** {response.content}")

for user, text in st.session_state.history:
    st.sidebar.write(f"**{user}:** {text}")
