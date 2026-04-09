<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > Mouse Button Behavior (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B0D1B503-D3A7-4495-8833-C04E7907F162.htm -->

# Mouse Button Behavior (.NET)

Mouse and digitizer button actions can be customized by associating them with shortcut menus or macro commands. The left mouse button and mouse wheel functions cannot be changed. 

Custom actions for the middle and right buttons work properly based upon the value of the MBUTTONPAN and SHORTCUTMENU system variables. 

The CustomizationSection.MenuGroup.MouseButtons property returns a MouseButtonGroupCollection collection of ButtonGroup objects. Each ButtonGroup object is a collection of ButtonItem objects. You use the ButtonItems property of the ButtonGroup object to get the ButtonItemCollection object. The ButtonItem object defines the behavior of a button by attaching a macro. The button items define the behavior for regular clicks and clicks executed while an accelerator key (SHIFT, CTRL or SHIFT+CTRL) is pressed and held. 

Use the CustomizationSection.MenuGroup.DigitzerButtons collection to modify digitizer button behavior.
