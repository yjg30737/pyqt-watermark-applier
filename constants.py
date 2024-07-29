
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

__version__ = '0.1.0'
__author__ = 'YJGSoft'

APP_ICON = 'icon.ico'
APP_NAME = 'YJG Watermark Applier'
LICENSE = 'MIT'
COMPANY_LOGO = 'yjgsoft_logo.png'
CONTACT = 'yjg30737@gmail.com'
FRAMEWORK = 'PySide6'

PAYPAL_URL = 'https://paypal.me/yjg30737'
BUYMEACOFFEE_URL = 'https://www.buymeacoffee.com/yjg30737'
GITHUB_URL = 'https://github.com/yjg30737/pyqt-watermark-applier'
DISCORD_URL = 'https://discord.gg/cHekprskVE'

ICON_DISCORD = 'ico/discord.svg'
ICON_GITHUB = 'ico/github.svg'
ICON_CLOSE = 'ico/close.svg'

EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_FAMILY = 'Arial'

# Update the __all__ list with the PEP8 standard dunder names
__all__ = ['__version__',
           '__author__']

# Update the __all__ list with the constants
__all__.extend([name for name, value in globals().items() if name.isupper()])
