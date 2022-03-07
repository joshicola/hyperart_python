import logging
import xml.etree.ElementTree as ET

from black import parse_ast

from .defs import (
    CIRCLE,
    DIAGRAM,
    EUCLID_POLY,
    EUCLID_POLYLINE,
    HYPER_POLY,
    HYPER_POLYLINE,
    IRREGULAR_PGON,
    REFL_EDGE_BISECTOR,
    REFL_NONE,
    REFL_PGON_RADIUS,
    REFLECTION,
    REGULAR_PGON,
    ROTATION,
)
from .diagram import Diagram

log = logging.getLogger(__name__)


class DataReader:
    """
    _summary_
    """

    def __init__(self):
        # m = diag;
        self.reflSymMap = {}
        self.reflSymMap["REFL_NONE"] = REFL_NONE
        self.reflSymMap["REFL_EDGE_BISECTOR"] = REFL_EDGE_BISECTOR
        self.reflSymMap["REFL_PGON_RADIUS"] = REFL_PGON_RADIUS

        self.orienMap = {}
        self.orienMap["ROTATION"] = ROTATION
        self.orienMap["REFLECTION"] = REFLECTION

        self.elemTypeMap = {}
        self.elemTypeMap["EUCLID_POLYLINE"] = EUCLID_POLYLINE
        self.elemTypeMap["EUCLID_POLY"] = EUCLID_POLY
        self.elemTypeMap["CIRCLE"] = CIRCLE
        self.elemTypeMap["HYPER_POLYLINE"] = HYPER_POLYLINE
        self.elemTypeMap["HYPER_POLY"] = HYPER_POLY

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
    #     return true;
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
        root = ET.fromstring(xmlText)

        # determine document type from the root node
        # and delegate Diagram object creation to appropriate reader
        type = DataReader.dgramType(root)
        if REGULAR_PGON == type:
            reader = DataReaderRegularPgon()
            rp = reader.readXML(root)
            # dynamic_cast<RegularPgon *>(reader.readXML(doc));
            if rp:
                rp.init()
                return rp
        elif IRREGULAR_PGON == type:
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
        root = doc.documentElement()
        designType = root.attributeNode("type").value()
        if "REGULAR_PGON" == designType:
            return REGULAR_PGON
        elif "IRREGULAR_PGON" == designType:
            return IRREGULAR_PGON
        else:
            log.warning("DataReader::dgramType : Not a valid diagram type")
            return DIAGRAM

    def readMetadata(self, m: Diagram, root) -> bool:
        pass

    # bool DataReader::readMetadata(self, m:Diagram, root)
    # {
    #     bool readOk = false;
    #     QDomNode node = root.firstChild();
    #     while (!node.isNull())
    #     {
    #         if (node.isElement())
    #         {
    #             if (node.nodeName() == "colors")
    #             {
    #                 readOk = false;
    #                 readOk = readColors(m, node);
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readColors(self, m: Diagram, root):
        pass

    # bool DataReader::readColors(self, m:Diagram, root)
    # {
    #     bool readOk = false;
    #     QDomAttr colorCount = root.toElement().attributeNode("count");
    #     m->setNumColors(colorCount.value().toInt());
    #     QDomNode node = root.firstChild();
    #     for (int i = 0; i < m->numColors(); i++)
    #     {
    #         if (node.isElement())
    #         {
    #             if (node.nodeName() == "color")
    #             {
    #                 readOk = readColor(m, node);
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readColor(self, m: Diagram, root):
        pass

    # bool DataReader::readColor(self, m:Diagram, root)
    # {
    #     bool readOk = false;
    #     unsigned int cid;
    #     QColor c("#000000");
    #     QDomNode node = root.firstChild();
    #     while (!node.isNull())
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "cid")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 if (!text.isNull())
    #                 {
    #                     cid = text.nodeValue().toInt();
    #                     readOk = true;
    #                 }
    #             }
    #             if (node.nodeName() == "hex")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 if (!text.isNull())
    #                 {
    #                     c = "#" + text.nodeValue().stripWhiteSpace();
    #                     readOk = true;
    #                 }
    #             }
    #         }
    #         m->setColorMapVal(cid, c);
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readPerm(self, m: Diagram, root, perm: Permutation):
        pass

    # bool DataReader::readPerm(self, m:Diagram, root, Permutation &perm)
    # {
    #     bool readOk = false;
    #     QDomNode node = root.firstChild();
    #     for (int i = 0; i < m->numColors(); i++)
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "perm")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 if (!text.isNull())
    #                 {
    #                     perm[i] = text.nodeValue().toInt();
    #                     readOk = true;
    #                 }
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readAdjacency(self, m: Diagram, root) -> bool:
        pass

    # bool DataReader::readAdjacency(self, m:Diagram, root)
    # {
    #     bool readOk = false;
    #     QDomNode node = root.firstChild();
    #     for (int i = 0; i < m->p(); i++)
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "entry")
    #             {
    #                 readOk = readEntry(m, node);
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readEntry(self, m: Diagram, root) -> bool:
        pass

    # bool DataReader::readEntry(self, m:Diagram, root)
    # {
    #     QDomAttr eAttr = root.toElement().attributeNode("e");
    #     int e = eAttr.value().toInt();

    #     bool readOk = false;
    #     QDomNode node = root.firstChild();
    #     while (!node.isNull())
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "orientation")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 readOk = false;
    #                 if (!text.isNull())
    #                 {
    #                     m->edges[e].setOrientation(orienMap[text.nodeValue().stripWhiteSpace()]);
    #                     readOk = true;
    #                 }
    #             }
    #             if (node.nodeName() == "edge")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 readOk = false;
    #                 if (!text.isNull())
    #                 {
    #                     // as a saftey take abs value of adjacent edge
    #                     m->edges[e].setAdjEdgeId(abs(text.nodeValue().toInt()));
    #                     readOk = true;
    #                 }
    #             }
    #             if (node.nodeName() == "color_perm")
    #             {
    #                 readOk = readPerm(m, node, m->edges[e].colorPerm());
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readElements(self, m: Diagram, root) -> bool:
        pass

    # bool DataReader::readElements(self, m:Diagram, root)
    # {
    #     bool readOk = false;
    #     QDomNode node = root.firstChild();
    #     while (!node.isNull())
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "elem")
    #             {
    #                 readOk = readElem(m, node);
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readElem(self, m: Diagram, root) -> bool:
        read_ok = False
        z_order = 1  # start with a low z-order
        e = 0
        # TODO: Check that these are the correct attributes references
        type_attr = root.attribute["type"].value()
        if not self.elemTypeMap.contains(type_attr):
            return False
        e = self.createElementObject(self.elemTypeMap[type_attr])
        if not e:
            return False
        node = root.firstChild()
        # Editied to here
        while not node.isNull():
            if node.isElement():
                read_ok = False
                if node.nodeName() == "z_order":
                    z_order = node.firstChild().toText().nodeValue().toInt()
                    read_ok = True
                if node.nodeName() == "color":
                    color_attr = (
                        node.firstChild().toText().nodeValue().stripWhiteSpace()
                    )
                    if not self.colorMap.contains(color_attr):
                        return False
                    e.setColor(self.colorMap[color_attr])
                    read_ok = True
                if node.nodeName() == "perm":
                    perm = Permutation(m.numColors())
                    read_ok = self.readPerm(m, node, perm)
                    e.setPerm(perm)
                if node.nodeName() == "adjacency":
                    read_ok = self.readAdjacency(m, node)
                if node.nodeName() == "label":
                    label = node.firstChild().toText().nodeValue().stripWhiteSpace()
                    e.setLabel(label)
                    read_ok = True
            node = node.nextSibling()

    # bool DataReader::readElem(self, m:Diagram, root)
    # {
    #     bool readOk = false;
    #     static int zorder = 1; // start with a low zorder
    #     ElementPtr e = 0;
    #     QDomAttr typeAttr = root.toElement().attributeNode("type");
    #     if (!elemTypeMap.contains(typeAttr.value()))
    #         return readOk = false;
    #     e = createElementObject(elemTypeMap[typeAttr.value()]);
    #     if (!e)
    #     {
    #         return readOk = false;
    #     }

    #     QDomNode node = root.firstChild();
    #     while (!node.isNull())
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "fill")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 readOk = false;
    #                 if (!text.isNull())
    #                 {
    #                     if (text.nodeValue().stripWhiteSpace() == "true")
    #                     {
    #                         e->setFilled(true);
    #                     }
    #                     else
    #                     {
    #                         e->setFilled(false);
    #                     }
    #                     readOk = true;
    #                 }
    #             }
    #             if (node.nodeName() == "cid")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 readOk = false;
    #                 if (!text.isNull())
    #                 {
    #                     e->setCid(text.nodeValue().toInt());
    #                     readOk = true;
    #                 }
    #             }
    #             if (node.nodeName() == "points")
    #             {
    #                 readOk = readPoints(node, e);
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     e->setZOrder(zorder);
    #     zorder++; // put next element to the front of the previous
    #     m->fundPat().addElement(e);
    #     delete e; // safe to delete e now that it is added
    #     return readOk;
    # }

    def readPoints(self, root, e: ElementPtr) -> bool:
        pass

    # bool DataReader::readPoints(root, ElementPtr e)
    # {
    #     bool readOk = false;
    #     QDomNode node = root.firstChild();
    #     while (!node.isNull())
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "pt")
    #             {
    #                 double x = 0.0, y = 0.0;
    #                 readOk = readPt(node, x, y);
    #                 Point pt(x, y);
    #                 pt.poincareToWeierstrass(); // convert to Weierstrass as we read
    #                 e->addPoint(pt);
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readPt(self, root, x: float, y: float) -> bool:
        pass

    # bool DataReader::readPt(root, double &x, double &y)
    # {
    #     bool readOk = false;
    #     QDomNode node = root.firstChild();
    #     while (!node.isNull())
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "x")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 readOk = false;
    #                 if (!text.isNull())
    #                 {
    #                     x = text.nodeValue().toDouble();
    #                     readOk = true;
    #                 }
    #             }
    #             if (node.nodeName() == "y")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 readOk = false;
    #                 if (!text.isNull())
    #                 {
    #                     y = text.nodeValue().toDouble();
    #                     readOk = true;
    #                 }
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def createElementObject(self, type: ElemType) -> ElementPtr:
        pass

    # ElementPtr DataReader::createElementObject(ElemType type)
    # {
    #     ElementPtr e = 0;
    #     switch (type)
    #     {
    #     case EUCLID_POLYLINE:
    #         e = new EuclidPolyLine();
    #         break;
    #     case EUCLID_POLY:
    #         e = new EuclidPoly();
    #         break;
    #     case CIRCLE:
    #         e = new Circle();
    #         break;
    #     case HYPER_POLYLINE:
    #         e = new HyperPolyLine();
    #         break;
    #     case HYPER_POLY:
    #         e = new HyperPoly();
    #         break;
    #     case ELEMENT:
    #         throw "Unexpected ElemType";
    #     }
    #     return e;
    # }


