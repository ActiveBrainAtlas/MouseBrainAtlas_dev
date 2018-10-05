#! /usr/bin/env python

import sys, os
import argparse

import matplotlib.pyplot as plt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from multiprocess import Pool

sys.path.append(os.environ['REPO_DIR'] + '/utilities')
from utilities2015 import *
from metadata import *
from data_manager import *
from registration_utilities import find_contour_points
from gui_utilities import *
from qt_utilities import *
from preprocess_utilities import *
sys.path.append(os.path.join(os.environ['REPO_DIR'], 'web_services'))
#from web_service import web_services_request

from ui.ui_MaskEditingGui5 import Ui_MaskEditingGui
from widgets.DrawableZoomableBrowsableGraphicsScene import DrawableZoomableBrowsableGraphicsScene
from widgets.DrawableZoomableBrowsableGraphicsScene_ForMasking import DrawableZoomableBrowsableGraphicsScene_ForMasking
from widgets.DrawableZoomableBrowsableGraphicsScene_ForSnake import DrawableZoomableBrowsableGraphicsScene_ForSnake
from widgets.ZoomableBrowsableGraphicsScene import ZoomableBrowsableGraphicsScene
from DataFeeder import ImageDataFeeder_v2

#####################################################################

# STR_USING_AUTO = 'Using AUTO (Click to switch to USER)'
# STR_USING_USER = 'Using USER (Click to switch to AUTO)'

