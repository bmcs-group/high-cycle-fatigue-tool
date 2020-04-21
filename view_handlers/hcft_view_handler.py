import traitsui.api as ui
import traits.api as tr
import pickle
import os
from traitsui.file_dialog import open_file, save_file

from utils.csv_joiner import CSVJoiner

menu_exit = ui.Action(name='Exit', action='menu_exit')
menu_save = ui.Action(name='Save', action='menu_save')
menu_open = ui.Action(name='Open', action='menu_open')

menu_utilities_csv_joiner = ui.Action(name='CSV Joiner', action='menu_utilities_csv_joiner')

class ViewHandler(ui.Handler):

    info = tr.Instance(ui.UIInfo)

    exit_view = ui.View(
        ui.VGroup(
            ui.Label('Do you really wish to end '
                  'the session? Any unsaved data '
                  'will be lost.'),
            ui.HGroup(ui.Item('ok', show_label=False, springy=True),
                   ui.Item('cancel', show_label=False, springy=True)
                   )
        ),
        title='Exit dialog',
        kind='live'
    )

    def menu_utilities_csv_joiner(self):
        csv_joiner = CSVJoiner()
        # kind='modal' pauses the background traits window until this window is closed
        csv_joiner.configure_traits(kind='modal')

    def get_outfile(self, folder_name, file_name):
        '''Returns a file in the specified folder using the home
        directory as root.
        '''
        HOME_DIR = os.path.expanduser("~")
        out_dir = os.path.join(HOME_DIR, folder_name)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        outfile = os.path.join(out_dir, file_name)
        return outfile

    def menu_save(self, info):
        file_name = self.get_outfile(folder_name='.hcft', file_name='')
        file_ = save_file(file_name=file_name)
        if file_:
            pickle.dump(info.object.root, open(file_, 'wb'), 1)

    def menu_open(self, info):
        file_name = self.get_outfile(folder_name='.hcft', file_name='')
        file_ = open_file(file_name=file_name)
        if file_:
            info.object.root = pickle.load(open(file_, 'rb'))

    def menu_exit(self, info):
        if info.initialized:
            self.info = info
            self._ui = self.edit_traits(view='exit_view')