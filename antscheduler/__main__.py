from GuiMain import main as guimain
from CliMain import main as climain
import sys

if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        climain()

    else:
        guimain()
