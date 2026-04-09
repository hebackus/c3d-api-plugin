<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Work With Text Styles (.NET) > Substitute Fonts (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B2E279E6-B80A-4430-AEA0-4A8D3828BCB7.htm -->

# Substitute Fonts (.NET)

You can designate fonts to be substituted for other fonts or as defaults when AutoCAD cannot find a font specified in a drawing. 

The fonts used for the text in your drawing are determined by the text style and, for MText, by individual font formats applied to sections of text. 

You can use font mapping tables to ensure that your drawing uses only certain fonts, or to convert the fonts you used to other fonts. You can use these font mapping tables to enforce corporate font standards, or to facilitate offline printing. AutoCAD comes with a default font mapping table. You can edit this file using any ASCII text editor. You also can specify a different font mapping table file by using the FONTMAP system variable. 

## Specify an Alternative Default Font

If your drawing specifies a font that is not currently on your system, AutoCAD automatically substitutes the font designated as your alternate font. By default, AutoCAD uses the _simplex.shx_ file. However, you can specify a different font if necessary. Use the FONTALT system variable to set the alternative font file name. 

If you use a text style that uses a Big Font, you can map it to another font using the FONTALT system variable. The font mapping must be done in pairs of font files: _txt.shx_ , _bigfont.shx_. 

If AutoCAD cannot find a font file when a drawing is opened, it applies a default set of font substitution rules.
