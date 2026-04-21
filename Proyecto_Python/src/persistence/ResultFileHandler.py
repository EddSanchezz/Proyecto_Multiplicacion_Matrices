import os
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom.minidom import parseString
from pathlib import Path
from persistence import Results, ResultData


class ResultFileHandler:
    LANGUAGE = "python"
    DEFAULT_DIRECTORY = Path(__file__).resolve().parent.parent.parent.parent /"src/main/resources/results"
    FILE_NAME = f"{LANGUAGE}_results.xml"
    FILE_PATH = DEFAULT_DIRECTORY / FILE_NAME

    @staticmethod
    def save_results(results: Results):
        if not ResultFileHandler.DEFAULT_DIRECTORY.exists():
            os.makedirs(ResultFileHandler.DEFAULT_DIRECTORY)
        xml_str = results.to_xml()
        pretty_xml_as_string = parseString(xml_str).toprettyxml(indent="  ")
        with open(ResultFileHandler.FILE_PATH, 'w') as f:
            f.write(pretty_xml_as_string)

    @staticmethod
    def save_result(size, algorithm, execution_time, case="", rows=0, cols=0):
        """
        Guarda un resultado de ejecución de algoritmo.
        
        Args:
            size: Tamaño total (rows * cols) para compatibilidad hacia atrás
            algorithm: Nombre del algoritmo
            execution_time: Tiempo de ejecución en nanosegundos
            case: "Caso1" o "Caso2"
            rows: Filas de la matriz resultado
            cols: Columnas de la matriz resultado
        """
        results = ResultFileHandler.load_results()
        result_data = ResultData.ResultData(
            size=size, 
            algorithm=algorithm, 
            language=ResultFileHandler.LANGUAGE, 
            executionTime=execution_time,
            case=case,
            rows=rows,
            cols=cols
        )
        results.results.append(result_data)
        ResultFileHandler.save_results(results)

    @staticmethod
    def load_results(file_path=None):
        file_path = file_path if file_path else ResultFileHandler.FILE_PATH
        if not Path(file_path).exists():
            return Results.Results([])
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_data = f.read()
        return Results.Results.from_xml(xml_data)