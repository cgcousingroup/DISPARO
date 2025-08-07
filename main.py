from telethon import TelegramClient, types
import asyncio

api_id = '18111898'  # substitua pelo seu API ID
api_hash = 'e3efed3fad547b52459ace4b80cf9832'  # substitua pelo seu API Hash
client = TelegramClient('session_name', api_id, api_hash)
channel_id = 1002861052320  # substitua pelo ID do seu canal de origem

async def send_message_to_my_groups():
    dialogs = await client.get_dialogs()  # Pega todos os diálogos (chats, grupos e canais)
    
    # Pega a última postagem do canal de origem
    last_post = await client.get_messages(channel_id, limit=1)  # Última postagem
    if not last_post:
        print(f"Não foi possível encontrar mensagens no canal {channel_id}")
        return

    # Pega o conteúdo da última postagem
    post_text = last_post[0].text
    
    for dialog in dialogs:
        try:
            # Verifica se é um grupo ou canal
            if dialog.is_group or dialog.is_channel:
                # Para canais, usamos PeerChannel e para grupos PeerChat
                if dialog.is_channel:
                    peer = types.PeerChannel(dialog.id)  # Para canais
                else:
                    peer = types.PeerChat(dialog.id)  # Para grupos

                # Tenta encaminhar a mensagem
                await client.forward_messages(peer, last_post[0].id, from_peer=channel_id)
                print(f"Mensagem encaminhada para: {dialog.title}")
        
        except Exception as e:
            # Ignora os erros e segue para o próximo
            pass

# Função para rodar o loop a cada 1 hora
async def periodic_task():
    while True:
        await send_message_to_my_groups()
        print("Esperando 1 hora até o próximo envio...")
        await asyncio.sleep(3600)  # Aguardar 1 hora (3600 segundos)

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(periodic_task())  # Inicia o loop
