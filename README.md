# Plover Combo
[![PyPI](https://img.shields.io/pypi/v/plover-combo)](https://pypi.org/project/plover-combo/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/plover-combo)
![GitHub](https://img.shields.io/github/license/Kaoffie/plover_combo)

A plugin for the open-source stenography software [Plover](https://www.openstenoproject.org) that adds a Combo counter. Inspired by the [Code in the Dark Editor](https://github.com/codeinthedark/editor).

![combo](https://user-images.githubusercontent.com/30435273/131253406-878f1d0b-6f83-4d31-8f2b-b919f5f9424a.gif)

## Usage Notes

- Shortcuts:
    - `Ctrl/Cmd + S` to open settings
    - `Ctrl/Cmd + X` to close widget. 

- Left click on the counter number and drag to move the widget around. (On some systems, you'll have to click on the opaque areas of the font.)
- After adjusting the settings, you might have to restart the plugin for all the changes to fully take effect.
- On macOS, you might experience repainting issues where a ghost image appears behind the counter. To fix this, turn on the "Force Repaint" option in the settings dialog.
- The window width is controlled by the width of the number currently displayed; to adjust the left and right padding, change the "Horizontal Margin" setting.

## Installation

This plugin isn't on the Plover Plugin Registry yet; install it with the following command:

```
plover -s plover_plugins install plover_combo
```

Alternatively, if you are on Windows, locate the directory where Plover.exe is located in and install using the following command:

```
.\plover_command.exe -s plover_plugins install plover_combo
```

## Credits

Huge thanks to /usr, Emily and Jen on the Plover Discord for testing the plugin out on macOS!