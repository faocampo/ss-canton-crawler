from pathlib import Path

from extract_contenido import extract_text


def test_extract_sample():
    html = Path(__file__).with_name('data').joinpath('sample_contenido.html').read_text(encoding='utf-8')
    result = extract_text(html)
    expected = (
        "AVANCE EN SEGURIDAD VIAL | Habilitación de la Bicisenda en el Sector Deportivo\n\n"
        "Estimados vecinos:\n\n"
        "Nos complace informar que se ha alcanzado un hito importante: la finalización de la nueva bicisenda del Sector Deportivo, en el marco de las acciones previstas en el informe del CESVI.\n\n"
        "En el día de hoy se completaron las tareas de señalización y colocación de protecciones, tal como podrán observar en las fotografías adjuntas.\n\n"
        "Con esta intervención, la bicisenda queda oficialmente habilitada para su uso, reafirmando nuestro compromiso con la mejora continua de la seguridad vial dentro del barrio.\n\n"
        "Asimismo, como parte de estos trabajos, se procedió al cierre de uno de los accesos al estacionamiento, con el fin de reducir las demoras en la circulación por la vialidad principal durante los horarios de mayor tránsito.\n\n"
        "Agradecemos la colaboración de todos los vecinos y solicitamos hacer un uso responsable de este nuevo espacio, respetando las normas de circulación para preservar la seguridad y el cuidado de nuestra comunidad.\n\n"
        "Saludos cordiales,\nGerencia General"
    )
    combined = result.title + "\n\n" + result.text if result.title else result.text
    assert combined == expected
