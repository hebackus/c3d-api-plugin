<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Styles > Roadway Style Sets -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9064AAB9-9708-431D-A96B-A49F007E9DE6.htm -->

# Roadway Style Sets

The visual display of applied assemblies is defined by roadway style sets, which are a set of shape styles and link styles assigned to shapes and links that use specified code strings. The collection of all style sets are found in the AeccRoadwayDocument.StyleSets property. A style set is itself a collection of AeccRoadwayStyleSetItem objects. Each style set item has a AeccRoadwayStyleSetItem.CodeStyle property that can reference either an existing shape style object or link shape object. New style set items are added to a style set though the AeccRoadwayStyleSet.Add method which takes parameters describing the kind of style object, the code string, and the style object itself. The particular style set in use is selected through the AeccRoadwayStyleSet.InitAsCurrent method.
    
    
    ' Create a new style set using our previously created styles.
    Dim oStyleSet As AeccRoadwayStyleSet
    Set oStyleSet = oRoadwayDocument.StyleSets.Add("Style Set 01")
    Call oStyleSet.Add( _
       aeccLinkType, _
       "TOP", _
       g_oRoadwayDocument.LinkStyles.Item("Style2"))
    Call oStyleSet.Add( _
       aeccShapeType, _
       "BASE", _
       oRoadwayDocument.ShapeStyles.Item("Style3"))
     
    ' Assign our new style set as the style set in current use.
    oStyleSet.InitAsCurrent