class DataReaderRegularPgon(DataReader):
    def __init__(self):
        super().__init__()

    def readXML(self, doc):
        pass


#     Diagram *DataReaderRegularPgon::readXML(QDomDocument &doc)
# {
#     RegularPgon *m = new RegularPgon();

#     QDomElement root = doc.documentElement();
#     if (root.tagName() != "design")
#     {
#         qWarning("Not a valid motif xml document");
#         return 0;
#     }

#     Diagram *d = dynamic_cast<Diagram *>(m);
#     QDomNode node;
#     node = root.firstChild();
#     bool readOk = true;
#     while (!node.isNull() && readOk)
#     {
#         if (node.isElement())
#         {
#             readOk = false;
#             if (node.nodeName() == "metadata")
#             {
#                 readOk = readMetadata(m, node);
#             }
#             if (node.nodeName() == "p")
#             {
#                 QDomText text = node.firstChild().toText();
#                 if (!text.isNull())
#                 {
#                     m->setP(text.nodeValue().toInt());
#                 }
#                 readOk = true;
#             }
#             if (node.nodeName() == "q")
#             {
#                 QDomText text = node.firstChild().toText();
#                 if (!text.isNull())
#                 {
#                     m->setQ(text.nodeValue().toInt());
#                 }
#                 readOk = true;
#             }
#             if (node.nodeName() == "fund_reg_edges")
#             {
#                 QDomText text = node.firstChild().toText();
#                 if (!text.isNull())
#                 {
#                     m->setFundRegEdges(text.nodeValue().toInt());
#                 }
#                 readOk = true;
#             }

