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
    # unnecessary with xml.etree.ElementTree
    # def collectXML(fileName):

    @staticmethod
    def createDiagram(fileName: str) -> Diagram:
        """
        Create a diagram from a file.
        """
        try:
            with open(fileName, "r") as f:
                xmlText = f.read()
        except FileNotFoundError:
            log.error("File not found: %s", fileName)
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
    def dgramType(doc) -> DiagramType:
        """
        Get the diagram type from the root node.

        Args:
            doc (xml.etree.ElementTree): root node of the xml document

        Returns:
            DiagramType: The type of diagram we are dealing with.
        """
        designType = doc.get("type")
        if "REGULAR_PGON" == designType:
            return DiagramType.REGULAR_PGON
        elif "IRREGULAR_PGON" == designType:
            return DiagramType.IRREGULAR_PGON
        else:
            log.warning("DataReader::dgramType : Not a valid diagram type")
            return DiagramType.DIAGRAM

    def readMetadata(self, m: Diagram, root: ET) -> bool:
        """Read the metadata from the xml tree.

        Args:
            m (Diagram): The diagram to read the metadata into.
            root (xml.etree.ElementTree): XML tree root node.

        Returns:
            bool: Success or failure.
        """
        readOk = False
        for metadata in root:
            if metadata.tag == "colors":
                readOk = self.readColors(m, metadata)
        return readOk

    def readColors(self, m: Diagram, root) -> bool:
        """Read color information from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the colors into.
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool: Success or failure.
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

    def readColor(self, m: Diagram, root) -> bool:
        """Read specific color information from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the color into.
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool: success or failure.
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

    def readPerm(self, m: Diagram, root: ET, perm: Permutation) -> bool:
        """Read permutation information from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the color into.
            root (xml.etree.ElementTree): xml tree root node.
            perm (Permutation): Initialized Permutaiton object.

        Returns:
            bool: Success or failure.
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

    def readAdjacency(self, m: Diagram, root: ET) -> bool:
        """Read adjacency information from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the color into.
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool: Success or failure.
        """
        readOk = False
        adjacencies = list(root)
        for i in range(m.p()):
            if adjacencies[i].tag == "entry":
                readOk = self.readEntry(m, adjacencies[i])
        return readOk

    def readEntry(self, m: Diagram, root: ET) -> bool:
        """Read Entry information from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the color into.
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool: Success or failure.
        """
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

    def readElements(self, m: Diagram, root: ET) -> bool:
        """Read elements from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the color into.
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool: success or failure.
        """
        readOk = False
        for element in root:
            if element.tag == "elem":
                readOk = self.readElement(m, element)
        return readOk

    def readElement(self, m: Diagram, root: ET) -> bool:
        """Read element from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the color into.
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool: Success or failure.
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

    def readPoints(self, root: ET, e: Element) -> bool:
        """Read points from the xml tree into element.

        Args:
            root (xml.etree.ElementTree): xml tree root node.
            e (Element): Element to read the points into.

        Returns:
            bool: Success or failure.
        """
        readOk = False
        for point in root:
            if point.tag == "pt":
                readOk, x, y = self.readPoint(point)
                pt = Point(x, y)
                pt.poincareToWeierstrass()
                e.addPoint(pt)
        return readOk

    def readPoint(self, root: ET) -> bool:
        """Read point from the xml tree into element.

        Args:
            root (xml.etree.ElementTree): XML tree root node.

        Returns:
            bool: Success or failure.
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
        """Create an element object of the given type.

        Args:
            type (ElemType): Initialized element type.

        Raises:
            NotImplementedError: Error when Type is not implemented.

        Returns:
            Element: Initialized element object.
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
    """Data reader for regular polygons."""

    def __init__(self):
        super().__init__()

    def readXML(self, doc) -> Diagram:
        """Read the xml tree into diagram.

        Args:
            doc (xml.etree.ElementTree): Root of the xml tree.

        Returns:
            Diagram: Rendered diagram or None
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
        return None


class DataReaderIrregularPgon(DataReader):
    """Data reader for irregular polygons."""

    def __init__(self):
        super().__init__()

    def readQlist(self, m, root: ET) -> bool:
        """Read qlist from the xml tree into diagram.

        Args:
            m (Diagram): Diagram to read the color into.
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool: Success or failure.
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

    def readQ(self, root: ET):
        """Read q from the xml tree into diagram.

        Args:
            root (xml.etree.ElementTree): xml tree root node.

        Returns:
            bool, int: Success or failure, q value.
        """
        text = root.text
        if text:
            qval = int(text.strip())
            return True, qval
        return False, 0

    def readXML(self, doc):
        """Read the xml tree into diagram.

        Args:
            doc (xml.etree.ElementTree): xml tree root node.

        Returns:
            Diagram: Diagram or None
        """
        m = IrregularPgon()

        if doc.tag != "design":
            log.warning("Not a valid motif xml document.")
            return None

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
