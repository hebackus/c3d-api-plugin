<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Layouts (.NET) > Layout Settings (.NET) > Plot Area (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9F7F854D-5172-4F42-A6C5-E7E54DF6E0B6.htm -->

# Plot Area (.NET)

When a layout is plotted, the area in which is plotted is determined by the PlotType property. The value stored in the PlotType property is one of the values defined by the PlotType enum. The PlotType enum defines the following values: 

Display
    

Prints everything that is in the current model space display. This option is unavailable when plotting from a Paper space layout. 

Extents
    

Prints everything that falls within the boundaries of the currently selected space. 

Limits
    

Prints everything that is in the limits of the current space. 

View
    

Prints the view named by the PlotViewName property. 

Window
    

Prints everything in the window specified by the PlotWindowArea property. 

Layout
    

Prints everything that falls within the margins of the specified paper size. This option is not available when printing from Model space. 

When you create a new Paper space layout, the default option is Layout.
