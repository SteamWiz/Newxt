from wizlib.app import WizApp
from wizlib.stream_handler import StreamHandler
from wizlib.config_handler import ConfigHandler
from wizlib.ui_handler import UIHandler

from newxt.command import NewxtCommand


class NewxtApp(WizApp):

    base = NewxtCommand
    name = 'newxt'
    handlers = [StreamHandler, ConfigHandler, UIHandler]
