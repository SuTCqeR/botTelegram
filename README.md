## BOT de Dowload Telegram usando Thelethon
## Única alteração a ser feita:

```
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
```
- **API_ID & API_HASH** Podem ser pego no site do telegram
- `https://my.telegram.org/auth`. Basta fazer login, e após a criação pegar os dados
