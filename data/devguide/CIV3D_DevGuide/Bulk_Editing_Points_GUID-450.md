<!-- Developer's Guide > API Developer's Guide > Points > Using Points > Bulk Editing Points -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-45038B51-099C-41FD-B643-D5D81BE7EA07.htm -->

# Bulk Editing Points

The CogoPointCollection class provides several methods for changing the properties of multiple points with a single action. Most of the Set<Property>() methods have three versions: 

  1. Set the property for a single CogoPoint (identified by ObjectId) in the collection . 
  2. Set the property for all points in a list to a single value . 
  3. Set the property for all points in a list to a value in a corresponding list of values. 

The list of points can be a sub-collection of points, or you can pass the CivilDocument.CogoPoints collection to process all points in the document. 

Here is an example of setting Elevation, RawDescription and DescriptionFormat properties for all points in the drawing using the bulk editing methods. 
    
    
    // Change a couple of properties using bulk editing methods
    cogoPoints.SetElevationByOffset(cogoPoints, 3.00);
    cogoPoints.SetRawDescription(cogoPoints, "NEW_DESC");
    // Sets Full Description = Raw Description:
    cogoPoints.SetDescriptionFormat(cogoPoints, "$*");
