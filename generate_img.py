import pyttsx3
import openai
import requests

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def generate_image(prompt, filename="generated_image.png"):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        img_data = requests.get(image_url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
        speak(f"Image generated and saved as {filename}")
    except Exception as e:
        print(f"Error generating image: {e}")
        speak("Sorry, I couldn't generate the image.")
