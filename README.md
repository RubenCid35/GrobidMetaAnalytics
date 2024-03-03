# GrobidMetaAnalytics

En este repositorio se puede encontrar un script de Python para la lectura de publicaciones y la extracción de características
como número de figuras, links o el abstracto. En base a estas características, se genera un archivo PDF y varias figuras. Estos
archivos continen los siguientes puntos de análisis:

* Nube de Palabras de los abstractos de todas las publicaciones. Se puede encontrar en los archivos: `reporte.pdf` y `abstract-wordcloud.png`.
* Número de Figuras por Publicación. Se puede encontrar en los archivos: `reporte.pdf` y `num-figures.png`.
* Tabla con un listado de Links por Publicación. Solamente se puede encontrar únicamente en `reporte.pdf`.

En este [archivo](rationale.md) se puede comprender la ejecución del script. 

## Instalación y Requerimientos
Para poder usar este script, se puede hacer uso de manera local o mediante un conjunto de contenedores de Docker

### Instalación en local

Para poder ejecutar este script en local, se deben seguir una serie de pasos:
1. Instalar [Python](https://www.python.org/) preferiblemente la versión 3.11 o superior
2. (Opcional) Instalar Anaconda y crear una ambiente para instalar las librerías requeridas
3. Instalar **poetry** e instalar las librerias requeridas:
    ```bash
    poetry shell && poetry install
    ```
4. Instalar la librería del [cliente de Grobid de Python](https://github.com/kermitt2/grobid_client_python). Esta librería se debe instalar manualmente para poder funcionar.
    ```bash
    git clone https://github.com/kermitt2/grobid_client_python
    cd grobid_client_python
    python3 setup.py install
    ```

Posteriormente, se debe descargar e instalar [Grobid](https://github.com/kermitt2/grobid). Se recomienda usar el servicio de Docker para poder 
ejecutar Grobid. De esta forma, será más fácil de ejecutar y gestionar. Para descargar la imagen del contenedor se puede usar el comando siguiente

```bash
docker pull lfoppiano/grobid:0.8.0
```
## Ejecución

Como se mencionó previamente, se puede ejecutar de manera local o mediante Docker

### Ejecución en Local
Para poder ejecutar en local, se deberá:
1. Mover todos las publicaciones para la lectura del script a la carpeta `/papers/`.
2. Activar el servidor de Grobid. Si se está usando la versión de docker de Grobid, se usa el siguiente comando:
    ```bash
    docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
    ```
3. Tras esperar un rato a la inicialización del servidor ( se deben cargar todos los modelos), se puede usar el script de Python mediante: 
    ```bash
    python report_generator.py
    ```

Al acabar el programa, se generarán los archivos solicitados en la carpeta `/results/`

### Ejecución en Docker Compose
Para poder ejecutar en local, se deberá:
1. Mover todos las publicaciones para la lectura del script a la carpeta `/papers/`.
2. Crear carpeta `results`
3. Usar Docker Compose V2 para ejecutar imágenes del script
    ```bash
    docker compose build
    docker compose run report-generator
    ``` 

## Solución de Posibles Errores
Debido a que el script debe esperar a la inicialización del servicio de Grobid, pueden producirse errores y no leer
todas las publicaciones dadas al script. En estos casos, se recomienda volver a ejecutar de nuevo y esperar previamente
un par de segundos.
