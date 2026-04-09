<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Single-Line Text (.NET) > Format Single-Line Text (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4410A195-214E-4F9D-AF7E-5D8390C8CE08.htm -->

# Format Single-Line Text (.NET)

A single-text object is created using the active text style. You can change the formatting of a single-line text object by changing the text style associated with it, or by editing the properties of the single-line text object directly. You _cannot_ apply formats to individual words and characters with single-line text objects. 

To change a text style associated with an individual single-line text object, set the TextStyleId property to a new text style. Once you have changed the text style, you must regenerate the drawing or update the object to see the changes in your drawing. 

In addition to the standard editable properties for entities (color, layer, linetype, and so forth), other properties that you can change on a single-line text object include the following: 

HorizontalMode
    

Specifies the horizontal alignment for the text. 

VerticalMode
    

Specifies the vertical alignment for the text. 

Position
    

Specifies the insertion point for the text. 

Oblique
    

Specifies the oblique angle of the individual text object. 

Rotation
    

Specifies the rotation angle in radians for the text. 

WidthFactor
    

Specifies the scale factor for the text. 

AlignmentPoint
    

Specifies the alignment point for the text. 

IsMirroredInX
    

Specifies whether the text is displayed backwards. 

IsMirroredInY
    

Specifies whether the text is displayed upside-down. 

TextString
    

Specifies the actual text string displayed. 

Once you have changed a property, regenerate the drawing or update the object to see the changes made.
