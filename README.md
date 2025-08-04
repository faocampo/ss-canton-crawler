# ss-canton-crawler

Herramienta que recorre el sitio de la Simple Solutions del barrio indicado y descarga la información relevante.

## Requisitos

- Python 3.11+
- Dependencias: `requests`, `beautifulsoup4`

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -m ss_canton_crawler.runner --user USUARIO --password CLAVE \
    [--base-url URL] [--output CARPETA] [--sections ARCHIVO] \
    [--max-workers N] [--max-links M]
```

Parámetros:

- `--user`: usuario para autenticación.
- `--password`: contraseña para autenticación.
- `--base-url`: URL base del sitio. Por defecto `https://ss-canton.example.com`.
- `--output`: directorio donde se almacenarán los archivos. Por defecto `output`.
- `--sections`: archivo con las secciones iniciales a recorrer. Se aceptan rutas
  relativas y absolutas. Si se omite sólo se descarga la página principal.
- `--max-workers`: número de hilos de trabajo para el recorrido completo. Por defecto `4`.
- `--max-links`: límite opcional de enlaces visitados.

La aplicación creará el directorio especificado y guardará tanto las páginas descargadas como la información procesada.
