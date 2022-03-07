import logging
import os
import os.path as op
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QFile, QFileInfo, QIODevice, Qt, QTextStream
from PyQt6.QtGui import QAction, QKeySequence, QPainter, QTextDocument
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QInputDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
)

from .data_reader import DataReader
from .diagram_view import DiagramView
from .poincare_view import PoincareView
from .regular_polygon import RegularPgon

log = logging.getLogger(__name__)


class HyperArtWindow(QMainWindow):
    """
    _summary_

    Args:
        QMainWindow (_type_): _description_
    """

    def __init__(self):
        super().__init__()
        self.printer = QPrinter()
        self.curFile = None
        self.source_dir = Path(op.dirname(os.path.realpath(__file__)))
        self.setWindowTitle("Hyperart")
        Form, _ = uic.loadUiType(self.source_dir / "hyperart.ui")
        self.ui = Form()
        self.ui.setupUi(self)

        #   #by default show the poincare view
        #   #(currently the only one implemented)

        self.viewLayerActions = []
        viewLayerPopupMenu = QMenu("&Layer", self)
        self.ui.View.addMenu(viewLayerPopupMenu)

        self.numLayers = 3

        for i in range(9):
            layerId = str(i + 1)
            text = "Toggle Layer " + layerId
            menuText = "&" + layerId

            layerAction = QAction(menuText, self)
            layerAction.setText(text)
            layerAction.setCheckable(True)
            if i < self.numLayers:
                layerAction.setChecked(True)
            layerAction.setEnabled(False)
            layerAction.toggled.connect(self.toggleLayer)
            viewLayerPopupMenu.addAction(layerAction)

        self.dgram = RegularPgon()
        self.dgram.setNumLayers(self.numLayers)
        self.poincare = PoincareView("Poincare Disk View", self)
        self.poincare.setDocument(self.dgram)
        self.poincare.setFocus()
        self.setCentralWidget(self.poincare)

        self.setGeometry(100, 100, 800, 600)
        self.show()

    def destroy(self):
        """
        _summary_
        """
        self.printer = None

    def fileNew(self):
        """
        _summary_
        """
        ed = HyperArtWindow()
        ed.setWindowTitle("HyperArt")
        ed.show()

    def fileOpen(self):
        """
        _summary_
        """
        fn = QFileDialog.getOpenFileName(self, "Select Design", filter="*.had")[0]
        if fn:
            self.load(fn)
        else:
            self.statusBar().showMessage("Loading aborted", 2000)

    def fileSave(self):
        pass

    def fileSaveAs(self):
        """
        _summary_
        """
        fd = QFileDialog(self, "Save design as ...", True)  # a modal file dialog
        fd.setFileMode(QFileDialog.AnyFile)  # allow new filename creation
        fd.setFilter("Images (*.png *.jpg)")
        fi = QFileInfo(self.curFile)
        saveName = fi.baseName() + ".jpg"
        fd.setSelection(saveName)
        if fd.exec() == QDialog.Accepted:  # if the user clicked "OK"
            saveName = fd.selectedFile()
            self.view = self.resolveViewType(self.centralWidget())
            if not self.view:
                log.warning("HyperArt::load : invalid view object")
                return
            self.view.save(saveName)

    def filePrint(self):
        if self.printer.setup(self):  # printer dialog
            self.statusBar().message("Printing...")
            p = QPainter(self.printer)

            view = self.resolveViewType(self.centralWidget())
            if not view:
                log.warning("HyperArt::load : invalid view object")
                return

            view.print(p)
            self.statusBar().message("Printing completed", 2000)
        else:
            self.statusBar().message("Printing aborted", 2000)

    def fileExit(self):
        """
        _summary_
        """
        self.close()

    def editUndo(self):
        """
        _summary_
        """
        pass

    def editRedo(self):
        """
        _summary_
        """
        pass

    def editCut(self):
        """
        _summary_
        """
        pass

    def editCopy(self):
        pass

    def editPaste(self):
        pass

    def editFind(self):
        pass

    def helpIndex(self):
        pass

    def helpContents(self):
        pass

    def helpAbout(self):
        """
        Display the application's About box.
        """
        qm = QMessageBox()
        qm.about(
            self,
            "Hyper by Ajit Datar",
            (
                "Hyper lets you view and create repeating hyperbolic patterns "
                "using algorithms developed by Dr Douglas Dunham"
            ),
        )

    def load(self, fileName: str):
        """
        Determine type of document to be created and create it

        Args:
            fileName (str): _description_
        """

        d = DataReader.createDiagram(fileName)
        if d:
            self.dgram = d
            view = self.resolveViewType(self.centralWidget())
            if not view:
                log.warning("HyperArt::load : invalid view object")
                return
            view.setDocument(d)
            self.dgram.setNumLayers(self.numLayers)
            self.dgram.updateAllViews()
            self.setCentralWidget(view)
            self.setWindowTitle(fileName)
            self.curFile = fileName
            self.statusBar().showMessage("File loaded", 2000)

            self.animatePlayAction.setEnabled(True)
            self.animatePauseAction.setEnabled(True)
            self.animateStopAction.setEnabled(True)
            self.animatePrevAction.setEnabled(True)
            self.animateNextAction.setEnabled(True)
            self.zoomDefaultAction.setEnabled(True)
            self.zoomZoom_InAction.setEnabled(True)
            self.zoomZoom_outAction.setEnabled(True)
            self.viewToggle_FrameAction.setEnabled(True)
            self.filePrintAction.setEnabled(True)
            self.fileSaveAsAction.setEnabled(True)

            self.editPreferencesNumber_of_LayersAction.setEnabled(True)
            for i in range(9):
                if i < self.numLayers:
                    self.viewLayerActions[i].setEnabled(True)
                    self.viewLayerActions[i].setOn(True)

                else:
                    self.viewLayerActions[i].setEnabled(False)
                    self.viewLayerActions[i].setOn(False)

            self.statusBar().showMessage(f"Loaded document {fileName}", 2000)
        else:
            self.statusBar().showMessage(f"Failed to load document {fileName}", 2000)

    def resolveViewType(self, view) -> DiagramView:
        """
        _summary_

        Args:
            view (_type_): _description_

        Returns:
            DiagramView: _description_
        """
        # ref: bioinformatics.org/pipermail/wcurve-devel/2002-September/000001.html
        # if(PoincareView *poincare = dynamic_cast<PoincareView*>(view))
        #     return (DiagramView*)poincare
        if isinstance(view, PoincareView):
            return view
        # elif(other = dynamic_cast<SomeOtherView*>(view)):
        #     return (DiagramView*)other
        else:
            return None

    def animatePlay(self):
        # {
        #  emit doAnimatePlay()
        self.animatePrevAction.setEnabled(False)
        self.animateNextAction.setEnabled(False)
        self.animateStopAction.setEnabled(True)
        self.animatePauseAction.setEnabled(True)
        self.animatePlayAction.setEnabled(False)

    def animatePause(self):
        # {
        # emit doAnimatePause()
        self.PrevAction.setEnabled(True)
        self.NextAction.setEnabled(True)
        self.PauseAction.setEnabled(False)
        self.PlayAction.setEnabled(True)

    def animateStop(self):
        # {
        # emit doAnimateStop()
        self.PrevAction.setEnabled(False)
        self.NextAction.setEnabled(False)
        self.StopAction.setEnabled(False)
        self.PauseAction.setEnabled(False)
        self.PlayAction.setEnabled(True)

    def animateNext(self):
        # {
        # emit doAnimateNext()
        # }
        pass

    def animatePrev(self):
        # {
        # emit doAnimatePrev()
        # }
        pass

    def viewToggle_FrameAction_toggled(self, state: bool):
        # {
        # emit doToggleFrame(state)
        # }
        pass

    def zoomDefaultAction_activated(self):
        # {
        # emit doZoom(DEFAULT)
        # }
        pass

    def zoomZoom_InAction_activated(self):
        # {
        # emit doZoom(ZOOM_IN)
        # }
        pass

    def zoomZoom_outAction_activated(self):
        # {
        # emit doZoom(ZOOM_OUT)
        # }
        pass

    def viewLayerAction_activated(self, state: bool):
        # {
        # emit doToggleLayer(action.text().toInt()-1, state)
        # }
        pass

    def editPreferencesNumber_of_LayersAction_activated(self):
        ok = False
        res = QInputDialog.getInteger(
            "Number of layers",
            (
                "Enter how many layers to generate. \nPlease note that successful "
                "generation of 4 or more layers\ndepends on your system resources.\n"
                "The value set here will be used for designs loaded from now on."
            ),
            self.numLayers,
            1,
            9,
            1,
            ok,
            self,
        )
        if ok:
            if self.numLayers != res:
                self.numLayers = res
                view = self.resolveViewType(self.centralWidget())
                if not view:
                    log.warning("HyperArt::load : invalid view object")
                    return

            for i in range(9):
                if i < self.numLayers:
                    self.viewLayerActions[i].setEnabled(True)
                    self.viewLayerActions[i].setOn(True)

                else:
                    self.viewLayerActions[i].setEnabled(False)
                    self.viewLayerActions[i].setOn(False)

                self.dgram.setNumLayers(self.numLayers)
                self.dgram.updateAllViews()

        pass

    def fileSaveAsAction_activated(self):
        """
        _summary_
        """
        s = QFileDialog.getSaveFileName(
            self, "Save Diagram", self.curFile, "Hyper Diagram (*.hdi)All Files (*)"
        )
        if not s:
            return
            # emit doSaveAs(s)

    def filePrintAction_activated(self):
        """
        _summary_
        """
        # emit doPrint()
        pass

    def toggleLayer(self, state: bool):
        """
        _summary_

        Args:
            state (bool): _description_
        """
        text = self.sender().name()
        layerNum = text.toInt()
        # emit doToggleLayer(layerNum, state)
        pass

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        """
        _summary_

        Args:
            e (QtGui.QKeyEvent): _description_
        """
        k = e.key()
        if k == Qt.Key_Left:
            # emit doPanning(PAN_LEFT)
            pass
        elif k == Qt.Key_Right:
            # emit doPanning(PAN_RIGHT)
            pass
        elif k == Qt.Key_Up:
            # emit doPanning(PAN_UP)
            pass
        elif k == Qt.Key_Down:
            # emit doPanning(PAN_DOWN)
            pass
        else:
            e.ignore()
