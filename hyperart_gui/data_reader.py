import copy
import logging
import xml.etree.ElementTree as ET

from PyQt6.QtGui import QColor

from .defs import DiagramType, ElemType, Orientation, ReflSymType
from .diagram import Diagram
from .element import (
    Circle,
    Element,
    EuclidPoly,
    EuclidPolyLine,
    HyperPoly,
    HyperPolyLine,
    Point,
)
from .irregular_pgon import IrregularPgon
from .permutation import Permutation
from .regular_pgon import RegularPgon

log = logging.getLogger(__name__)


class DataReader:
    """
    _summary_
    """

    def __init__(self):
        # m = diag;
        self.reflSymMap = {}
        self.reflSymMap["REFL_NONE"] = ReflSymType.REFL_NONE
        self.reflSymMap["REFL_EDGE_BISECTOR"] = ReflSymType.REFL_EDGE_BISECTOR
        self.reflSymMap["REFL_PGON_RADIUS"] = ReflSymType.REFL_PGON_RADIUS

        self.orienMap = {}
        self.orienMap["ROTATION"] = Orientation.ROTATION
        self.orienMap["REFLECTION"] = Orientation.REFLECTION

        self.elemTypeMap = {}
        self.elemTypeMap["EUCLID_POLYLINE"] = ElemType.EUCLID_POLYLINE
        self.elemTypeMap["EUCLID_POLY"] = ElemType.EUCLID_POLY
        self.elemTypeMap["CIRCLE"] = ElemType.CIRCLE
        self.elemTypeMap["HYPER_POLYLINE"] = ElemType.HYPER_POLYLINE
        self.elemTypeMap["HYPER_POLY"] = ElemType.HYPER_POLY

    # @staticmethod
    # https://docs.python.org/3/library/xml.etree.elementtree.html
    # def collectXML(fileName):
    #     parse_ast
    # /*!
    #     \fn DataReader::collectXML(const QString &fileName)
    #     Read all the XML file into string xmlText
    # */
    # bool DataReader::collectXML(const QString &fileName)
    # {
    #     QFile f(fileName);
    #     if (!f.open(QIODevice::ReadOnly))
    #         return false;

    #     QString line = "";
    #     Q3TextStream stream(&f);
    #     DataReader::xmlText = "";
    #     while (!stream.atEnd())
    #     {
    #         line = stream.readLine();
    #         DataReader::xmlText += line + "\n";
    #     }

    #     f.close();
    #     return True;
    # }

    @staticmethod
    def createDiagram(fileName: str) -> Diagram:
        """
        Create a diagram from a file.
        """
        try:
            with open(fileName, "r") as f:
                xmlText = f.read()
        except FileNotFoundError:
            log.error("File not found: " + fileName)
            return None
        # TODO: Can I load this directly from the file?
        root = ET.fromstring(xmlText)

        # determine document type from the root node
        # and delegate Diagram object creation to appropriate reader
        type = DataReader.dgramType(root)
        if DiagramType.REGULAR_PGON == type:
            reader = DataReaderRegularPgon()
            rp = reader.readXML(root)
            # dynamic_cast<RegularPgon *>(reader.readXML(doc));
            if rp:
                rp.init()
                return rp
        elif DiagramType.IRREGULAR_PGON == type:
            reader = DataReaderIrregularPgon()
            ip = reader.readXML(root)
            # dynamic_cast<IrregularPgon *>(reader.readXML(doc));
            if ip:
                ip.init()
                return ip

        return None

    @staticmethod
    def dgramType(doc) -> int:
        """
        _summary_

        Args:
            doc (_type_): _description_

        Returns:
            int: _description_

        TODO: Get this from the file.
        """
        designType = doc.get("type")
        if "REGULAR_PGON" == designType:
            return DiagramType.REGULAR_PGON
        elif "IRREGULAR_PGON" == designType:
            return DiagramType.IRREGULAR_PGON
        else:
            log.warning("DataReader::dgramType : Not a valid diagram type")
            return DiagramType.DIAGRAM

    def readMetadata(self, m: Diagram, root) -> bool:
        readOk = False
        for metadata in root:
            if metadata.tag == "colors":
                readOk = self.readColors(m, metadata)
        return readOk

    def readColors(self, m: Diagram, root):
        """_summary_

        Args:
            m (Diagram): _description_
            root (_type_): _description_

        Returns:
            _type_: _description_
        """
        readOk = False
        # TODO: Check this
        colorCount = int(root.attrib["count"])
        m.setNumColors(int(colorCount))
        colors = list(root)
        for i in range(colorCount):
            color = colors[i]
            readOk = self.readColor(m, color)
        return readOk

    def readColor(self, m: Diagram, root):
        """_summary_

        Args:
            m (Diagram): _description_
            root (_type_): _description_

        Returns:
            _type_: _description_
        """
        readOk = False
        cid = 0
        c = QColor("#000000")
        for attr in root:
            if attr.tag == "cid":
                text = attr.text
                if text:
                    cid = int(attr.text.strip())
                    readOk = True
            elif attr.tag == "hex":
                text = attr.text
                if text:
                    c = QColor("#" + attr.text.strip())
                    readOk = True
        # Check this with the cpp, this seems like it should be the way.
        if readOk:
            m.setColorMapValue(cid, c)
        return readOk

    def readPerm(self, m: Diagram, root, perm: Permutation):
        """_summary_

        Args:
            m (Diagram): _description_
            root (_type_): _description_
            perm (Permutation): _description_

        Returns:
            _type_: _description_
        """
        readOk = False
        permutations = list(root)
        for i in range(m.numColors()):
            if permutations[i].tag == "perm":
                text = permutations[i].text
                if text:
                    perm[i] = int(text.strip())
                    readOk = True
        return readOk

    def readAdjacency(self, m: Diagram, root) -> bool:
        readOk = False
        adjacencies = list(root)
        for i in range(m.p()):
            if adjacencies[i].tag == "entry":
                readOk = self.readEntry(m, adjacencies[i])
        return readOk

    def readEntry(self, m: Diagram, root) -> bool:
        readOk = False
        e = int(root.attrib["e"])
        for attr in root:
            if attr.tag == "orientation":
                text = attr.text
                if text:
                    orientation = text.strip()
                    m.edges[e].setOrientation(self.orienMap[orientation])
                    readOk = True
            elif attr.tag == "edge":
                text = attr.text
                if text:
                    edge = int(text.strip())
                    m.edges[e].setAdjEdgeId(edge)
                    readOk = True
            elif attr.tag == "color_perm":
                readOk = self.readPerm(m, attr, m.edges[e].colorPerm())
        return readOk

    def readElements(self, m: Diagram, root) -> bool:
        readOk = False
        for element in root:
            if element.tag == "elem":
                readOk = self.readElement(m, element)
        return readOk

    def readElement(self, m: Diagram, root) -> bool:
        """_summary_

        Args:
            m (Diagram): _description_
            root (_type_): _description_

        Returns:
            bool: _description_
        """
        readOk = False
        z_order = 1  # start with a low z-order
        type_attr = root.attrib["type"]
        if type_attr not in self.elemTypeMap:
            return False
        e = self.createElementObject(self.elemTypeMap[type_attr])
        if not e:
            return False
        for element in root:
            if element.tag == "fill":
                text = element.text
                if text:
                    is_filled = text.strip() == "true"
                    e.setFilled(is_filled)
                    readOk = True
            elif element.tag == "cid":
                text = element.text
                if text:
                    cid = int(text.strip())
                    e.setCid(cid)
                    readOk = True
            elif element.tag == "points":
                readOk = self.readPoints(element, e)
        e.setZOrder(z_order)
        z_order += 1
        m.fundPat().addElement(e)
        return readOk

    def readPoints(self, root, e: Element) -> bool:
        """_summary_

        Args:
            root (_type_): _description_
            e (Element): _description_

        Returns:
            bool: _description_
        """
        readOk = False
        for point in root:
            if point.tag == "pt":
                readOk, x, y = self.readPoint(point)
                pt = Point(x, y)
                pt.poincareToWeierstrass()
                e.addPoint(pt)
        return readOk

    def readPoint(self, root) -> bool:
        """_summary_

        Args:
            root (_type_): _description_

        Returns:
            bool: _description_
        """
        readOk, x, y = False, 0.0, 0.0
        for coord in root:
            if coord.tag == "x":
                text = coord.text.strip()
                if text:
                    x = float(coord.text)
                    readOk = True
            elif coord.tag == "y":
                text = coord.text.strip()
                if text:
                    y = float(coord.text)
                    readOk = True
        return readOk, x, y

    def createElementObject(self, type: ElemType) -> Element:
        """_summary_

        Args:
            type (ElemType): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            Element: _description_
        """
        if type == ElemType.EUCLID_POLYLINE:
            return EuclidPolyLine()
        elif type == ElemType.EUCLID_POLY:
            return EuclidPoly()
        elif type == ElemType.CIRCLE:
            return Circle()
        elif type == ElemType.HYPER_POLYLINE:
            return HyperPolyLine()
        elif type == ElemType.HYPER_POLY:
            return HyperPoly()
        elif type == ElemType.ELEMENT:
            # TODO: Implement this
            raise NotImplementedError


