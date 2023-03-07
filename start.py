import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

import requests
import json







# Initialize the speech recognizer and the text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to speak text aloud


def talk(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to listen for a voice command and convert it to text


def take_command():

    print('Listening...')
    with sr.Microphone() as source:
        voice = listener.listen(source)

    try:
        command = listener.recognize_google(voice)
    except Exception as e:
        command = "None"
    return command


# Define a function to execute a command based on the user's voice input


def run_assistant():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)  # Play the song on YouTube
    elif 'send email' in command:
        talk('To whom you want to send the email')
        to = input()
        talk('What is the subject of the email?')
        subject = input()
        talk('What should be the body of the email?')
        body = input()
        send_email(to, subject, body)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)  # Speak the current time
    elif 'search' in command:
        search_term = command.replace('search', '')
        pywhatkit.search(search_term)  # Search for the given term on Google
    elif 'who is' in command:
        person = command.replace('who is', '')
        # Get a summary of the person from Wikipedia
        info = wikipedia.summary(person, 2)
        talk(info)  # Speak the summary
    elif 'sleep' in command:
        talk('Goodbye!')
        exit()

    elif 'joke' in command:
        talk(pyjokes.get_joke())  # Tell a joke
    elif 'weather' in command:
        # Prompt the user to enter a location
        talk("Enter a location: ")
        location = take_command()
        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "units": "metric",
                "appid": "c639d72280802aeef447c0645a1bc07f"
            }

            # Make an HTTP GET request to the API
            response = requests.get(url, params=params)

            # Parse the JSON response and extract the relevant weather information
            data = response.json()

            print()
            print(data)
            print()
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            description = data["weather"][0]["description"]

            # Display the weather information in a user-friendly format
            talk(f"Temperature: {temperature}°C")
            talk(f"Humidity: {humidity}%")
            talk(f"Wind Speed: {wind_speed} m/s")
            talk(f"Description: {description}")
        except:
            # Speak an error message if the weather data is not available
            talk('Sorry, I could not find the weather information for ' + city_name)
    else:
        # Speak a message indicating that the command was not understood
        talk('Sorry, I did not understand your command.')


# Main code
if __name__ == '__main__':
    talk('Hi, I am your virtual assistant. How can I help you?')  # Greet the user
    while True:  # Run the assistant loop
        run_assistant()
