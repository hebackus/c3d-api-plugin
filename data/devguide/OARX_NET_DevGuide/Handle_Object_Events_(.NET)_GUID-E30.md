<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Register and Unregister Events (.NET) > Handle Object Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E30279D1-E4B5-48A4-A3D8-9CEC83BD0967.htm -->

# Handle Object Events (.NET)

Object events are used to respond to the opening, adding, modifying, and erasing of objects from a drawing database. There are two types of object related events: object and database level. Object level events are defined to respond to a specific object in a database, whereas Database level events respond to all objects in a database. 

You define an object level event by registering an event handler with the event of a database object. Database level object events are defined by registering an event handler with one of the events of an open Database object. 

The following events are available for DBObjects: 

Cancelled
    

Triggered when the opening of the object is cancelled text. 

Copied
    

Triggered after the object is cloned. 

Erased
    

Triggered when the object is flagged to be erased or is unerased. 

Goodbye
    

Triggered when the object is about to be deleted from memory because its associated database is being destroyed. 

Modified
    

Triggered when the object is modified. 

ModifiedXData
    

Triggered when the XData attached to the object is modified. 

ModifyUndone
    

Triggered when previous changes to the object are being undone. 

ObjectClosed
    

Triggered when the object is closed. 

OpenedForModify
    

Triggered before the object is modified. 

Reappended
    

Triggered when the object is removed from the database after an Undo operation and then re-appended with a Redo operation. 

SubObjectModified
    

Triggered when a subobject of the object is modified. 

Unappended
    

Triggered when the object is removed from the database after an Undo operation. 

The following are some of the events used to respond to object changes at the Database level: 

ObjectAppended
    

Triggered when an object is added to a database. 

ObjectErased
    

Triggered when an object is erased or unerased from a database. 

ObjectModified
    

Triggered when an object has been modified. 

ObjectOpenedForModify
    

Triggered before an object is modified. 

ObjectReappended
    

Triggered when an object is removed from a database after an Undo operation and then re-appended with a Redo operation. 

ObjectUnappended
    

Triggered when an object is removed from a database after an Undo operation. 

## Enable an Object event

