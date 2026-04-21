import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ResultData:
    size: int = field(default=0)
    algorithm: str = field(default="")
    language: str = field(default="")
    executionTime: int = field(default=0)
    case: str = field(default="")  # "Caso1" o "Caso2"
    rows: int = field(default=0)   # Filas de la matriz resultado
    cols: int = field(default=0)   # Columnas de la matriz resultado

    def to_xml(self):
        root = ET.Element("ResultData")
        ET.SubElement(root, "size").text = str(self.size)
        ET.SubElement(root, "algorithm").text = self.algorithm
        ET.SubElement(root, "language").text = self.language
        ET.SubElement(root, "executionTime").text = str(self.executionTime)
        ET.SubElement(root, "case").text = self.case
        ET.SubElement(root, "rows").text = str(self.rows)
        ET.SubElement(root, "cols").text = str(self.cols)
        return ET.tostring(root, encoding='unicode')

    @staticmethod
    def from_xml(xml_data):
        tree = ET.fromstring(xml_data)
        return ResultData(
            size=int(tree.find('size').text),
            algorithm=tree.find('algorithm').text,
            language=tree.find('language').text,
            executionTime=int(tree.find('executionTime').text),
            case=tree.find('case').text if tree.find('case') is not None else "",
            rows=int(tree.find('rows').text) if tree.find('rows') is not None else 0,
            cols=int(tree.find('cols').text) if tree.find('cols') is not None else 0
        )
    
    def to_xml_element(self):
        root = ET.Element("result")
        ET.SubElement(root, "size").text = str(self.size)
        ET.SubElement(root, "algorithm").text = self.algorithm
        ET.SubElement(root, "language").text = self.language
        ET.SubElement(root, "executionTime").text = str(self.executionTime)
        ET.SubElement(root, "case").text = self.case
        ET.SubElement(root, "rows").text = str(self.rows)
        ET.SubElement(root, "cols").text = str(self.cols)
        return root

    @staticmethod
    def from_xml_element(elem):
        return ResultData(
            size=int(elem.find('size').text),
            algorithm=elem.find('algorithm').text,
            language=elem.find('language').text,
            executionTime=int(elem.find('executionTime').text),
            case=elem.find('case').text if elem.find('case') is not None else "",
            rows=int(elem.find('rows').text) if elem.find('rows') is not None else 0,
            cols=int(elem.find('cols').text) if elem.find('cols') is not None else 0
        )
