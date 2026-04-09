<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use External References (.NET) > Detach Xrefs (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DEAD46A2-BC5B-4313-B84B-AB2B62D66DB2.htm -->

# Detach Xrefs (.NET)

You can detach an xref definition to remove the xrefs completely from your drawing. You can also erase the individual xref instances. Detaching the xref definition removes all dependent symbols associated with that xref. If all the instances of an xref are erased from the drawing, AutoCAD removes the xref definition the next time the drawing is opened. 

To detach an xref, use the DetachXref method. You cannot detach a nested xref. 

## Detach an xref definition

This example attaches an external reference and then detaches the external reference. This example uses the _Exterior Elevations.dwg_ file found in the _Sample_ directory. If you do not have this image, or if it is located in a different directory, insert a valid path and file name. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("DetachingExternalReference")]
    public void DetachingExternalReference()
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
    
                acCurDb.DetachXref(acXrefId);
    
                Application.ShowAlertDialog("The external reference is detached.");
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
    
    <CommandMethod("DetachingExternalReference")> _
    Public Sub DetachingExternalReference()
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
    
                acCurDb.DetachXref(acXrefId)
    
                MsgBox("The external reference is detached.")
            End If
    
            ' Save the new objects to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub DetachingExternalReference()
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
     
        ' Detach the external reference definition
        Dim name As String
        name = xrefInserted.name
        ThisDrawing.Blocks.Item(name).Detach
        MsgBox "The external reference is detached."
    End Sub