class DataReaderRegularPgon(DataReader):
    def __init__(self):
        super().__init__()

    def readXML(self, doc):
        """_summary_

        Args:
            doc (_type_): _description_

        Returns:
            _type_: _description_
        """
        m = RegularPgon()

        if doc.tag != "design":
            log.warning("Not a valid motif xml document.")
            return None

        # diagram = copy.deepcopy(m)  # do I really need this?
        for doc_element in doc:
            if doc_element.tag == "metadata":
                readOk = self.readMetadata(m, doc_element)
            elif doc_element.tag == "p":
                text = doc_element.text
                if text:
                    m.setP(int(text.strip()))
                readOk = True
            elif doc_element.tag == "q":
                text = doc_element.text
                if text:
                    m.setQ(int(text.strip()))
                readOk = True
            elif doc_element.tag == "fund_reg_edges":
                text = doc_element.text
                if text:
                    fund_reg_edges = int(text.strip())
                    m.setFundRegEdges(fund_reg_edges)
            elif doc_element.tag == "refl_sym_type":
                text = doc_element.text
                if text:
                    text = text.strip()
                    m.setReflSym(self.reflSymMap[text])
            elif doc_element.tag == "color_perm_rotn":
                readOk = self.readPerm(m, doc_element, m.rotnColorPerm())
            elif doc_element.tag == "color_perm_refl":  # Stop Here
                readOk = self.readPerm(m, doc_element, m.reflColorPerm())
            elif doc_element.tag == "adjacency":
                readOk = self.readAdjacency(m, doc_element)
            elif doc_element.tag == "elements":
                readOk = self.readElements(m, doc_element)
        if readOk:
            return m
        return 0


