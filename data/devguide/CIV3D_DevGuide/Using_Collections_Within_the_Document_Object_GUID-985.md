<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Root Objects and Common Concepts in COM > Root Objects > Using Collections Within the Document Object -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9853070A-8B0A-4C71-B772-5165F1C1DDD1.htm -->

# Using Collections Within the Document Object

The document object not only contains collections of all Autodesk Civil 3D drawing elements (such as surfaces and alignments) but all objects that modify those elements (such as styles and label styles). These collections have the same core set of methods: Count, Item, Remove, and Add. Count represents the number of items in the collection. Item returns an object from the collection, usually specified by the identification number or the name for the object. Remove deletes a specified item from the collection. Add creates a new item, adds it to the collection, and returns a reference to the newly created item. This item is already set with default values as defined by the document ambient settings.

This example creates a new point style:
    
    
    Dim oPointStyle As AeccPointStyle
    Set oPointStyle = oAeccDocument.PointStyles.Add("Name")
    ' Now a new point style is added to the collection of styles,
    ' and we can modify it by setting the properties
    ' of the oPointStyle object.
    oPointStyle.Elevation = 114.6
    

If you attempt to add a new element with properties that match an already existing element, try to access an item that does not exist, or remove an item that does not exist or is in use, an error will result. You should trap the error and respond accordingly. 

The following sample demonstrates one method of dealing with such errors:
    
    
    ' Try to access the style named "Name".
    Dim oPointStyle As AeccPointStyle
    On Error Resume Next
    Set oPointStyle = oAeccDocument.PointStyles.Item("Name")
    ' Turn off error handling as soon as we no longer need it.
    On Error Goto 0
     
    ' If there was a problem retrieving the item, then
    ' the oPointStyle object will remain empty. Check if that
    ' is the case. If so, it is most likely because the item
    ' does not exist. Try making a new one.
    If (oPointStyle Is Nothing) Then
        Set oPointStyle = oAeccDocument.PointStyles.Add("Name")
    End If