class MaskEditingGUI(QMainWindow):
    def __init__(self, parent=None, stack=None, version=None):
        QMainWindow.__init__(self, parent)

        self.stack = stack
        self.version = version

        self.ui = Ui_MaskEditingGui()
        self.dialog = QDialog(self)
        self.ui.setupUi(self.dialog)

        self.ui.button_snake.clicked.connect(self.do_snake_current_section)
        self.ui.button_update_merged_mask.clicked.connect(self.update_merged_mask_button_clicked)
        # self.ui.button_toggle_accept_auto.clicked.connect(self.toggle_accept_auto)
        # self.ui.button_toggle_accept_auto.setText(STR_USING_AUTO)
        # self.ui.button_autoSnake.clicked.connect(self.snake_all)
        self.ui.button_loadAnchorContours.clicked.connect(self.load_anchor_contours)
        self.ui.button_saveAnchorContours.clicked.connect(self.save_anchor_contours)
        self.ui.button_loadAllInitContours.clicked.connect(self.load_all_init_snake_contours)
        self.ui.button_saveAllInitContours.clicked.connect(self.save_all_init_snake_contours)
        self.ui.button_saveAllFinalMasks.clicked.connect(self.save_final_masks_all_sections)
        self.ui.button_saveCurrFinalMasks.clicked.connect(self.save_final_masks_curr_section)
        self.ui.button_exportAllMasks.clicked.connect(self.export_final_masks_all_sections)

        self.ui.slider_snakeShrink.setSingleStep(1)
        self.ui.slider_snakeShrink.setMinimum(0)
        self.ui.slider_snakeShrink.setMaximum(40)
        self.ui.slider_snakeShrink.setValue(MORPHSNAKE_LAMBDA1/.5)
        self.ui.slider_snakeShrink.valueChanged.connect(self.snake_shrinkParam_changed)

        self.ui.slider_minSize.setSingleStep(100)
        self.ui.slider_minSize.setMinimum(0)
        self.ui.slider_minSize.setMaximum(2000)
        self.ui.slider_minSize.setValue(MIN_SUBMASK_SIZE)
        self.ui.slider_minSize.valueChanged.connect(self.snake_minSize_changed)

        self.sections_to_filenames = DataManager.load_sorted_filenames(stack)[1]
        self.valid_sections_to_filenames = {sec: fn for sec, fn in self.sections_to_filenames.iteritems() if not is_invalid(fn)}
        self.valid_filenames_to_sections = {fn: sec for sec, fn in self.valid_sections_to_filenames.iteritems()}
        q = sorted(self.valid_sections_to_filenames.items())
        self.valid_sections = [sec for sec, fn in q]
        self.valid_filenames = [fn for sec, fn in q]

        ########################################################

        self.original_images = {}
        self.selected_channels = {}
        # self.thresholded_images = {}
        self.contrast_stretched_images = {}
        self.selected_snake_lambda1 = {}
        self.selected_snake_min_size = {}
        self.user_submasks = {}
        # self.accepted_final_masks = {}
        # self.accept_which = {sec: 0 for sec in self.valid_sections}
        self.merged_masks = {}
        self.merged_mask_vizs = {}

        user_submask_decisions = {}

        self.user_modified_sections = set([])

        # Load decisions from final decision file.
        from pandas import read_csv

        # auto_submask_rootdir = DataManager.get_auto_submask_rootdir_filepath(stack)
        for fn in self.valid_filenames:
            auto_decision_fp = DataManager.get_auto_submask_filepath(stack=stack, what='decisions', fn=fn)
            user_decision_fp = DataManager.get_user_modified_submask_filepath(stack=stack, fn=fn, what='decisions')

            if os.path.exists(user_decision_fp):
                sys.stderr.write('Loaded user-modified submasks for image %s.\n' % fn)
                user_submask_decisions[fn] = read_csv(user_decision_fp, header=None).to_dict()[1]
                self.user_submasks[fn] = {submask_ind: \
                imread(DataManager.get_user_modified_submask_filepath(stack=stack, what='submask', fn=fn, submask_ind=submask_ind)).astype(np.bool)
                for submask_ind in user_submask_decisions[fn].iterkeys()}
            elif os.path.exists(auto_decision_fp):
                user_submask_decisions[fn] = read_csv(auto_decision_fp, header=None).to_dict()[1]
                self.user_submasks[fn] = {submask_ind: \
                imread(DataManager.get_auto_submask_filepath(stack=stack, what='submask', fn=fn, submask_ind=submask_ind)).astype(np.bool)
                for submask_ind in user_submask_decisions[fn].iterkeys()}
            else:
                sys.stderr.write("No submasks exist for %s.\n" % fn)
                continue

        ######################################
        ## Generate submask review results. ##
        ######################################

        self.auto_submasks_gscene = DrawableZoomableBrowsableGraphicsScene_ForSnake(id='init_snake_contours', gview=self.ui.init_snake_contour_gview)
        self.auto_masks_feeder = ImageDataFeeder_v2(name='init_snake_contours', stack=self.stack, \
                                    sections=self.valid_sections, auto_load=True,
                                    resolution='thumbnail',
                                    prep_id='alignedPadded',
                                    version=self.version,
                                    use_thread=False)
                                    # labeled_filenames={sec: os.path.join(RAW_DATA_DIR, self.stack, fn + ".png")
                                        # for sec, fn in self.valid_sections_to_filenames.iteritems()})
        self.auto_submasks_gscene.set_data_feeder(self.auto_masks_feeder)
        self.auto_submasks_gscene.active_image_updated.connect(self.auto_submasks_gscene_section_changed)
        # self.auto_submasks_gscene.submask_decision_updated.connect(self.auto_submask_decision_updated)

        #########################################

        self.anchor_fn = DataManager.load_anchor_filename(stack=self.stack)
        filenames_to_sections, _ = DataManager.load_sorted_filenames(stack=self.stack)
        self.auto_submasks_gscene.set_active_section(filenames_to_sections[self.anchor_fn], emit_changed_signal=False)
        # self.auto_submasks_gscene.set_active_section(100, emit_changed_signal=False)

        ##########################
        ## User Submasks Gscene ##
        ##########################

        self.user_submasks_gscene = DrawableZoomableBrowsableGraphicsScene_ForMasking(id='user_submasks', gview=self.ui.gview_final_masks_user)
        self.user_submasks_feeder = ImageDataFeeder_v2(name='user_submasks', stack=self.stack, \
                                    sections=self.valid_sections, auto_load=True,
                                    resolution='thumbnail',
                                    prep_id='alignedPadded',
                                    version=self.version,
                                    use_thread=False)
        self.user_submasks_gscene.set_data_feeder(self.user_submasks_feeder)
        self.user_submasks_gscene.submask_decision_updated.connect(self.user_submask_decision_updated)
        self.user_submasks_gscene.submask_updated.connect(self.user_submask_updated)

        #######################################################

        def filter_by_keys(d, allowed_key_list):
            return {fn: v for fn, v in d.iteritems() if fn in allowed_key_list}

        def convert_keys_fn_to_sec(d):
            return {self.valid_filenames_to_sections[fn]: v for fn, v in d.iteritems()}

        self.user_submasks = convert_keys_fn_to_sec(filter_by_keys(self.user_submasks, self.valid_filenames))
        user_submask_decisions = convert_keys_fn_to_sec(filter_by_keys(user_submask_decisions, self.valid_filenames))

        #########################################################

        # self.ui.comboBox_channel.activated.connect(self.channel_changed)
        self.ui.comboBox_channel.addItems(['Red', 'Green', 'Blue'])
        self.ui.comboBox_channel.currentIndexChanged.connect(self.channel_changed)

        ###########################

        self.gscene_thresholded = ZoomableBrowsableGraphicsScene(id='thresholded', gview=self.ui.gview_thresholded)
        self.thresholded_image_feeder = ImageDataFeeder_v2(name='thresholded', stack=self.stack, \
                                                        sections=self.valid_sections, auto_load=False,
                                                        resolution='thumbnail',
                                                        use_thread=False
                                                        )
        self.gscene_thresholded.set_data_feeder(self.thresholded_image_feeder)

        #########################################################

        self.gscene_merged_mask = ZoomableBrowsableGraphicsScene(id='mergedMask', gview=self.ui.gview_merged_mask)
        self.merged_masks_feeder = ImageDataFeeder_v2(name='mergedMask', stack=self.stack, \
                                                sections=self.valid_sections, auto_load=False,
                                                resolution='thumbnail',
                                                use_thread=False)
        self.gscene_merged_mask.set_data_feeder(self.merged_masks_feeder)


        ########################################################

        try:
            self.load_all_init_snake_contours()
        except:
            sys.stderr.write('No initial snake contours are loaded.\n')

        try:
            self.user_submasks_gscene.set_submasks_and_decisions(submasks=self.user_submasks, submask_decisions=user_submask_decisions)
            for sec in self.valid_sections:
                self.update_merged_mask(sec=sec)
        except Exception as e:
            sys.stderr.write(str(e) + '\n')

        #########################################################

        self.dialog.showMaximized()


    def load_anchor_contours(self):
        contours_on_anchor_sections = load_pickle(DataManager.get_anchor_initial_snake_contours_filepath(self.stack))
        for sec, vertices in contours_on_anchor_sections.iteritems():
            self.auto_submasks_gscene.set_init_snake_contour(section=sec, vertices=vertices)
            self.auto_submasks_gscene.set_section_as_anchor(section=sec)

    def save_anchor_contours(self):
        contours_on_anchor_sections = \
            {sec: vertices_from_polygon(self.auto_submasks_gscene.init_snake_contour_polygons[sec])
            for sec in self.auto_submasks_gscene.anchor_sections}
        fp = DataManager.get_anchor_initial_snake_contours_filepath(self.stack)
        save_pickle(contours_on_anchor_sections, fp)
        print 'Anchor contours saved to', fp

    def load_all_init_snake_contours(self):
        init_snake_contours_on_all_sections = load_pickle(DataManager.get_initial_snake_contours_filepath(stack=self.stack))
        for fn, vertices in init_snake_contours_on_all_sections.iteritems():
            try:
                self.auto_submasks_gscene.set_init_snake_contour(section=self.valid_filenames_to_sections[fn], vertices=vertices)
            except:
                sys.stderr.write('Initial snake contour is not specified for image %s.\n' % fn)

    def save_all_init_snake_contours(self):
        """Save initial snake contours for all sections."""
        init_snake_contours_on_all_sections = {}
        for sec, fn in self.valid_sections_to_filenames.iteritems():
            if sec in self.auto_submasks_gscene.init_snake_contour_polygons:
                init_snake_contours_on_all_sections[fn] = vertices_from_polygon(self.auto_submasks_gscene.init_snake_contour_polygons[sec])
            else:
                sys.stderr.write("Image %s (section %d) does not have any initial snake contour.\n" % (fn, sec))
        fp = DataManager.get_initial_snake_contours_filepath(stack=self.stack)
        save_pickle(init_snake_contours_on_all_sections, fp)
        print 'Initial contours for all sections saved to', fp

    def save_final_masks_all_sections(self):
        # pool = Pool(16)
        # pool.map(lambda sec: self.save_submasks_and_decisions(submasks_dir=submasks_dir, sec=sec), self.valid_sections)
        # pool.close()
        # pool.join()
        for sec in self.user_modified_sections:
            self.save_submasks_and_decisions(sec=sec)
            # self.export_final_masks(sec=sec)

    def save_final_masks_curr_section(self):
        # submasks_dir = create_if_not_exists(DataManager.get_user_modified_submask_rootdir_filepath(stack=stack))
        self.save_submasks_and_decisions(sec=self.auto_submasks_gscene.active_section)
        # self.export_final_masks(sec=sec)

    def export_final_masks_all_sections(self):
        create_if_not_exists(DataManager.get_thumbnail_mask_dir_v3(stack=self.stack, prep_id='alignedPadded'))
        for sec in self.valid_sections:
            # imsave(DataManager.get_thumbnail_mask_filename_v3(stack=self.stack, section=sec, version='aligned'), self.merged_mask_vizs[sec])
            imsave(DataManager.get_thumbnail_mask_filename_v3(stack=self.stack, section=sec, prep_id='alignedPadded'), self.merged_mask_vizs[sec])
        sys.stderr.write('Export is completed.\n')

    def save_submasks_and_decisions(self, sec):
        # submasks = self.user_submasks
        # submask_decisions = self.user_submask_decisions

        if sec not in self.user_submasks or sec not in self.user_submasks_gscene._submask_decisions:
            return

        fn = self.valid_sections_to_filenames[sec]

        # submask_fn_dir = os.path.join(submasks_dir, fn)
        submask_fn_dir = DataManager.get_user_modified_submask_dir_filepath(stack=self.stack, fn=fn)
        execute_command('rm -rf \"%(dir_fp)s\"; mkdir -p \"%(dir_fp)s\"' % {'dir_fp': submask_fn_dir})

        # Save submasks
        for submask_ind, m in self.user_submasks[sec].iteritems():
            # submask_fp = os.path.join(submask_fn_dir, fn + '_alignedTo_' + self.anchor_fn + '_submask_%d.png' % submask_ind)
            submask_fp = DataManager.get_user_modified_submask_filepath(stack=self.stack, fn=fn, what='submask', submask_ind=submask_ind)
            imsave(submask_fp, np.uint8(m)*255)

        # Save submask contour vertices.
        submask_contour_vertices_fp = DataManager.get_user_modified_submask_filepath(stack=self.stack, fn=fn, what='contour_vertices')
        # submask_contour_vertices_fp = os.path.join(submask_fn_dir, fn + '_alignedTo_' + self.anchor_fn + '_submask_contour_vertices.pkl')
        submask_contour_vertices_dict = {}
        for submask_ind, m in self.user_submasks[sec].iteritems():
            cnts = find_contour_points(m)[1]
            if len(cnts) != 1:
                sys.stderr.write("Must have exactly one contour per submask, section %d, but the sizes are %s.\n" % (sec, map(len, cnts)))
            submask_contour_vertices_dict[submask_ind] = cnts[np.argsort(map(len, cnts))[-1]]
        save_pickle(submask_contour_vertices_dict, submask_contour_vertices_fp)

        # Save submask decisions.
        decisions_fp = DataManager.get_user_modified_submask_filepath(stack=self.stack, fn=fn, what='decisions')
        # decisions_fp = os.path.join(submask_fn_dir, fn +'_alignedTo_' + self.anchor_fn +  '_submasksUserReview.txt')
        from pandas import Series
        Series(self.user_submasks_gscene._submask_decisions[sec]).to_csv(decisions_fp)
        # save_json({k: int(v) for k,v in submask_decisions[sec].iteritems()}, decisions_fp)

        # Save parameters.
        params_fp = DataManager.get_user_modified_submask_filepath(stack=self.stack, fn=fn, what='parameters')
        params = {}
        if sec in self.selected_channels:
            params['channel'] = self.selected_channels[sec]
        if sec in self.selected_snake_lambda1:
            params['snake_lambda1'] = self.selected_snake_lambda1[sec]
        if sec in self.selected_snake_min_size:
            params['min_size'] = self.selected_snake_min_size[sec]
        if len(params) > 0:
            save_json(params, params_fp)

    @pyqtSlot(int, int)
    def user_submask_updated(self, sec, submask_ind):
        print "user_submask_updated"
        self.user_modified_sections.add(sec)
        contour_vertices = self.user_submasks_gscene.get_polygon_vertices(section=sec, polygon_ind=submask_ind)
        self.user_submasks[sec][submask_ind] = contours_to_mask([contour_vertices], self.user_submasks[sec][submask_ind].shape[:2])
        self.update_merged_mask()

    @pyqtSlot(int, int, bool)
    def user_submask_decision_updated(self, sec, submask_ind, decision):
        # self.user_submask_decisions[sec][submask_ind] = self.user_submasks_gscene._submask_decisions[sec][submask_ind]
        self.user_modified_sections.add(sec)
        self.update_merged_mask()
        self.update_mask_gui_window_title()

    # @pyqtSlot(int)
    # def auto_submask_decision_updated(self, submask_ind):
    #     self.update_merged_mask()
    #     self.update_mask_gui_window_title()

    @pyqtSlot()
    def update_merged_mask_button_clicked(self):
        sec = self.auto_submasks_gscene.active_section
        for submask_ind, m in self.user_submasks[sec].iteritems():
            contour_vertices = self.user_submasks_gscene.get_polygon_vertices(section=sec, polygon_ind=submask_ind)
            self.user_submasks[sec][submask_ind] = contours_to_mask([contour_vertices], m.shape[:2])
        self.update_merged_mask(sec=sec)

    def update_merged_mask(self, sec=None):
        """
        Update merged mask based on user submasks and decisions. Change the image shown in "Merged Mask" panel.
        """

        if sec is None:
            sec = self.auto_submasks_gscene.active_section

        if sec not in self.user_submasks_gscene._submask_decisions:
            sys.stderr.write("Section %d not in user_submask_decisions.\n" % sec)
            return

        accepted_submasks = [self.user_submasks[sec][sm_i] for sm_i, dec in self.user_submasks_gscene._submask_decisions[sec].iteritems() if dec]
        if len(accepted_submasks) == 0:
            sys.stderr.write('No submask accepted.\n')
            return
        else:
            merged_mask = np.any(accepted_submasks, axis=0)
        # else:
        #     raise Exception('accept_which is neither 0 or 1.')
        self.merged_masks[sec] = merged_mask
        self.merged_mask_vizs[sec] = img_as_ubyte(self.merged_masks[sec])
        self.merged_masks_feeder.set_image(sec=sec, numpy_image=self.merged_mask_vizs[sec])
        self.gscene_merged_mask.update_image(sec=sec)
        # except Exception as e:
        #     # sys.stderr.write('%s\n' % e)
        #     raise e

    def update_contrast_stretched_image(self, sec):
        if sec not in self.original_images:
            # img = DataManager.load_image_v2(stack=self.stack, section=sec, resol='thumbnail', prep_id=1, ext='tif')
            img = DataManager.load_image_v2(stack=self.stack, section=sec, resol='thumbnail', prep_id='alignedPadded', ext='tif', version=self.version)
            self.original_images[sec] = brightfieldize_image(img)
        if sec not in self.selected_channels:
            self.selected_channels[sec] = DEFAULT_MASK_CHANNEL

        if self.original_images[sec].ndim == 3:
            self.contrast_stretched_images[sec] = contrast_stretch_image(self.original_images[sec][..., self.selected_channels[sec]])
        elif self.original_images[sec].ndim == 2:
            self.contrast_stretched_images[sec] = contrast_stretch_image(self.original_images[sec])
        self.update_thresholded_image(sec=sec)

    def update_thresholded_image(self, sec=None):
        """
        Update the image in the thresholded image gscene, based on contrast_stretched_images.
        """

        print "update_thresholded_image"
        if sec is None:
            sec = self.auto_submasks_gscene.active_section
        self.thresholded_image_feeder.set_image(sec=sec, qimage=numpy_to_qimage(self.contrast_stretched_images[sec]))
        self.gscene_thresholded.update_image(sec=sec)

    def do_snake(self, sec):
        self.selected_snake_lambda1[sec] = self.ui.slider_snakeShrink.value() * .5
        self.selected_snake_min_size[sec] = self.ui.slider_minSize.value()

        init_snake_contour_vertices = vertices_from_polygon(self.auto_submasks_gscene.init_snake_contour_polygons[sec])
        submasks = snake(img=self.contrast_stretched_images[sec], init_contours=[init_snake_contour_vertices],
                        lambda1=self.selected_snake_lambda1[sec], min_size=self.selected_snake_min_size[sec])

        self.user_submasks[sec] = dict(enumerate(submasks))
        # self.user_submask_decisions[sec] = {sm_i: True for sm_i in self.user_submasks[sec].iterkeys()}

        self.user_submasks_gscene.set_submasks_and_decisions_one_section(sec=sec, submasks=self.user_submasks[sec], submask_decisions={sm_i: True for sm_i in self.user_submasks[sec].iterkeys()})
        # self.user_submasks_gscene.update_image_from_submasks_and_decisions(sec=sec)
        self.update_merged_mask(sec=sec)

        self.user_modified_sections.add(sec)


    def do_snake_current_section(self):
        self.do_snake(sec=self.auto_submasks_gscene.active_section)

    def channel_changed(self, index):
        # if index == self.selected_channels[self.auto_submasks_gscene.active_section]:
        #     return
        self.selected_channels[self.auto_submasks_gscene.active_section] = index
        # channel_text = str(self.sender().currentText())
        self.update_contrast_stretched_image(sec=self.auto_submasks_gscene.active_section)
        # if channel_text == 'Red':
        #     self.change_channel(0)
        # elif channel_text == 'Green':
        #     self.change_channel(1)
        # elif channel_text == 'Blue':
        #     self.change_channel(2)

    def snake_minSize_changed(self, value):
        self.ui.label_minSize.setText(str(value))

    def snake_shrinkParam_changed(self, value):
        self.ui.label_snakeShrink.setText(str(value*.5))

    def auto_submasks_gscene_section_changed(self):
        """
        What happens when the image in "Automatic Masks" panel is changed.
        """

        self.update_mask_gui_window_title()

        sec = self.auto_submasks_gscene.active_section

        # Set parameters if those for the current section have been modified before.

        if sec not in self.selected_channels:
            self.selected_channels[sec] = DEFAULT_MASK_CHANNEL

        self.ui.comboBox_channel.setCurrentIndex(self.selected_channels[sec])
        # self.change_channel(self.selected_channels[sec])

        # try:
        self.update_contrast_stretched_image(sec)
        self.gscene_thresholded.set_active_section(sec)
        # except: # The first time this will complain "Image not loaded" yet. But will not once update_thresholded_image() loads the image.
        #     pass

        if sec in self.selected_snake_lambda1:
            self.ui.slider_snakeShrink.setValue(self.selected_snake_lambda1[sec]/.5)
        else:
            self.ui.slider_snakeShrink.setValue(MORPHSNAKE_LAMBDA1/.5)

        if sec in self.selected_snake_min_size:
            self.ui.slider_minSize.setValue(self.selected_snake_min_size[sec])
        else:
            self.ui.slider_minSize.setValue(MIN_SUBMASK_SIZE)

        try:
            self.user_submasks_gscene.set_active_section(sec)
        except:
            pass

        try:
            self.gscene_merged_mask.set_active_section(sec)
        except:
            pass

    def update_mask_gui_window_title(self):
        curr_sec = self.auto_submasks_gscene.active_section
        curr_fn = self.valid_sections_to_filenames[curr_sec]
        try:
            title = '%s (%d) - Active: %s - Alg:%s User:%s' % (curr_fn, curr_sec, ['Alg', 'User'][self.accept_which[curr_sec]], self.auto_submask_decisions[curr_sec], self.user_submasks_gscene._submask_decisions[curr_sec])
            self.dialog.setWindowTitle(title)
            print title
        except:
            pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Mask Editing GUI')
    parser.add_argument("stack", type=str, help="stack name")
    parser.add_argument("version", type=str, help="version")
    args = parser.parse_args()
    
    app = QApplication(sys.argv)

    m = MaskEditingGUI(stack=args.stack, version=args.version)
    # m.showMaximized()
    m.show()
    sys.exit(app.exec_())