class DataReaderIrregularPgon(DataReader):
    def __init__(self):
        super().__init__()

    def readQlist(self, m, root):
        """_summary_

        Args:
            m (_type_): _description_
            root (_type_): _description_

        Returns:
            _type_: _description_
        """
        readOk = True

        root_elements = list(root)
        for i in range(m.p()):
            if root_elements[i].tag == "q":
                readOk, qval = self.readQ(root_elements[i])
                if readOk:
                    m.setQ(i, qval)
                else:
                    log.warning("Failed to read q value.")
        return readOk

    def readQ(self, root):
        """_summary_

        Args:
            root (_type_): _description_
            qval (_type_): _description_

        Returns:
            _type_: _description_
        """
        text = root.text
        if text:
            qval = int(text.strip())
            return True, qval
        return False, 0

    def readXML(self, doc):
        """_summary_

        Args:
            doc (_type_): _description_

        Returns:
            _type_: _description_
        """
        m = IrregularPgon()

        if doc.tag != "design":
            log.warning("Not a valid motif xml document.")
            return None

        # diagram = copy.deepcopy(m)  # do I really need this?
        for doc_element in doc:
            readOk = False
            if doc_element.tag == "metadata":
                readOk = self.readMetadata(m, doc_element)
            elif doc_element.tag == "p":
                text = doc_element.text
                if text:
                    m.setP(int(text.strip()))
                readOk = True
            elif doc_element.tag == "qlist":
                readOk = self.readQlist(m, doc_element)
            elif doc_element.tag == "adjacency":
                readOk = self.readAdjacency(m, doc_element)
            elif doc_element.tag == "elements":
                readOk = self.readElements(m, doc_element)
        if readOk:
            return m
        return 0
