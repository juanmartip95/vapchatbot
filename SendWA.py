from heyoo import WhatsApp
from ChatResponse import get_completion_from_messages
import os

# WA credentials
token=os.environ['WA_TOKEN']
# WA Business id
phoneNumberId='121302277626979'
# Initialize WA messages
WAMessage=WhatsApp(token,phoneNumberId)

def sendWA(tel,historial):
    historial.append(
        {'role':'system', 'content':'Extrae de la conversación anterior: \
        1) nombre del usuario 2) teléfono del usuario 3) dirección del usuario y 4) pedido.'}
        )
    resumen = get_completion_from_messages(historial, temperature=0)
    mensaje=f"""
    ⚠️🚨 Hemos recibido una solicitud de domicilio. 
    Resumen del pedido:
    {resumen}
    """

    WAMessage.send_message(mensaje,tel)
   