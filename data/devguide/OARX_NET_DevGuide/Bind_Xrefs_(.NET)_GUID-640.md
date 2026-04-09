<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use External References (.NET) > Bind Xrefs (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-640D3814-6258-4DCF-8407-FE58B5DB5D9C.htm -->

# Bind Xrefs (.NET)

Binding an xref to a drawing using the Bind method makes the xref a permanent part of the drawing and no longer an externally referenced file. The externally referenced information becomes a block. When the externally referenced drawing is updated, the bound xref is not updated. This process binds the entire drawing's database, including all of its dependent symbols. 

Dependent symbols are named objects such as blocks, dimension styles, layers, linetypes, and text styles. Binding the xref allows named objects from the xref to be used in the current drawing. 

The BindXref method requires two parameters: xrefIds (collection of ObjectIDs) and insertBind (boolean). If the insertBind parameter is set to True, the symbol names of the xref drawing are prefixed in the current drawing with _< blockname>$x$_, where _x_ is an integer that is automatically incremented to avoid overriding existing block definitions. If the insertBind parameter is set to False, the symbol names of the xref drawing are merged into the current drawing without the prefix. If duplicate names exist, AutoCAD uses the symbols already defined in the local drawing. If you are unsure whether your drawing contains duplicate symbol names, it is recommended that you set insertBind to True. 

For more information on binding xrefs, see “About Archiving Drawings with Xrefs (Binding)” in the product Help system. 

## Bind an xref definition

This example attaches an external reference and then binds the external -reference to the drawing. This example uses the _Exterior Elevations.dwg_ file found in the _Sample_ directory. If you do not have this image, or if it is located in a different directory, insert a valid path and file name. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("BindingExternalReference")]
    public void BindingExternalReference()
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
    
                    acCurDb.BindXrefs(acXrefIdCol, false);
                }
    
                Application.ShowAlertDialog("The external reference is bound.");
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
    
    <CommandMethod("BindingExternalReference")> _
    Public Sub BindingExternalReference()
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
     
                    acCurDb.BindXrefs(acXrefIdCol, False)
                End Using
    
                MsgBox("The external reference is bound.")
            End If
    
            ' Save the new objects to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub BindingExternalReference()
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
     
        ' Bind the external reference definition
        ThisDrawing.Blocks.Item(xrefInserted.name).Bind False
        MsgBox "The external reference is bound."
    End Sub
