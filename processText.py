import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def filter_and_validate_texts(texts):
    prompt = (
        "Tengo una lista de textos detectados en una imagen, algunos pueden ser nombres de videojuegos "
        "y otros pueden no tener relación. Filtra y devuelve solo los nombres válidos de videojuegos:\n"
        + "\n".join(texts)
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    valid_texts = response['choices'][0]['message']['content']
    return valid_texts.split("\n")

def process_texts(texts):
    valid_texts = filter_and_validate_texts(texts)

    prompt = (
        "Tengo esta lista de nombres de videojuegos:\n"
        + "\n".join(valid_texts) +
        "\nPor favor, organiza esta información en un formato JSON donde cada objeto incluya el título, "
        "la plataforma (si se puede incluir) y el año de lanzamiento (si se conoce)."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response['choices'][0]['message']['content']
