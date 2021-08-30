# Plover Combo

A plugin for [Plover](https://github.com/openstenoproject/plover) that adds a Combo counter. Inspired by the [Code in the Dark Editor](https://github.com/codeinthedark/editor).

![combo](https://user-images.githubusercontent.com/30435273/131253406-878f1d0b-6f83-4d31-8f2b-b919f5f9424a.gif)

## Usage Notes

- `Ctrl/Cmd + S` to open settings, `Ctrl/Cmd + X` to close widget. 
- Left click on the counter number and drag to move the widget around. (On some systems, you'll have to click on the opaque areas of the font.)
- On macOS, you might experience repainting issues where a ghost image appears behind the counter. This issue has not been fixed yet.

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

Huge thanks to /usr and Emily on the Plover Discord for testing the plugin out on macOS!