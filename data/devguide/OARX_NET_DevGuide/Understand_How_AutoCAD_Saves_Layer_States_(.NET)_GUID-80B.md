<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Save and Restore Layer States (.NET) > Understand How AutoCAD Saves Layer States (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-80B3DAD6-B1F6-4BCC-86C7-7FA2444EEDFB.htm -->

# Understand How AutoCAD Saves Layer States (.NET)

AutoCAD saves layer setting information in an extension dictionary of the LayerTable object. When you first save a layer state, AutoCAD does the following: 

  * Creates an extension dictionary on the Layers table. 
  * Creates a Dictionary object named ACAD_LAYERSTATE in the extension dictionary. 
  * Stores the properties of each layer in the drawing in an XRecord object in the ACAD_LAYERSTATE dictionary. AutoCAD stores all layer settings in the XRecord, but identifies the specific settings you chose to save. When you restore the layer settings, AutoCAD restores only the settings you chose to save. 

Each time you save another layer setting in the drawing, AutoCAD creates another XRecord object describing the saved settings and stores the XRecord in the ACAD_LAYERSTATE dictionary. The following diagram illustrates the process. 

You do not need (and should not try) to directly manipulate the entries when working with layer states. Use the functions of the LayerStateManager object to access the dictionary. Once you have a reference to the dictionary, you can step through each of the entries which are represented as DBDictionaryEntry objects. 

## List the saved layer states in a drawing

If layer states have been saved in the current drawing, the following code lists the names of all saved layer states: 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("ListLayerStates")]
    public static void ListLayerStates()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            LayerStateManager acLyrStMan;
            acLyrStMan = acCurDb.LayerStateManager;
    
            DBDictionary acDbDict;
            acDbDict = acTrans.GetObject(acLyrStMan.LayerStatesDictionaryId(true),
                                            OpenMode.ForRead) as DBDictionary;
    
            string sLayerStateNames = "";
    
            foreach (DBDictionaryEntry acDbDictEnt in acDbDict)
            {
                sLayerStateNames = sLayerStateNames + "\n" + acDbDictEnt.Key;
            }
    
            Application.ShowAlertDialog("The saved layer settings in this drawing are:" +
                                        sLayerStateNames);
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("ListLayerStates")> _
    Public Sub ListLayerStates()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            Dim acLyrStMan As LayerStateManager
            acLyrStMan = acCurDb.LayerStateManager
    
            Dim acDbDict As DBDictionary
            acDbDict = acTrans.GetObject(acLyrStMan.LayerStatesDictionaryId(True), _
                                         OpenMode.ForRead)
    
            Dim sLayerStateNames As String = ""
    
            For Each acDbDictEnt As DBDictionaryEntry In acDbDict
                sLayerStateNames = sLayerStateNames & vbLf & acDbDictEnt.Key
            Next
    
            Application.ShowAlertDialog("The saved layer settings in this drawing are:" & _
                                        sLayerStateNames)
    
            '' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ListLayerStates()
         On Error Resume Next
        Dim oLSMDict As AcadDictionary
        Dim XRec As Object
        Dim layerstateNames As String
     
        layerstateNames = ""
        ' Get the ACAD_LAYERSTATES dictionary, which is in the
        ' extension dictionary in the Layers object.
        Set oLSMDict = ThisDrawing.Layers. _
                                   GetExtensionDictionary.Item("ACAD_LAYERSTATES")
     
        ' List the name of each saved layer setting. Settings are
        ' stored as XRecords in the dictionary.
        For Each XRec In oLSMDict
           layerstateNames = layerstateNames + XRec.Name + vbCrLf
        Next XRec
     
        MsgBox "The saved layer settings in this drawing are: " + _
               vbCrLf + layerstateNames
    End Sub
