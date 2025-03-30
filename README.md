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
- **API_ID & API_HASH** Podem ser pegos no site do telegram
- `https://my.telegram.org/auth`. Basta fazer login, e após a criação pegar os dados.
- `Phone_number`. Mude para seu número.
- `group_id`. Após a listagem, copie o id(grupo ou canal) e insira no input automático no código.
- `download_folder` Coloque o diretório onde será feito o download dos arquivos.
