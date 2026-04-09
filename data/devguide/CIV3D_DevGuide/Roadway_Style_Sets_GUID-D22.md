<!-- Developer's Guide > API Developer's Guide > Corridors > Styles > Roadway Style Sets -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D22CE6F9-6D8C-4E08-956F-50270363D3CA.htm -->

# Roadway Style Sets

The visual display of applied assemblies is defined by roadway style sets, which are a set of shape styles and link styles assigned to shapes and links that use specified code strings. The collection of all style sets are found in the CivilDocument.Styles.CodeSetStyles property. A style set is itself a collection of CodeSetStyleItem objects. Each style set item has a CodeSetStyleItem.CodeStyle property that can reference either an existing shape style object or link shape object. New style set items are added to a style set though the CodeSetStyleCollection.Add() method which takes parameters describing the kind of style object, the code string, and the style object itself.

Note:

You cannot set the CodeSetStyle to be the currently used style with the .NET API. However, you can get the ObjectId for the currently used style by calling CodeSetStyle.GetCurrentStyleSetId().
    
    
    // Create a new style set using our previously created styles.
    objId = doc.Styles.ShapeStyles.Add("Style Set 1");
    CodeSetStyle oCodeSetStyle = ts.GetObject(objId, OpenMode.ForWrite) as CodeSetStyle;
    oCodeSetStyle.Add("TOP", doc.Styles.LinkStyles["Style2"]);
    oCodeSetStyle.Add("BASE", doc.Styles.ShapeStyles["Style3"]);
     
    ts.Commit();
