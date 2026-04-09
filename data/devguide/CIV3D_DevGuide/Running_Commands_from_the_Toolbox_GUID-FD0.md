<!-- Developer's Guide > API Developer's Guide > Getting Started > Running Commands from the Toolbox > Running Commands from the Toolbox -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FD05D402-7082-4530-9943-E7BE0ED7A399.htm -->

# Running Commands from the Toolbox

To create a toolbox macro for a compiled command using the Toolbox Editor

  1. Click the Toolbox tab in Toolspace.
  2. Click to open the Toolbox Editor.
  3. Right-click Miscellaneous Utilities and click New Category. 
  4. Right-click the new category, and click New Tool.
  5. Select the new tool, and enter its name.
  6. For Execute Type, click the drop-down and select CMD or .NET.

Note:

CMD is the recommended execution type in most cases, because you do not need to explicitly handle document locking. See the discussion above.

  7. For Execute File, browse to the .NET assembly or ARX DLL that contains the command.
  8. For Macro Name, enter:
     * Name of the command to run, if the execute type is CMD
     * Name of the method to run, if the execute type is .NET.
  9. Optionally, enter a help file and help topic for the command.
  10. Click  to apply the changes and close the editor.

After a command has been set up, it can be run by right-clicking it and clicking Execute.
