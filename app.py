import gradio as gr
from SysPrompt import sysPrompt
from index_query import get_docs
from ChatResponse import get_completion_from_messages, template
from SendWA import sendWA 
from List_Sharepoint import upload_list_sharepoint
import uuid
conversation_id = str(uuid.uuid4())
print(conversation_id)
def res(prompt, historial):
    # Preparar historial
    #historial=json.loads(historial)
    if historial==[]:
        historial=sysPrompt
    historial.append({'role':'user', 'content':prompt})
    
    # Respuesta 
    context=get_docs(prompt)
    historial.append({'role':'system', 'content':template(context)})
    try:
        respuesta = get_completion_from_messages(historial)
        historial.pop() # delete the context prompt
        historial.append({'role':'assistant', 'content': respuesta})
    except Exception as e:
        respuesta=str(e)

    return respuesta, historial

def respond(message, chat_history, history):
        #print(history,type(history))
        response= res(message,history)
        bot_message = response[0]
        chat_history.append((message, bot_message))
        upload_list_sharepoint(conversation_id,"Anonymous",message,bot_message)
        return "", chat_history,response[1]

def WA(history):
  sendWA("573138614084",history)
  return "✅ Validado"


css = """.gradio-container-3-47-1 button {font-size: 75%;}
.message.svelte-1pjfiar.svelte-1pjfiar.svelte-1pjfiar {padding: 5px;}
"""
botImg='https://lagunaai-my.sharepoint.com/personal/juanariasv_lagunaai_onmicrosoft_com/Documents/output-onlinepngtools.png'
with gr.Blocks(theme=gr.themes.Default(text_size="sm"),css=css) as demo:
    chatbot = gr.Chatbot(height=150,avatar_images=(None,botImg), bubble_full_width=False) #just to fit the notebook
    with gr.Row():
      with gr.Column():
        msg = gr.Textbox(show_label=False)
      with gr.Column():
        with gr.Row():
          btn = gr.Button("➤")
          btn.size="sm"
          clear = gr.ClearButton(components=[msg, chatbot], value="🔄")
          clear.size="sm"
        with gr.Row():
          upload=gr.UploadButton("Cargar comprobante 📁", file_types=["image"])
          upload.size="sm"
          pedido=gr.Button("Validar pedido")
          pedido.size="sm"
        with gr.Row():
          humano = gr.Button("Asesor humano 🙋‍♂️🙋‍♀️",link='https://wa.me')
          humano.size="sm"    
    history=gr.JSON(value="[]",visible=False)
    #history_button = gr.Button("Show history")
    btn.click(respond, inputs=[msg, chatbot,history], outputs=[msg, chatbot,history])
    msg.submit(respond, inputs=[msg, chatbot,history], outputs=[msg, chatbot,history]) #Press enter to submit
    pedido.click(WA, inputs=history,outputs=pedido)
    clear.click(lambda: None, None, chatbot, queue=False)
    #history_box = gr.Textbox()
    #history_button.click(history, inputs=chatbot, outputs=history_box)
gr.close_all()
demo.launch()
