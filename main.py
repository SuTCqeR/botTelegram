from tkinter import dialog
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import os
import sys
import asyncio
from datetime import datetime
from telethon.tl.types import PeerChannel

CONFIG = {
    "api_id": "",
    "api_hash": "",
    "phone_number": "",
    "group_id": "",
    "download_folder": "",
    "max_files": None,  # Limite de arquivos para baixar (None = sem limite)
    "start_date": None,  # Data inicial (ex: datetime(2023, 1, 1)) ou None
    "media_types": ["photo", "video"],  # Tipos de mídia para baixar
}

#Cria pasta
os.makedirs(CONFIG["download_folder"], exist_ok=True)

client = TelegramClient("user_session", CONFIG["api_id"], CONFIG["api_hash"])

#Conecta ao telegram do usuário
async def conectar():
        # Conectar e fazer login com número de telefone
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(CONFIG["phone_number"])
            code = input("Digite o código recebido: ")
            await client.sign_in(CONFIG["phone_number"], code)

        print(f"Conectado com sucesso ao Telegram como {CONFIG['phone_number']}")
#Lista Grupos e Channels
async def listarGC():
        #Opção Listar Grupos e Canais
        print("Listar -> Grupos[1] - Canais[2] ")
        opcao = int(input("Opção: "))

        #Lista Grupos
        dialogs = await client.get_dialogs()

        if opcao not in [1,2]:
            print("Comando Não encontrado... Saindo!")
            sys.exit()
         # Obter informações do grupo
        for chat in dialogs:
            if opcao == 1 and chat.is_group:
                print(f"Nome: {chat.title} | Username: {chat.id} | Tipo: Grupo:{ chat.is_group }")
            if opcao == 2 and chat.is_channel:
                print(f"Nome: {chat.title} | ID: {chat.id} | Tipo: Canal:{ chat.is_channel }")
            


async def download():
    try:    #Faz Download
        baixar = int(input("Cole aqui seu ID ou usernameGroup:"))
        CONFIG["group_id"] = baixar
        group = await client.get_entity(PeerChannel( CONFIG["group_id"]))
        print(f"Baixando mídias do grupo: {group.title}")
        # Contadores
        downloaded_count = 0
        skipped_count = 0
        # Iterar pelas mensagens
        async for message in client.iter_messages(group, limit=CONFIG["max_files"]):
            # Filtrar por data, se configurado
            if CONFIG["start_date"] and message.date < CONFIG["start_date"]:
                skipped_count += 1
                continue
            if message.media:
                # Verificar tipo de mídia pela classe do objeto message.media
                media_type = None
                if isinstance(message.media, MessageMediaPhoto):  # Foto
                    media_type = "photo"
                elif isinstance(message.media, MessageMediaDocument):  # Documento (vídeo, áudio, outros)
                    if hasattr(message.media.document, "mime_type"):
                        if message.media.document.mime_type.startswith("video/"):
                            media_type = "video"
                        elif message.media.document.mime_type.startswith("audio/"):
                            media_type = "audio"
                        else:
                            media_type = "document"
                    else:
                        media_type = "document"
                else:
                    skipped_count += 1
                    continue
                
                # Verificar se o tipo de mídia está na lista permitida
                if media_type in CONFIG["media_types"]:
                    try:
                        # Gerar nome de arquivo único com timestamp
                        timestamp = message.date.strftime("%Y%m%d_%H%M%S")
                        file_ext = ".unknown"
                        if media_type == "photo":
                            file_ext = ".jpg"
                        elif media_type == "video":
                            file_ext = ".mp4"
                        elif media_type == "audio":
                            file_ext = ".mp3"
                        elif media_type == "document":
                            file_ext = ".bin"  # Pode ajustar conforme a extensão real do documento
                        file_name = f"media_{timestamp}_{message.id}{file_ext}"
                        file_path = os.path.join(CONFIG["download_folder"], file_name)
                        # Baixar a mídia
                        await client.download_media(message.media, file_path)
                        downloaded_count += 1
                        print(f"[{downloaded_count}] Baixado: {file_path}")
                    except FloodWaitError as e:
                        print(f"Limite de requisições atingido. Aguardando {e.seconds} segundos...")
                        await asyncio.sleep(e.seconds)
                    except Exception as e:
                        print(f"Erro ao baixar mídia da mensagem {message.id}: {str(e)}")
                else:
                    skipped_count += 1
            else:
                skipped_count += 1
        print(f"\nResumo: {downloaded_count} arquivos baixados, {skipped_count} mensagens ignoradas")
        print(CONFIG["group_id"])
    except SessionPasswordNeededError:
        print("Senha de autenticação necessária.")
    except FloodWaitError as e:
        print(f"Limite de requisições atingido. Aguardando {e.seconds} segundos...")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    finally:
        await client.disconnect()
        print("Desconectado do Telegram")


async def main():
    await conectar()
    await listarGC()
    await download()


if __name__ == "__main__":
    asyncio.run(main())