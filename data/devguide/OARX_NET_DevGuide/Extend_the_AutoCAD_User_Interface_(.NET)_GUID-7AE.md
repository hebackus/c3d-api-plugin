<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Extend the AutoCAD User Interface (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7AE1E920-2F7F-497B-A6C3-FB22987974B6.htm -->

# Extend the AutoCAD User Interface (.NET)

Custom dialog boxes can be used to get input from the user and extend the functionality of the AutoCAD user interface. 

AutoCAD Managed .NET classes allow applications to access many AutoCAD UI resources and incorporate new dialog boxes or forms. Some of the classes in the Autodesk.AutoCAD.Windows namespace provide access to AutoCAD feature dialog boxes, such as Linetype and Color. These classes provide a ShowDialog method that displays the form. When using these classes, an application automatically gains persistence for its dialog box size and position settings. 

The Autodesk.AutoCAD.Windows namespace also exposes interfaces that provide access to some extendible elements of the AutoCAD user interface, including palettes and palette sets, tray items, and the status bar. The classes and interfaces related to tool palettes are found in the Autodesk.AutoCAD.Windows.ToolPalette namespace. The AutoCAD icon, as well as the pick point and pick set bitmaps, can be accessed through the Autodesk.AutoCAD.Windows.Visuals class. 

Custom dialog boxes or forms in the AutoCAD Managed .NET API extend the classes from the System.Windows.Forms namespace directly. However, such applications should not call the Form.ShowDialog method but instead use the Autodesk.AutoCAD.ApplicationServices.Application.ShowModalDialog and ShowModelessDialog methods to display their custom forms. Using Form.ShowDialog in an AutoCAD extension application may result in unexpected behavior.
