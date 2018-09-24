from collections import defaultdict
from datetime import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from SignalEmittingItems import *
from ZoomableBrowsableGraphicsSceneWithReadonlyPolygon import ZoomableBrowsableGraphicsSceneWithReadonlyPolygon
from SignalEmittingGraphicsPathItemWithVertexCircles import SignalEmittingGraphicsPathItemWithVertexCircles

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from metadata import *
from data_manager import DataManager

class DrawableZoomableBrowsableGraphicsScene(ZoomableBrowsableGraphicsSceneWithReadonlyPolygon):
    """
    Extend base class by:
    - allowing user to draw polygons.
    """

    drawings_updated = pyqtSignal(object)
    polygon_completed = drawings_updated
    polygon_deleted = pyqtSignal(object, int, int)
    polygon_changed = pyqtSignal(int, int) # Notify upper parties to re-compute data for the changed polygon (e.g. binary masks)

    def __init__(self, id, gview=None, parent=None):
        super(DrawableZoomableBrowsableGraphicsScene, self).__init__(id=id, gview=gview, parent=parent)
        self.mode = 'idle'

        self.default_vertex_color = 'r'
        self.default_vertex_radius = 5

    def get_polygon_vertices(self, polygon_ind, section=None, index=None):
        index, _ = self.get_requested_index_and_section(i=index, sec=section)
        vertices = vertices_from_polygon(self.drawings[index][polygon_ind])
        return vertices

    def set_default_vertex_color(self, color):
        """
        Args:
            color (str): can be one of r,g or b
        """
        self.default_vertex_color = color

    def set_default_vertex_radius(self, size):
        self.default_vertex_radius = size

    def set_mode(self, mode):
        if hasattr(self, 'mode'):
            print 'Mode change:', self.mode, '=>', mode

        if mode == 'add vertices consecutively':
            self.gview.setDragMode(QGraphicsView.NoDrag)
        elif mode == 'idle':
            self.gview.setDragMode(QGraphicsView.ScrollHandDrag)
        elif mode == 'delete vertices':
            self.gview.setDragMode(QGraphicsView.RubberBandDrag)

        self.mode = mode

    def add_polygon_with_circles(self, path, linecolor=None, linewidth=None,
                                            vertex_color=None, vertex_radius=None,
                                            section=None, index=None):
        polygon = self.add_polygon(path, color=linecolor, linewidth=linewidth, index=index, section=section)
        if len(polygon.vertex_circles) == 2:
            raise
        polygon.signal_emitter.property_changed.connect(self.polygon_property_changed)

        if vertex_color is None:
            vertex_color = self.default_vertex_color

        if vertex_radius is None:
            vertex_radius = self.default_vertex_radius

        polygon.add_circles_for_all_vertices(radius=vertex_radius, color=vertex_color)
        polygon.set_closed(True)

        return polygon

    def add_polygon_with_circles_and_label(self, path, linecolor=None, linewidth=None,
                                            vertex_color=None, vertex_radius=None,
                                            label='unknown', label_pos=None,
                                            section=None, index=None, type=None,
                                            edits=[], side=None, side_manually_assigned=None,
                                            contour_id=None,
                                            position=None,
                                            category='contour', **kwargs):
        """
        Additional keyword arguments are used to set polygon properties.
        - set_name (str): specifies the set this polygon belongs to (handdrawn or aligned_atlas)

        Args:
            type (str): One of the following,
                    - derived_from_atlas
                    - confirmed (hand-drawn or confirming interpolated polygons)
                    - interpolated
        """

        closed = polygon_is_closed(path=path)
        vertices = vertices_from_polygon(path=path, closed=closed)
        if len(vertices) == 2:
            raise Exception("Polygon has only two vertices. Skip adding this polygon.")

        if index is not None:
            assert isinstance(index, int), "add_polygon_with_circles_and_label(): Argument `index` must be integer."

        polygon = self.add_polygon_with_circles(path, linecolor=linecolor, linewidth=linewidth,
                                                vertex_color=vertex_color, vertex_radius=vertex_radius,
                                                section=section, index=index)
        polygon.signal_emitter.property_changed.connect(self.polygon_property_changed)

        # Compute the polygon's coordinate in the depth dimension.
        if hasattr(self.data_feeder, 'sections'):
            if section is None:
                section = self.data_feeder.sections[index]
            position = DataManager.convert_section_to_z(sec=section, resolution=self.data_feeder.resolution, mid=True, stack=self.gui.stack)
            # z0, z1 = self.convert_section_to_z(sec=section, downsample=self.data_feeder.downsample, mid=True)
            # position = (z0 + z1) / 2
        else:
            position = index
        polygon.set_properties('position', position)

        polygon.set_properties('label', label)
        if label_pos is not None:
            polygon.set_properties('label_pos', label_pos)
        polygon.set_properties('type', type)
        polygon.set_properties('side', side)
        polygon.set_properties('side_manually_assigned', side_manually_assigned)
        polygon.set_properties('contour_id', contour_id) # Could be None - will be generated new in convert_drawings_to_entries()

        polygon.set_properties('orientation', self.data_feeder.orientation)

        if edits is None or len(edits) == 0:
            polygon.set_properties('edits',
            [{'username': self.gui.get_username(), 'timestamp': datetime.now().strftime("%m%d%Y%H%M%S")}])
        else:
            polygon.set_properties('edits', edits)

        polygon.set_properties('class', category)

        if hasattr(self.data_feeder, 'sections'):
            polygon.set_properties('section', section)
            d_voxel = DataManager.convert_section_to_z(sec=section, resolution=self.data_feeder.resolution, mid=True, stack=self.gui.stack)
            d_um = d_voxel * convert_resolution_string_to_voxel_size(stack=self.gui.stack, resolution=self.data_feeder.resolution)
            polygon.set_properties('position_um', d_um)
            # print 'd_voxel', d_voxel, 'position_um', d_um
        else:
            polygon.set_properties('voxel_position', index)
            d_um = index * convert_resolution_string_to_voxel_size(stack=self.gui.stack, resolution=self.data_feeder.resolution)
            polygon.set_properties('position_um', d_um)
            # print 'index', index, 'position_um', d_um

        for key, value in kwargs.iteritems():
            polygon.set_properties(key, value)

        return polygon

    @pyqtSlot(str, object, object)
    def polygon_property_changed(self, property_name, new_value, old_value):
        """
        This function deals with cases when setting polygon property affect gscene display.
        """

        polygon = self.sender().parent
        # sender is signal_emitter; its parent is polygon

        # Set polygon color if polygon type property is changed.
        if property_name == 'type':
            print property_name, new_value, old_value
            if new_value == 'confirmed':
                curr_pen = polygon.pen()
                curr_pen.setColor(Qt.red)
                polygon.setPen(curr_pen)
            elif new_value == 'intersected':
                curr_pen = polygon.pen()
                curr_pen.setColor(Qt.green)
                polygon.setPen(curr_pen)

        # If polygon label is set, add label textitems.
        if property_name == 'label':
            if 'label_textItem' not in polygon.properties or polygon.properties['label_textItem'] is None:
                # assert polygon.properties['label_pos'] is None
                # Use the centroid of polygon vertices.
                label_textItem = QGraphicsSimpleTextItem(QString(new_value), parent=polygon)
                label_textItem.setScale(1.5)
                label_textItem.setFlags(QGraphicsItem.ItemIgnoresTransformations | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemClipsToShape | QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemSendsScenePositionChanges)
                label_textItem.setZValue(99)
                polygon.set_properties('label_textItem', label_textItem)
                if not hasattr(polygon.properties, 'label_pos') or polygon.properties['label_pos'] is None:
                    centroid = np.mean([(v.scenePos().x(), v.scenePos().y()) for v in polygon.vertex_circles], axis=0)
                    polygon.set_properties('label_pos', centroid)
            else:
                polygon.properties['label_textItem'].setText(new_value)

        if property_name == 'label_pos':
            assert polygon.properties['label_textItem'] is not None
            polygon.properties['label_textItem'].setPos(new_value[0], new_value[1])


    def add_polygon(self, path=QPainterPath(), color=None, linewidth=None, section=None, index=None, z_value=50, vertex_color=None, vertex_radius=None):
        '''
        Add a polygon to a specified section.

        Args:
            path (QPainterPath): path of the polygon
            pen (QPen): pen used to draw polygon

        Returns:
            QGraphicsPathItemModified: added polygon
        '''

        if color is None:
            color = self.default_line_color

        if color == 'r':
            pen = QPen(Qt.red)
        elif color == 'g':
            pen = QPen(Qt.green)
        elif color == 'b':
            pen = QPen(Qt.blue)
        elif color == 'w':
            pen = QPen(Qt.white)
        elif isinstance(color, tuple) or  isinstance(color, list):
            pen = QPen(QColor(color[0], color[1], color[2]))
        else:
            raise Exception('color argument to polygon must be r,g,b or w')

        if linewidth is None:
            linewidth = self.default_line_width
        pen.setWidth(linewidth)

        if vertex_radius is None:
            vertex_radius = self.default_vertex_radius

        index, _ = self.get_requested_index_and_section(i=index, sec=section)

        polygon = SignalEmittingGraphicsPathItemWithVertexCircles(path, gscene=self, vertex_radius=vertex_radius)

        polygon.setPen(pen)
        polygon.setZValue(z_value)
        polygon.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemClipsToShape | QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemSendsScenePositionChanges)
        polygon.setFlag(QGraphicsItem.ItemIsMovable, False)

        polygon.signal_emitter.press.connect(self.polygon_pressed_callback)
        # polygon.signal_emitter.release.connect(self.polygon_release)
        polygon.signal_emitter.vertex_added.connect(self.vertex_added)
        # polygon.signal_emitter.vertex_clicked.connect(self.vertex_clicked)
        polygon.signal_emitter.polygon_changed.connect(self.polygon_changed_callback)
        polygon.signal_emitter.polygon_completed.connect(self.polygon_completed_callback)
        polygon.signal_emitter.property_changed.connect(self.polygon_property_changed)

        self.drawings[index].append(polygon)
        self.drawings_mapping[polygon] = index

        # if adding polygon to current section
        if index == self.active_i:
            print 'polygon added.'
            self.addItem(polygon)

        return polygon

    @pyqtSlot()
    def polygon_changed_callback(self):
        sending_polygon = self.sender().parent # Must get parent because sender is the signal_emitter object.
        sending_index = self.drawings_mapping[sending_polygon]
        polygon_ind = self.drawings[sending_index].index(sending_polygon)
        _, sending_sec = self.get_requested_index_and_section(i=sending_index)
        self.polygon_changed.emit(sending_sec, polygon_ind)

    @pyqtSlot(QGraphicsEllipseItemModified)
    def vertex_added(self, circle):
        pass
        # polygon = self.sender().parent
        # if polygon.index == self.active_i:
        #     pass

    @pyqtSlot()
    def polygon_completed_callback(self):
        polygon = self.sender().parent
        self.set_mode('idle')
        self.drawings_updated.emit(polygon)

    @pyqtSlot(object)
    def polygon_pressed_callback(self, polygon):

        print 'polygon pressed'

        if self.mode == 'add vertices consecutively':
            # if we are adding vertices, do nothing when the click triggers a polygon.
            pass
        else:
            self.active_polygon = polygon
            print 'active polygon selected', self.active_polygon
            self.polygon_pressed.emit(polygon)

    def show_context_menu(self, pos):
        myMenu = QMenu(self.gview)

        action_newPolygon = myMenu.addAction("New polygon")
        action_deletePolygon = myMenu.addAction("Delete polygon")
        action_insertVertex = myMenu.addAction("Insert vertex")
        action_deleteVertices = myMenu.addAction("Delete vertices")

        selected_action = myMenu.exec_(self.gview.viewport().mapToGlobal(pos))

        if selected_action == action_newPolygon:
            self.close_curr_polygon = False
            self.active_polygon = self.add_polygon(QPainterPath(), index=self.active_i, linewidth=10)
            self.active_polygon.set_closed(False)
            self.set_mode('add vertices consecutively')

        # elif selected_action == action_deletePolygon:
        #     self.polygon_deleted.emit(self.active_polygon, self.active_i, self.drawings[self.active_i].index(self.active_polygon))
        #     sys.stderr.write('%s: polygon_deleted signal emitted.\n' % (self.id))
        #     self.drawings[self.active_i].remove(self.active_polygon)
        #     self.removeItem(self.active_polygon)

        elif selected_action == action_insertVertex:
            self.set_mode('add vertices randomly')

        elif selected_action == action_deleteVertices:
            self.set_mode('delete vertices')

    def delete_all_polygons_one_section(self, section):
        index, _ = self.get_requested_index_and_section(sec=section)
        print "before delete", self.drawings[index]

        # Be careful not to modify self.drawings within the loop !
        for polygon_index, polygon in enumerate(self.drawings[index]):
            self.drawings_mapping.pop(polygon)
            self.removeItem(polygon)
            self.polygon_deleted.emit(polygon, index, polygon_index)
            sys.stderr.write('%s: polygon_deleted signal emitted.\n' % (self.id))

        self.drawings[index] = []
        print "after delete", self.drawings[index]

    @pyqtSlot()
    def delete_polygon(self, section=None, polygon_ind=None, index=None, polygon=None):
        """
        Specify either section/index + polygon_ind or polygon object.
        """

        if polygon is None:
            assert section is not None or index is not None
            index, section = self.get_requested_index_and_section(i=index, sec=section)
            assert polygon_ind is not None
            polygon = self.drawings[index][polygon_ind]
        else:
            index = self.drawings_mapping[polygon]
            polygon_ind = self.drawings[index].index(polygon)

        self.drawings[index].remove(polygon)
        self.drawings_mapping.pop(polygon)
        self.removeItem(polygon)

        self.polygon_deleted.emit(polygon, index, polygon_ind)
        sys.stderr.write('%s: polygon_deleted signal emitted.\n' % (self.id))

    @pyqtSlot()
    def vertex_clicked(self):
        # pass
        circle = self.sender().parent
        print 'vertex clicked:', circle

    @pyqtSlot()
    def vertex_released(self):
        # print self.sender().parent, 'released'

        clicked_vertex = self.sender().parent

        if self.mode == 'moving vertex' and self.vertex_is_moved:
            self.vertex_is_moved = False

    def eventFilter(self, obj, event):

        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_Escape:
                self.set_mode('idle')
                return True

            elif (key == Qt.Key_Enter or key == Qt.Key_Return) and self.mode == 'add vertices consecutively': # CLose polygon
                first_circ = self.active_polygon.vertex_circles[0]
                first_circ.signal_emitter.press.emit(first_circ)
                return False

        elif event.type() == QEvent.GraphicsSceneMousePress:

            pos = event.scenePos()
            gscene_x = pos.x()
            gscene_y = pos.y()

            if event.button() == Qt.RightButton:
                obj.mousePressEvent(event)

            if self.mode == 'idle':
                # pass the event down
                obj.mousePressEvent(event)

                self.press_screen_x = gscene_x
                self.press_screen_y = gscene_y
                print self.press_screen_x, self.press_screen_y
                self.pressed = True
                return True

            elif self.mode == 'add vertices consecutively':
                # if in add vertices mode, left mouse press means:
                # - closing a polygon, or
                # - adding a vertex

                if event.button() == Qt.LeftButton:
                    obj.mousePressEvent(event)
                    if not self.active_polygon.closed:
                        if 'class' in self.active_polygon.properties and self.active_polygon.properties['class'] == 'neuron':
                            vertex_color = 'r'
                        else:
                            vertex_color = 'b'
                        self.active_polygon.add_vertex(gscene_x, gscene_y, color=vertex_color)
                    return True

            elif self.mode == 'add vertices randomly':
                if event.button() == Qt.LeftButton:
                    obj.mousePressEvent(event)

                    assert self.active_polygon.closed, 'Insertion is not allowed if polygon is not closed.'
                    new_index = find_vertex_insert_position(self.active_polygon, gscene_x, gscene_y)
                    if 'class' in self.active_polygon.properties and self.active_polygon.properties['class'] == 'neuron':
                        vertex_color = 'r'
                    else:
                        vertex_color = 'b'
                    self.active_polygon.add_vertex(gscene_x, gscene_y, new_index, color=vertex_color)

                    return True

        elif event.type() == QEvent.GraphicsSceneMouseRelease:

            if self.mode == 'delete vertices':
                items_in_rubberband = self.analyze_rubberband_selection()
                print "items_in_rubberband", items_in_rubberband
                for polygon, vertex_indices in items_in_rubberband.iteritems():
                    polygon.delete_vertices(vertex_indices, merge=True)
                self.set_mode('idle')

                return True

        return super(DrawableZoomableBrowsableGraphicsScene, self).eventFilter(obj, event)

    def analyze_rubberband_selection(self):
        """
        Returns:
            dict {polygon: vertex_indices}
        """

        items_in_rubberband = self.selectedItems()

        items_involved = defaultdict(list)
        for item in items_in_rubberband:
            if isinstance(item, QGraphicsEllipseItemModified):
                items_involved[item.polygon].append(item.polygon.vertex_circles.index(item))
        items_involved.default_factory = None
        return items_involved

    def set_active_i(self, i, emit_changed_signal=True):

        for polygon in self.drawings[self.active_i]:
            self.removeItem(polygon)

        super(DrawableZoomableBrowsableGraphicsScene, self).set_active_i(i, emit_changed_signal=emit_changed_signal)

        for polygon in self.drawings[i]:
            self.addItem(polygon)