#             if (node.nodeName() == "refl_sym_type")
#             {
#                 QDomText text = node.firstChild().toText();
#                 if (!text.isNull())
#                 {
#                     m->setReflSym(reflSymMap[text.nodeValue().stripWhiteSpace()]);
#                 }
#                 readOk = true;
#             }

#             if (node.nodeName() == "color_perm_rotn")
#             {
#                 readOk = readPerm(d, node, m->rotnColorPerm());
#             }
#             if (node.nodeName() == "color_perm_refl")
#             {
#                 readOk = readPerm(d, node, m->reflColorPerm());
#             }
#             if (node.nodeName() == "adjacency")
#             {
#                 readOk = readAdjacency(d, node);
#             }
#             if (node.nodeName() == "elements")
#             {
#                 readOk = readElements(d, node);
#             }
#         }
#         node = node.nextSibling();
#     }
#     if (readOk)
#     {
#         return m;
#     }
#     return 0;
# }


class DataReaderIrregularPgon(DataReader):
    def __init__(self):
        super().__init__()

    def readQlist(self, m, root):
        pass

    # bool DataReaderIrregularPgon::readQlist(IrregularPgon *m, root)
    # {
    #     bool readOk = true;
    #     QDomNode node = root.firstChild();
    #     for (int i = 0; readOk && i < m->p(); i++)
    #     {
    #         if (node.isElement())
    #         {
    #             if (node.nodeName() == "q")
    #             {
    #                 int qval;
    #                 readOk = readQ(node, qval);
    #                 if (readOk)
    #                 {
    #                     m->setQ(i, qval);
    #                 }
    #                 else
    #                 {
    #                     qWarning("Failed to read q value");
    #                 }
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     return readOk;
    # }

    def readQ(self, root, qval):
        pass

    # bool DataReaderIrregularPgon::readQ(root, int &qval)
    # {
    #     QDomText text = root.firstChild().toText();
    #     if (!text.isNull())
    #     {
    #         qval = text.nodeValue().toInt();
    #         return true;
    #     }
    #     return false;
    # }
    def readXML(self, doc):
        pass

    # Diagram *DataReaderIrregularPgon::readXML(QDomDocument &doc)
    # {
    #     IrregularPgon *m = new IrregularPgon();

    #     QDomElement root = doc.documentElement();
    #     if (root.tagName() != "design")
    #     {
    #         qWarning("Not a valid 'had' document");
    #         return 0;
    #     }

    #     Diagram *d = dynamic_cast<Diagram *>(m);
    #     QDomNode node;
    #     node = root.firstChild();
    #     bool readOk = true;
    #     while (!node.isNull() && readOk)
    #     {
    #         if (node.isElement())
    #         {
    #             readOk = false;
    #             if (node.nodeName() == "metadata")
    #             {
    #                 readOk = readMetadata(d, node);
    #             }
    #             if (node.nodeName() == "p")
    #             {
    #                 QDomText text = node.firstChild().toText();
    #                 if (!text.isNull())
    #                 {
    #                     m->setP(text.nodeValue().toInt());
    #                 }
    #                 readOk = true;
    #             }
    #             if (node.nodeName() == "qlist")
    #             {
    #                 readOk = readQlist(m, node);
    #             }
    #             if (node.nodeName() == "adjacency")
    #             {
    #                 readOk = readAdjacency(d, node);
    #             }
    #             if (node.nodeName() == "elements")
    #             {
    #                 readOk = readElements(d, node);
    #             }
    #         }
    #         node = node.nextSibling();
    #     }
    #     if (readOk)
    #     {
    #         return m;
    #     }
    #     return 0;
    # }
