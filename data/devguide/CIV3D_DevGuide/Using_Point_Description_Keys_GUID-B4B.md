<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Style > Using Point Description Keys -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B4B8FE05-2F6A-4605-B752-2944C3A0C332.htm -->

# Using Point Description Keys

Point description keys are a method for attaching style, label style, and orientation to point locations in a drawing - possibly imported from a text file which lacks such information. Keys are objects of type AeccPointDescriptionKey. The AeccPointDescriptionKey.Name property is a pattern matching code. If any new points are created with a description that matches the name of an existing key, the point is assigned all the settings of that key. 

The wildcards “?” and “*” are allowed in the name. Keys can contain either constant scale or rotation values for points or can assign orientation values depending on parameters passed through the description string. Point description keys are held in sets, objects of type AeccPointDescriptionKeySet. The collection of all sets in a document are held in the document’s AeccDocument.PointDescriptionKeySets property.
    
    
    ' Create a key set in the document's collection
    ' of sets.
    Dim oPointDescriptionKeySet As AeccPointDescriptionKeySet
    Set oPointDescriptionKeySet = _
      oDocument.PointDescriptionKeySets.Add("Sample Key Set")
     
    ' Create a new key in the set we just made. Match with
    ' any description beginning with "SMP".
    Dim oPointDescriptionKey As AeccPointDescriptionKey
    Set oPointDescriptionKey = oPointDescriptionKeySet.Add("SAMP*")
     
    ' Assign chosen styles and label styles to the key.
    oPointDescriptionKey.PointStyle = oPointStyle
    oPointDescriptionKey.OverridePointStyle = True
    oPointDescriptionKey.PointLabelStyle = oLabelStyle
    oPointDescriptionKey.OverridePointLabelStyle = True
     
    ' Turn off the scale override, and instead scale
    ' to whatever is passed as the first parameter.
    oPointDescriptionKey.OverrideScaleParameter = False
    oPointDescriptionKey.UseDrawingScale = False
    oPointDescriptionKey.ScaleParameter = 1
    oPointDescriptionKey.ScaleXY = True
     
    ' And turn on the rotation override, and rotate
    ' all points using this key 45 degrees clockwise.
    oPointDescriptionKey.OverrideFixedRotation = True
    oPointDescriptionKey.FixedRotation = 0.785398163 ' radians
    oPointDescriptionKey.ClockwiseRotation = True
    

The following is the contents of a text file in “PENZD (comma delimited)” format with point information, a description, and parameter. This creates two points using the previously defined SAMP* description key, resulting in point markers four times normal size.
    
    
    2000,3700.0,4900.0,150.0,SAMPLE 4
    2001,3750.0,4950.0,150.0,SAMPLE 4
    

When a text file is loaded using Points.ImportPoints, the first alphanumeric element in a point’s description is compared to the names of all point description keys. If a match is found, the point’s settings are adjusted to match the description key. Any parameters to pass to the key are added after the description, separated by spaces. If using parameters, use a comma delimited file format or else any parameters will be ignored. This process only takes place when points are read from a file - after a point is created, setting the AeccPoint.RawDescription property does nothing to change the point’s style.
