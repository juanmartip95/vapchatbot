import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

# ChatGPT completion
llm_name = "gpt-3.5-turbo"

def get_completion_from_messages(messages, model=llm_name, temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        )
    return response.choices[0].message["content"]

def template(context):
  text=f"""Responde a la entrada previa del usuario, usando el siguiente \
  contexto delimitado con ###, si este contexto es útil para responder \
  al usuario, si no, entonces omítelo:
  ###{context}###
  Si hay información solicitada por el usuario que no está en el contexto, \
  dices que no la conoces, pero no inventas. Si el usuario está dando sus datos, \
  omite el contexto. El hilo de la conversación es la prioridad.
  """
  return text