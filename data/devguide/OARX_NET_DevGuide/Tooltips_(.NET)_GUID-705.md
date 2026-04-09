<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > Tooltips (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-705CC39E-D2FA-470D-8252-5A4823A247A6.htm -->

# Tooltips (.NET)

Tooltips provide a short summary of a feature when the cursor of the pointing device is positioned over a command or control. 

The ToolTip and ToolTipContent classes of the Autodesk.AutoCAD.Customization namespace define the tooltips for commands and their content, respectively. When a tooltip is defined and assigned to a user interface element, the content of the tooltip can be displayed by positioning the cursor of the pointing device over the user interface element and pressing F1. 

The ToolTip and ToolTipService classes of the Autodesk.Windows namespace both derive from the classes of the same name in the System.Windows namespace. You use the Autodesk.Windows.ToolTip class to control the visual properties of a tooltip, such as showing and closing, fading in and fading out, and background opacity and color. The Autodesk.Windows.ToolTipService class is used to define the help source and topics for the text to be displayed.
