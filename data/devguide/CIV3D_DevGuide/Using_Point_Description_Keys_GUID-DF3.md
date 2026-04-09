<!-- Developer's Guide > API Developer's Guide > Points > Point Style > Using Point Description Keys -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DF32D012-5B57-4DED-BF76-51B42771BDB8.htm -->

# Using Point Description Keys

Point description keys are a method for attaching style, label style, and orientation to point locations in a drawing - possibly imported from a text file which lacks such information. Keys are objects of type PointDescriptionKey. The PointDescriptionKey.Code property is a pattern matching code. If any new points are created with a description that matches the code of an existing key, the point is assigned all the settings of that key. 

The wildcards “?” and “*” are allowed in the code. Keys can contain either constant scale or rotation values for points or can assign orientation values depending on parameters passed through the description string. Point description keys are held in sets, objects of type PointDescriptionKeySet. The collection of all sets in a document are accessed with the PointDescriptionKeySetCollection.GetPointDescriptionKeySets() static method. 

The collection of all key sets also exposes a SearchOrder property, which lets you specify the order that key sets are searched for matches when description keys are applied. Key sets at the beginning of the SearchOrder collection are searched first and therefore have higher priority. In the example below, this property is accessed, and the last item is moved to the first position. 
    
    
    // Create a Key Set in the collection of all Key Sets:
    ObjectId pointDescriptionKeySetId = 
      PointDescriptionKeySetCollection.GetPointDescriptionKeySets(_acaddoc.Database).Add("Example Key Set");
    PointDescriptionKeySet pointDescriptionKeySet = 
      pointDescriptionKeySetId.GetObject(OpenMode.ForWrite) as PointDescriptionKeySet;
    
    // Create a new key in the set we just made.  Match with any description starting with "GRND".
    ObjectId pointDescriptionKeyId = pointDescriptionKeySet.Add("GRND*");
    PointDescriptionKey pointDescriptionKey =
      pointDescriptionKeyId.GetObject(OpenMode.ForWrite) as PointDescriptionKey;
    
    // Assign chosen styles and label styles to the key
    pointDescriptionKey.StyleId = pointStyleId;
    pointDescriptionKey.ApplyStyleId = true;
    pointDescriptionKey.LabelStyleId = labelStyleId;
    pointDescriptionKey.ApplyLabelStyleId = true;
    
    // Turn off the scale override, and instead scale
    // to whatever is passed as the first parameter
    pointDescriptionKey.ApplyDrawingScale = false;
    pointDescriptionKey.ScaleParameter = 1;
    pointDescriptionKey.ApplyScaleParameter = true;
    pointDescriptionKey.ApplyScaleXY = true;
    
    // Turn off the rotation override and rotate
    // all points using the key 45 degrees clockwise
    pointDescriptionKey.FixedMarkerRotation = 0.785398163; // radians
    pointDescriptionKey.RotationDirection = RotationDirType.Clockwise;
    pointDescriptionKey.ApplyFixedMarkerRotation = true;
    
    // Before applying the description keys, we can set the order the key sets are searched
    // when point description keys are applied.
    // In this example, we take the last item and make it the first.
    ObjectIdCollection pdKeySetIds = 
      PointDescriptionKeySetCollection.GetPointDescriptionKeySets(_acaddoc.Database).SearchOrder;
    ObjectId keySetId = pdKeySetIds[pdKeySetIds.Count-1];
    pdKeySetIds.Remove(keySetId);
    pdKeySetIds.Insert(0, keySetId);                
    PointDescriptionKeySetCollection.GetPointDescriptionKeySets(_acaddoc.Database).SearchOrder = 
      pdKeySetIds;
    
    // Apply to point group
    pointGroup.ApplyDescriptionKeys();
