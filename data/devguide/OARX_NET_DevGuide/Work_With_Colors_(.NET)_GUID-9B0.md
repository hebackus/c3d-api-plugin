<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Colors (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9B0AA5E9-38DA-4E14-B22D-17923C89D29F.htm -->

# Work With Colors (.NET)

You can assign a color to an individual object in a drawing using its Color or ColorIndex property. The ColorIndex property accepts an AutoCAD Color Index (ACI) value as a numeric value of 0 - 256. The Color property is used to assign an ACI number, true color, or color book color to an object. To change the value of the Color property, you use the Color object which is under the Colors namespace. 

The Color object has a SetRGB method which allows you to choose from millions of color combinations based on mixing a red, green and blue color value together. The Color object also contains methods and properties for specifying color names, color books, color indexes, and color values. 

You can also assign colors to layers. If you want an object to inherit the color of the layer it is on, set the object’s color to ByLayer by setting its ACI value to 256. Any number of objects and layers can have the same color number. You can assign each color number to a different pen on a pen plotter or use the color numbers to identify certain objects in the drawing, even though you cannot see the colors on your screen.
