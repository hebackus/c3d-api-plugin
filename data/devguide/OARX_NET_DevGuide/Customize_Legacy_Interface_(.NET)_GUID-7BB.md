<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > Customize Legacy Interface (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7BB96748-D236-4860-BF83-E2840E463C2D.htm -->

# Customize Legacy Interface (.NET)

Screen menus, Image menus, Tablet menus, and Tablet buttons are legacy interface elements that can be accessed from a customization section’s menu group. 

Screen menus use blank lines as separators. The ScreenMenuItem.BlankLine property is used to set this up. Use ScreenMenu.AddBlankLine() to add a blank line to the end of the menu. You can also add lines by increasing the NumLines property of the screen menu, which adds blank lines at the end of the collection.
