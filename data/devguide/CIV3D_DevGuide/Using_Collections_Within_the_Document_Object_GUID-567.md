<!-- Developer's Guide > API Developer's Guide > Root Objects and Common Concepts > Root Objects > Using Collections Within the Document Object -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5676A992-E881-4467-A1A7-4412425B5F36.htm -->

# Using Collections Within the Document Object

The document object not only contains collections of Autodesk Civil 3D drawing elements (such as points and alignments) but also objects that modify those elements (such as styles and label styles). Collections in CivilDocument are ObjectID collections (Autodesk.AutoCAD.DatabaseServices.ObjectIdCollection) for most objects. Objects in these collections must be retrieved with a Transaction.GetObject(), and cast to their type before they can be used. 

Note:

In the COM API, document objects are contained in collections of objects that do not need to be cast. 

ObjectIdCollection objects implement the IList interface, and can be enumerated or accessed by index. Here’s an example of iterating through the Corridor collection with foreach, and retrieving and casting the resulting ObjectId to a Corridor to access its methods and properties: 
    
    
    public static void iterateCorridors () {
        CivilDocument doc = CivilApplication.ActiveDocument;
        using ( Transaction ts = Application.DocumentManager.MdiActiveDocument.
                Database.TransactionManager.StartTransaction() ) {
            foreach ( ObjectId objId in doc.CorridorCollection ) {
                Corridor oCorridor = ts.GetObject(objId, OpenMode.ForRead) as Corridor;
                Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("Corridor: {0}\nLargest possible triangle side: {1}\n",
                    oCorridor.Name, oCorridor.MaximumTriangleSideLength);
            }
        }
    }
    

For more information about ObjectIdCollections, see the Civil 3D .NET API Reference. 

This example creates a new point style: 
    
    
    ObjectId pointStyleID = doc.Styles.PointStyles.Add("Name");
    // Now a new point style is added to the collection of styles,
    // and we can modify it by setting the properties
    // of the oPointStyle object, which we get from the Transaction ts:
    PointStyle oPointStyle = ts.GetObject(pointStyleID, OpenMode.ForWrite) as PointStyle;
    oPointStyle.Elevation = 114.6;
    // You must commit the transaction for the add / modify operation
    // to take effect
    ts.Commit();
    

If you attempt to add a new element with properties that match an already existing element, try to access an item that does not exist, or remove an item that does not exist or is in use, an error will result. You should trap the error and respond accordingly. 

The following sample demonstrates one method of dealing with such errors: 
    
    
    // Try to access the style named "Name"
    try {
        // This raises an ArgumentException if the item doesn't
        // exist:
        ObjectId pointStyleId = doc.Styles.PointStyles["Name"];
        // do something with the point style...
    } catch ( ArgumentException e ) {
        ed.WriteMessage(e.Message);
    }
