# ss-canton-crawler

Herramienta que recorre el sitio de la Secretaría de Salud de Cantón y descarga la información relevante.

## Requisitos

- Python 3.11+
- Dependencias: `requests`, `beautifulsoup4`

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -m ss_canton_crawler.runner --user USUARIO --password CLAVE [--base-url URL] [--output CARPETA]
```

Parámetros:

- `--user`: usuario para autenticación.
- `--password`: contraseña para autenticación.
- `--base-url`: URL base del sitio. Por defecto `https://ss-canton.example.com`.
- `--output`: directorio donde se almacenarán los archivos. Por defecto `output`.

La aplicación creará el directorio especificado y guardará tanto las páginas descargadas como la información procesada.
