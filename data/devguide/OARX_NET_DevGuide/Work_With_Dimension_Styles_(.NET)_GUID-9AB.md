<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Work With Dimension Styles (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9ABB8370-38D0-4246-A5A5-65E527EDDFD1.htm -->

# Work With Dimension Styles (.NET)

A named dimension style is a group of settings that determines the appearance of a dimension. Using named dimension styles, you can establish and enforce drafting standards for the dimensions in a drawing. 

All dimensions are created using the active dimension style. If you do not define or apply a style before creating dimensions, AutoCAD applies the default style, STANDARD. To set the active dimension style, use the Dimstyle property of the current database. 

To set up a dimension style, you begin by naming and saving a style. The new style is based on the current style and includes all the settings that define the parts of the dimensions, the positioning of text, and the appearance of annotation. Annotation in this case means primary and alternate units, tolerances, and text.
