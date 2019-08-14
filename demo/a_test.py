import math
from PyQt4 import QtCore, QtGui

class DraggableGraphicsItemSignaller(QtCore.QObject):

    positionChanged = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self):
        super( QtCore.QObject, self ).__init__()

def make_GraphicsItem_draggable(parent):

    class DraggableGraphicsItem(parent):

        def __init__(self, *args, **kwargs):
            """
            By default QGraphicsItems are not movable and also do not emit signals when the position is changed for
            performance reasons. We need to turn this on.
            """
            parent.__init__(self, *args, **kwargs)
            self.parent = parent
            self.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemSendsScenePositionChanges)
            self.signaller = DraggableGraphicsItemSignaller()

        def itemChange(self, change, value):
            if change == QtGui.QGraphicsItem.ItemPositionChange:
                value2 = value.toPyObject()
                self.signaller.positionChanged.emit(value2)

            return parent.itemChange(self, change, value)

    return DraggableGraphicsItem

def rotate_item(position):
    item_position = item.transformOriginPoint()
    angle = math.atan2(item_position.y() - position.y(), item_position.x() - position.x()) / math.pi * 180 - 45 # -45 because handle item is at upper left border, adjust to your needs
    print(angle)
    item.setRotation(angle)


DraggableRectItem = make_GraphicsItem_draggable(QtGui.QGraphicsRectItem)

app = QtGui.QApplication([])

scene = QtGui.QGraphicsScene()
item = scene.addRect(0, 0, 100, 100)
item.setTransformOriginPoint(50, 50)

handle_item = DraggableRectItem( )
handle_item.signaller.positionChanged.connect(rotate_item)
handle_item.setRect(-40, -40, 20, 20)
scene.addItem(handle_item)

view = QtGui.QGraphicsView(scene)
view.setFixedSize(300, 200)
view.show()

app.exec_()