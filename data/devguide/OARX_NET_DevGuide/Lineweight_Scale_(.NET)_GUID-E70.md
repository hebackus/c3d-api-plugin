<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Layouts (.NET) > Layout Settings (.NET) > Lineweight Scale (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E707ABCB-0D64-41C9-B432-B0FECDF7C1F5.htm -->

# Lineweight Scale (.NET)

Lineweights can be scaled proportionately in a layout with the plot scale. Typically, lineweights specify the linewidth of plotted objects and are plotted with the linewidth size regardless of the plot scale. Most often, you use the default plot scale of 1:1 when plotting a layout. However, if you want to plot an E-size layout that is scaled to fit on an A-size sheet of paper, for example, you can specify lineweights to be scaled in proportion to the new plot scale. 

The ScaleLineweights property retrurns whether lineweights are scaled or not; a value of TRUE indicates that lineweights are to be scaled when the layout is plotted.
