<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Using VBA in Autodesk Civil 3D -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-BDF4897D-B1B8-4A86-835E-A080CC1D365C.htm -->

# Using VBA in Autodesk Civil 3D

The following Autodesk Civil 3D command-line instructions enable you to interact with the Visual Basic programming environment and loaded VBA macros.

Note:

VBA support is not included with Autodesk Civil 3D by default, and must be obtained as a separate download.

  * **VBAMAN** \- Displays a dialog box allowing you to load, unload, edit, embed, extract, edit, and save copies of VBA applications.
  * **VBAIDE** \- Displays the Visual Basic programming environment.
  * **VBARUN** \- Displays a dialog box where you can choose a macro to run from all the available subroutines.
  * **-VBARUN** _< module.macro>_ \- Runs a particular macro from the command line.
  * **VBALOAD** \- Loads a global VBA project into the current work session. After entering this instruction, you are presented with a file selection dialog box.
  * **-VBALOAD** _< full path and filename>_ \- Loads a particular project from the command line. If the path contains spaces, you need to type quotes around the path and filename string.
  * **VBAUNLOAD** \- Unloads an existing VBA project. After entering this instruction, you are prompted to type in the full path and filename of the project. If the path contains spaces, you need to type quotes around the path and filename string.
  * **VBASTMT** \- Executes a VBA statement on the command line. A statement generally occupies a single line, although you can use a colon (:) to include more than one statement on a line. VBA statements are executed in the context of the current drawing.

VBA projects are usually stored in separate _.dvb_ files, which allow macros to interact with many separate Autodesk Civil 3D drawings.
