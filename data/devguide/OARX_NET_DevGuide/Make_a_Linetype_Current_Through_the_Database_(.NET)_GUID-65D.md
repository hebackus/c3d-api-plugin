<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Linetypes (.NET) > Make a Linetype Active (.NET) > Make a Linetype Current Through the Database (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-65DA31BC-0D10-4305-B890-1DF532701B30.htm -->

# Make a Linetype Current Through the Database (.NET)

This example sets a linetype current through the Database object with the Celtype property. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("SetLinetypeCurrent")]
    public static void SetLinetypeCurrent()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Linetype table for read
            LinetypeTable acLineTypTbl;
            acLineTypTbl = acTrans.GetObject(acCurDb.LinetypeTableId,
                                             OpenMode.ForRead) as LinetypeTable;
    
            string sLineTypName = "Center";
    
            if (acLineTypTbl.Has(sLineTypName) == true)
            {
                // Set the linetype Center current
                acCurDb.Celtype = acLineTypTbl[sLineTypName];
    
                // Save the changes
                acTrans.Commit();
            }
    
            // Dispose of the transaction
        }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("SetLinetypeCurrent")> _
    Public Sub SetLinetypeCurrent()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Linetype table for read
            Dim acLineTypTbl As LinetypeTable
            acLineTypTbl = acTrans.GetObject(acCurDb.LinetypeTableId, _
                                             OpenMode.ForRead)
    
            Dim sLineTypName As String = "Center"
    
            If acLineTypTbl.Has(sLineTypName) = True Then
                '' Set the linetype Center current
                acCurDb.Celtype = acLineTypTbl(sLineTypName)
    
                '' Save the changes
                acTrans.Commit()
            End If
    
            '' Dispose of the transaction
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    ThisDrawing.ActiveLinetype = ThisDrawing.Linetypes.Item("Center")