This example creates a lightweight polyline with events. The event handler for the polyline then displays the new area whenever the polyline is changed. To trigger the event, simply change the size of the polyline in AutoCAD. Remember that you must run the CreatePLineWithEvents subroutine before the event handler is activated. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    // Global variable for polyline object
    Polyline acPoly = null;
     
    [CommandMethod("AddPlObjEvent")]
    public void AddPlObjEvent()
    {
      // Get the current document and database, and start a transaction
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
      Database acCurDb = acDoc.Database;
     
      using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
      {
          // Open the Block table record for read
          BlockTable acBlkTbl;
          acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                       OpenMode.ForRead) as BlockTable;
     
          // Open the Block table record Model space for write
          BlockTableRecord acBlkTblRec;
          acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                          OpenMode.ForWrite) as BlockTableRecord;
     
          // Create a closed polyline
          acPoly = new Polyline();
          acPoly.AddVertexAt(0, new Point2d(1, 1), 0, 0, 0);
          acPoly.AddVertexAt(1, new Point2d(1, 2), 0, 0, 0);
          acPoly.AddVertexAt(2, new Point2d(2, 2), 0, 0, 0);
          acPoly.AddVertexAt(3, new Point2d(3, 3), 0, 0, 0);
          acPoly.AddVertexAt(4, new Point2d(3, 2), 0, 0, 0);
          acPoly.Closed = true;
     
          // Add the new object to the block table record and the transaction
          acBlkTblRec.AppendEntity(acPoly);
          acTrans.AddNewlyCreatedDBObject(acPoly, true);
     
          acPoly.Modified += new EventHandler(acPolyMod);
     
          // Save the new object to the database
          acTrans.Commit();
      }
    }
     
    [CommandMethod("RemovePlObjEvent")]
    public void RemovePlObjEvent()
    {
      if (acPoly != null)
      {
          // Get the current document and database, and start a transaction
          Document acDoc = Application.DocumentManager.MdiActiveDocument;
          Database acCurDb = acDoc.Database;
     
          using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
          {
              // Open the polyline for read
              acPoly = acTrans.GetObject(acPoly.ObjectId,
                                         OpenMode.ForRead) as Polyline;
     
              if (acPoly.IsWriteEnabled == false)
              {
                  acTrans.GetObject(acPoly.ObjectId, OpenMode.ForWrite);
              }
     
              acPoly.Modified -= new EventHandler(acPolyMod);
              acPoly = null;
          }
      }
    }
     
    public void acPolyMod(object senderObj,
                          EventArgs evtArgs)
    {
      Application.ShowAlertDialog("The area of " +
                                  acPoly.ToString() + " is: " +
                                  acPoly.Area);
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    '' Global variable for polyline object
    Dim acPoly As Polyline = Nothing
     
    <CommandMethod("AddPlObjEvent")> _
    Public Sub AddPlObjEvent()
      '' Get the current document and database, and start a transaction
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
      Dim acCurDb As Database = acDoc.Database
     
      Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
          '' Open the Block table record for read
          Dim acBlkTbl As BlockTable
          acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                       OpenMode.ForRead)
     
          '' Open the Block table record Model space for write
          Dim acBlkTblRec As BlockTableRecord
          acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                          OpenMode.ForWrite)
     
          '' Create a closed polyline
          acPoly = New Polyline()
          acPoly.AddVertexAt(0, New Point2d(1, 1), 0, 0, 0)
          acPoly.AddVertexAt(1, New Point2d(1, 2), 0, 0, 0)
          acPoly.AddVertexAt(2, New Point2d(2, 2), 0, 0, 0)
          acPoly.AddVertexAt(3, New Point2d(3, 3), 0, 0, 0)
          acPoly.AddVertexAt(4, New Point2d(3, 2), 0, 0, 0)
          acPoly.Closed = True
     
          '' Add the new object to the block table record and the transaction
          acBlkTblRec.AppendEntity(acPoly)
          acTrans.AddNewlyCreatedDBObject(acPoly, True)
     
          AddHandler acPoly.Modified, AddressOf acPolyMod
     
          '' Save the new object to the database
          acTrans.Commit()
      End Using
    End Sub
     
    <CommandMethod("RemovePlObjEvent")> _
    Public Sub RemovePlObjEvent()
      If acPoly <> Nothing Then
          '' Get the current document and database, and start a transaction
          Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
          Dim acCurDb As Database = acDoc.Database
     
          Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
              '' Open the polyline for read
              acPoly = acTrans.GetObject(acPoly.ObjectId, _
                                         OpenMode.ForRead)
     
              If acPoly.IsWriteEnabled = False Then
                  acTrans.GetObject(acPoly.ObjectId, OpenMode.ForWrite)
              End If
     
              RemoveHandler acPoly.Modified, AddressOf acPolyMod
              acPoly = Nothing
          End Using
      End If
    End Sub
     
    Public Sub acPolyMod(ByVal senderObj As Object, _
                         ByVal evtArgs As EventArgs)
      Application.ShowAlertDialog("The area of " & _
                                  acPoly.ToString() & " is: " & _
                                  acPoly.Area)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Public WithEvents PLine As AcadLWPolyline
    
    Sub CreatePLineWithEvents()
        ' This example creates a light weight polyline
        Dim points(0 To 9) As Double
        points(0) = 1: points(1) = 1
        points(2) = 1: points(3) = 2
        points(4) = 2: points(5) = 2
        points(6) = 3: points(7) = 3
        points(8) = 3: points(9) = 2
     
        Set PLine = ThisDrawing.ModelSpace. _
        AddLightWeightPolyline(points)
        PLine.Closed = True
     
        ThisDrawing.Application.ZoomAll
    End Sub
    
    Private Sub PLine_Modified _
     (ByVal pObject As AutoCAD.IAcadObject)
        ' This event is triggered when the polyline is resized.
        ' If the polyline is deleted the modified event is still
        ' triggered, so we use the error handler to avoid
        ' reading data from a deleted object.
     
        On Error GoTo ERRORHANDLER
        MsgBox "The area of " & pObject.ObjectName & " is: " _
        & pObject.Area
        Exit Sub
     
    ERRORHANDLER:
        MsgBox Err.Description
    End Sub
