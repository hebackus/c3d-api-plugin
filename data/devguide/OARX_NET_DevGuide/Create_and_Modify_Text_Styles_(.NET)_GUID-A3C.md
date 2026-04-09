<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Work With Text Styles (.NET) > Create and Modify Text Styles (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A3CA7191-A979-4FD4-8322-357C27180BB6.htm -->

# Create and Modify Text Styles (.NET)

New text inherits height, width factor, obliquing angle, and text generation properties from the current text style. To create a text style, create a new instance of a TextStyleTableRecord object. Assign the new text style a name using the Name property. Then open the TextStyleTable object for write and use the Add method to create the new text style. 

Style names can contain letters, numbers, and the special characters dollar sign ($), underscore (_), and hyphen (-). AutoCAD converts the characters to uppercase. If you do not enter a style name, the new style will not have a name. 

You can modify an existing style by changing the properties of the TextStyleTableRecord object. If you want to work with the current text style, use the TextStyle property of the Database object which holds the object id of the current text style. 

You can also update existing text of that style type to reflect the changes. Use the following properties to modify a TextStyleTableRecord object: 

BigFontFileName
    

Specifies the special shape definition file used for a non-ASCII character set. 

FileName
    

Specifies the file associated with a font (character style). 

FlagBits
    

Specifies backward text, upside-down text, or both. 

Font
    

Specifies the typeface, bold, italic, character set, and pitch and family settings of the text style. 

IsVertical
    

Specifies vertical or horizontal text. 

ObliquingAngle
    

Specifies the slant of the characters. 

TextSize
    

Specifies the character height. 

XScale
    

Specifies the expansion or compression of the characters. 

If you change an existing style's font or orientation, all text using that style is changed to use the new font or orientation. Changing text height, width factor, and oblique angle does not change existing text but does change subsequently created text objects. 

Note: The drawing must be regenerated to see any changes to the above properties.
