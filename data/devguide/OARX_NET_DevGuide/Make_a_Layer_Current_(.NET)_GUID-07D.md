<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Make a Layer Current (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-07DDED83-4D27-4A5F-B411-25BF4F5E76D4.htm -->

# Make a Layer Current (.NET)

You are always drawing on the active layer. When you make a layer active, you create new objects on that layer. If you make a different layer active, any new objects you create is assigned that new active layer and uses its color and linetype. You cannot make a layer active if it is frozen. 

To make a layer active, use the Clayer property of the Database object or the CLAYER system variable. For example: 

## Make a layer current through the database 

This example sets a layer current through the Database object with the Clayer property. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("SetLayerCurrent")]
    public static void SetLayerCurrent()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Layer table for read
            LayerTable acLyrTbl;
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                         OpenMode.ForRead) as LayerTable;
    
            string sLayerName = "Center";
    
            if (acLyrTbl.Has(sLayerName) == true)
            {
                // Set the layer Center current
                acCurDb.Clayer = acLyrTbl[sLayerName];
    
                // Save the changes
                acTrans.Commit();
            }
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("SetLayerCurrent")> _
    Public Sub SetLayerCurrent()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Layer table for read
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                         OpenMode.ForRead)
    
            Dim sLayerName As String = "Center"
    
            If acLyrTbl.Has(sLayerName) = True Then
                '' Set the layer Center current
                acCurDb.Clayer = acLyrTbl(sLayerName)
    
                '' Save the changes
                acTrans.Commit()
            End If
    
            '' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    ThisDrawing.ActiveLayer = ThisDrawing.Layers("Center")

## Make a layer current with the CLAYER system variable 

This example sets a layer current with the CLAYER system variable. 

### C#
    
    
    Application.SetSystemVariable("CLAYER", "Center");

### VB.NET
    
    
    Application.SetSystemVariable("CLAYER", "Center")

### VBA/ActiveX Code Reference
    
    
    ThisDrawing.SetVariable "CLAYER", "Center"
