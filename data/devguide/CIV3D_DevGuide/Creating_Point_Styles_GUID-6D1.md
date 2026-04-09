<!-- Developer's Guide > API Developer's Guide > Points > Point Style > Creating Point Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6D1BC307-1824-4B66-9B62-8C7AECB130DC.htm -->

# Creating Point Styles

A point style is a group of settings that define how a point is drawn. These settings include marker style, marker color and line type, and label color and line type. Point objects can use any of the point styles that are currently stored in the document. Styles are assigned to a point through the point’s CogotPoint.StyleId property. Existing point styles are stored in the document’s CivilDocument.Styles.PointStyles collection. 

You can also create custom styles and add them to the document’s collection of point styles. First, add a new style to the document’s list of styles using the CivilDocument.Styles.PointStyles.Add() method. This method returns the ObjectId of a new style object that is set with all the properties of the default style. You can then make the changes to the style object you require. 

The display settings for PointStyle objects are accessed with the style’s GetDisplay*(), GetLabelDisplay*() and GetMarkerDisplay*() methods for the view mode (Model, Plan, Profile or Section) for the style. 

The point marker type is set by the PointStyle’s MarkerType property, and can be a symbol, custom marker, or an AutoCAD point style. Custom markers are set using the CustomMarkerStyle and CustomMarkersuperimposeStyle properties. Symbol markers are set using the MarkerSymbolName property, which is a string that names an AutoCAD BLOCK symbol in the drawing. 

Points assigned to PointGroups may have their styles overridden by the PointGroup. You can check the overridden style ID using the LabelStyleIdOverride and StyleIdOverride properties. 

This sample creates a new points style, adjusts the style settings, and the assigns the style to point “cogoPoint1”: 
    
    
    // Create a point style that uses a custom marker,
    // a Plus sign inside a square.
    ObjectId pointStyleId = _civildoc.Styles.PointStyles.Add("Example Point Style");
    PointStyle pointStyle = pointStyleId.GetObject(OpenMode.ForWrite) as PointStyle;
    pointStyle.MarkerType = PointMarkerDisplayType.UseCustomMarker;
    pointStyle.CustomMarkerStyle = CustomMarkerType.CustomMarkerPlus;
    pointStyle.CustomMarkerSuperimposeStyle = CustomMarkerSuperimposeType.Square;
    
    // Assign the style to a point object.
    cogoPoint1.StyleId = pointStyleId;
