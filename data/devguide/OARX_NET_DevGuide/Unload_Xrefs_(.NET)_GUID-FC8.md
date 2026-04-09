<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use External References (.NET) > Unload Xrefs (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FC87E6F7-1B67-4537-B155-B59FE226E38A.htm -->

# Unload Xrefs (.NET)

To unload an xref, use the Unload method. When you unload a referenced file that is not being used in the current drawing, the AutoCAD performance is enhanced by not having to read and display unnecessary drawing geometry or symbol table information. The xref geometry and that of any nested xref is not displayed in the current drawing until the xref is reloaded. 

## Unload an xref definition

This example attaches an external reference and then unloads the external reference. This example uses the _Exterior Elevations.dwg_ file found in the _Sample_ directory. If you do not have this image, or if it is located in a different directory, insert a valid path and file name. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("UnloadingExternalReference")]
    public void UnloadingExternalReference()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Create a reference to a DWG file
            string PathName = "C:\\AutoCAD\\Sample\\Sheet Sets\\Architectural\\Res\\Exterior Elevations.dwg";
            ObjectId acXrefId = acCurDb.AttachXref(PathName, "Exterior Elevations");
    
            // If a valid reference is created then continue
            if (!acXrefId.IsNull)
            {
                // Attach the DWG reference to the current space
                Point3d insPt = new Point3d(1, 1, 0);
                using (BlockReference acBlkRef = new BlockReference(insPt, acXrefId))
                {
                    BlockTableRecord acBlkTblRec;
                    acBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
    
                    acBlkTblRec.AppendEntity(acBlkRef);
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, true);
                }
    
                Application.ShowAlertDialog("The external reference is attached.");
    
                using (ObjectIdCollection acXrefIdCol = new ObjectIdCollection())
                {
                    acXrefIdCol.Add(acXrefId);
    
                    acCurDb.UnloadXrefs(acXrefIdCol);
                }
    
                Application.ShowAlertDialog("The external reference is unloaded.");
            }
    
            // Save the new objects to the database
            acTrans.Commit();
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    <CommandMethod("UnloadingExternalReference")> _
    Public Sub UnloadingExternalReference()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Create a reference to a DWG file
            Dim PathName As String = "C:\AutoCAD\Sample\Sheet Sets\Architectural\Res\Exterior Elevations.dwg"
            Dim acXrefId As ObjectId = acCurDb.AttachXref(PathName, "Exterior Elevations")
    
            ' If a valid reference is created then continue
            If Not acXrefId.IsNull Then
                ' Attach the DWG reference to the current space
                Dim insPt As New Point3d(1, 1, 0)
                Using acBlkRef As New BlockReference(insPt, acXrefId)
    
                    Dim acBlkTblRec As BlockTableRecord
                    acBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite)
    
                    acBlkTblRec.AppendEntity(acBlkRef)
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, True)
                End Using
    
                MsgBox("The external reference is attached.")
    
                Using acXrefIdCol As New ObjectIdCollection
                    acXrefIdCol.Add(acXrefId)
    
                    acCurDb.UnloadXrefs(acXrefIdCol)
                End Using
    
                MsgBox("The external reference is unloaded.")
            End If
    
            ' Save the new objects to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub UnloadingExternalReference()
        ' Define external reference to be inserted
        Dim xrefInserted As AcadExternalReference
        Dim insertionPnt(0 To 2) As Double
        Dim PathName As String
        insertionPnt(0) = 1
        insertionPnt(1) = 1
        insertionPnt(2) = 0
        PathName = "C:\AutoCAD\Sample\Sheet Sets\Architectural\Res\Exterior Elevations.dwg"
     
        ' Add the external reference
        Set xrefInserted = ThisDrawing.ActiveLayout.Block. _
            AttachExternalReference(PathName, "Exterior Elevations", insertionPnt, 1, 1, 1, 0, False)
        MsgBox "The external reference is attached."
     
        ' Unload the external reference definition
        ThisDrawing.Blocks.Item(xrefInserted.name).Unload
        MsgBox "The external reference is unloaded."
    End Sub
