<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Linetypes (.NET) > Specify Linetype Scale (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-29F800D2-45BC-4910-8C52-3B7E51BFC577.htm -->

# Specify Linetype Scale (.NET)

You can specify the linetype scale for objects you create. The smaller the scale, the more repetitions of the pattern are generated per drawing unit. By default, AutoCAD uses a global linetype scale of 1.0, which is equal to one drawing unit. You can change the linetype scale for all drawing objects and attribute references. 

The CELTSCALE system variable sets the linetype scale for newly created objects. LTSCALE system variable changes the global linetype scale of existing objects as well as new objects. The LinetypeScale property on an object is used to change the linetype scale for an object. The linetype scale at which an object is displayed at is based on the an individual object’s linetype scale multiplied by the global linetype scale. 

## Change the linetype scale for an object

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("SetObjectLinetypeScale")]
    public static void SetObjectLinetypeScale()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Save the current linetype
            ObjectId acObjId = acCurDb.Celtype;
    
            // Set the global linetype scale
            acCurDb.Ltscale = 3;
    
            // Open the Linetype table for read
            LinetypeTable acLineTypTbl;
            acLineTypTbl = acTrans.GetObject(acCurDb.LinetypeTableId,
                                             OpenMode.ForRead) as LinetypeTable;
    
            string sLineTypName = "Border";
    
            if (acLineTypTbl.Has(sLineTypName) == false)
            {
                acCurDb.LoadLineTypeFile(sLineTypName, "acad.lin");
            }
    
            // Set the Border linetype current
            acCurDb.Celtype = acLineTypTbl[sLineTypName];
    
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a circle object and set its linetype
            // scale to half of full size
            using (Circle acCirc1 = new Circle())
            {
                acCirc1.Center = new Point3d(2, 2, 0);
                acCirc1.Radius = 4;
                acCirc1.LinetypeScale = 0.5;
    
                acBlkTblRec.AppendEntity(acCirc1);
                acTrans.AddNewlyCreatedDBObject(acCirc1, true);
    
                // Create a second circle object
                using (Circle acCirc2 = new Circle())
                {
                    acCirc2.Center = new Point3d(12, 2, 0);
                    acCirc2.Radius = 4;
    
                    acBlkTblRec.AppendEntity(acCirc2);
                    acTrans.AddNewlyCreatedDBObject(acCirc2, true);
                }
            }
    
            // Restore the original active linetype
            acCurDb.Celtype = acObjId;
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("SetObjectLinetypeScale")> _
    Public Sub SetObjectLinetypeScale()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Save the current linetype
            Dim acObjId As ObjectId = acCurDb.Celtype
    
            '' Set the global linetype scale
            acCurDb.Ltscale = 3
    
            '' Open the Linetype table for read
            Dim acLineTypTbl As LinetypeTable
            acLineTypTbl = acTrans.GetObject(acCurDb.LinetypeTableId, _
                                             OpenMode.ForRead)
    
            Dim sLineTypName As String = "Border"
    
            If acLineTypTbl.Has(sLineTypName) = False Then
                acCurDb.LoadLineTypeFile(sLineTypName, "acad.lin")
            End If
    
            '' Set the Border linetype current
            acCurDb.Celtype = acLineTypTbl(sLineTypName)
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle object and set its linetype
            '' scale to half of full size
            Using acCirc1 As Circle = New Circle()
                acCirc1.Center = New Point3d(2, 2, 0)
                acCirc1.Radius = 4
                acCirc1.LinetypeScale = 0.5
    
                acBlkTblRec.AppendEntity(acCirc1)
                acTrans.AddNewlyCreatedDBObject(acCirc1, True)
    
                '' Create a second circle object
                Using acCirc2 As Circle = New Circle()
                    acCirc2.Center = New Point3d(12, 2, 0)
                    acCirc2.Radius = 4
    
                    acBlkTblRec.AppendEntity(acCirc2)
                    acTrans.AddNewlyCreatedDBObject(acCirc2, True)
                End Using
            End Using
    
            '' Restore the original active linetype
            acCurDb.Celtype = acObjId
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SetObjectLinetypeScale()
        ' Save the current linetype
        Dim currLineType As AcadLineType
        Set currLineType = ThisDrawing.ActiveLinetype
     
        ' Set global linetype scale
        ThisDrawing.SetVariable "LTSCALE", 3
     
        ' Load the Border linetype
        On Error Resume Next
        If Not IsObject(ThisDrawing.Linetypes.Item("Border")) Then
          ThisDrawing.Linetypes.Load "Border", "acad.lin"
        End If
     
        ThisDrawing.ActiveLinetype = ThisDrawing.Linetypes.Item("BORDER")
     
        ' Create a circle object in model space
        Dim center(0 To 2) As Double
        center(0) = 2: center(1) = 2: center(2) = 0
     
        Dim circleObj1 As AcadCircle
        Set circleObj1 = ThisDrawing.ModelSpace.AddCircle(center, 4)
     
        ' Set the linetype scale of the circle to half of full size
        circleObj1.LinetypeScale = 0.5
        circleObj1.Update
     
        Dim circleObj2 As AcadCircle
        center(0) = center(0) + 10
        Set circleObj2 = ThisDrawing.ModelSpace.AddCircle(center, 4)
        circleObj2.Update
     
        ' Restore original active linetype
        ThisDrawing.ActiveLinetype = currLineType
    End Sub
