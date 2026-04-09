<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Unicode Characters, Control Codes, and Special Characters (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-5DB14D3C-E778-42AA-8560-57A67900C515.htm -->

# Use Unicode Characters, Control Codes, and Special Characters (.NET)

You can use Unicode characters, control codes, and special characters in a text string to represent symbols. (All nontext characters must be entered as their ASCII equivalent.) 

You can create special characters by entering the following Unicode character strings: 

Unicode character descriptions   
---  
Unicode character  |  Description   
\U+00B0  |  Degree symbol   
\U+00B1  |  Plus/minus tolerance symbol   
\U+2205  |  Diameter dimensioning symbol   
  
In addition to using Unicode characters for special characters, you can specify a special character by including control information in the text string. Use a pair of percent signs (%%) to introduce each control sequence. For example, the following control code works with standard AutoCAD text and PostScript fonts to draw character number _nnn_ : 
    
    
    %%nnn
    

These control codes work with standard AutoCAD text fonts only: 

Control code descriptions   
---  
Control code  |  Description   
%%o  |  Toggles overscore mode on and off   
%%u  |  Toggles underscore mode on and off   
%%d  |  Draws degree symbol   
%%p  |  Draws plus and minus tolerance symbol   
%%c  |  Draws diameter dimensioning symbol   
%%%  |  Draws single percent sign
