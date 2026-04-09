<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Save and Restore Layer States (.NET) > Use the LayerStateManager to Manage Layer States (.NET) > Export and Import Saved Layer States (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-67A027CA-085C-4377-81D2-12DF67A4F76A.htm -->

# Export and Import Saved Layer States (.NET)

You can export and import saved layer states to use the same layer settings in other drawings. Use the ExportLayerState method to export a saved layer state to an LAS file; use the ImportLayerState method to import a LAS file into a drawing. 

Note: Importing layer states does not restore them; you must use the RestoreLayerState method to restore the layer state after it is imported. 

The ExportLayerState method accepts two parameters. The first parameter is a string identifying the saved layer state to export. The second parameter is the name of the file you are exporting the layer state to. If you do not specify a path for the file, it is saved in the same directory in which the drawing was opened from. If the file name you specified already exists, the existing file is overwritten. Use a ._las_ extension when naming files; this is the extension AutoCAD recognizes for exported layer state files. 

The ImportLayerState method accepts one parameter: a string naming the file that contains the layer states you are importing. If the layer state you want to import does not exist in a LAS file, but a drawing file. You can open the drawing file and then use the ImportLayerStateFromDb method to import a layer state from the Database object of the other drawing. 

When you import layer states, an error condition is raised if any properties referenced in the saved settings are not available in the drawing you are importing to. The import is completed, however, and default properties are used. For example, if an exported layer is set to a linetype that is not loaded in the drawing it is being imported into, an error condition is raised and the drawing's default linetype is substituted. Your code should account for this error condition and continue processing if it is raised. 

If the imported file defines settings for layers that do not exist in the current drawing, those layers are created in the current drawing. When you use the RestoreLayerState method, the properties specified when the settings were saved are assigned to the new layers; all other properties of the new layers are assigned default settings. 

## Export saved layer settings

The following example exports a saved layer state to a file named _ColorLinetype.las_. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("ExportLayerState")]
    public static void ExportLayerState()
    {
        // Get the current document
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        LayerStateManager acLyrStMan;
        acLyrStMan = acDoc.Database.LayerStateManager;
    
        string sLyrStName = "ColorLinetype";
    
        if (acLyrStMan.HasLayerState(sLyrStName) == true)
        {
            acLyrStMan.ExportLayerState(sLyrStName, "c:\\my documents\\" +
                                                    sLyrStName + ".las");
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("ExportLayerState")> _
    Public Sub ExportLayerState()
        '' Get the current document
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Dim acLyrStMan As LayerStateManager
        acLyrStMan = acDoc.Database.LayerStateManager
    
        Dim sLyrStName As String = "ColorLinetype"
    
        If acLyrStMan.HasLayerState(sLyrStName) = True Then
            acLyrStMan.ExportLayerState(sLyrStName, "c:\my documents\" & _
                                                    sLyrStName & ".las")
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ExportLayerStates()
        Dim oLSM As AcadLayerStateManager
        Set oLSM = ThisDrawing.Application. _
           GetInterfaceObject("AutoCAD.AcadLayerStateManager.25")
     
        oLSM.SetDatabase ThisDrawing.Database
        oLSM.Export "ColorLinetype", "c:\my documents\ColorLinetype.las"
    End Sub

## Import saved layer settings

The following example imports the layer state from a file named _ColorLinetype.las_. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("ImportLayerState")]
    public static void ImportLayerState()
    {
        // Get the current document
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        LayerStateManager acLyrStMan;
        acLyrStMan = acDoc.Database.LayerStateManager;
    
        string sLyrStFileName = "c:\\my documents\\ColorLinetype.las";
    
        if (System.IO.File.Exists(sLyrStFileName))
        {
            try
            {
                acLyrStMan.ImportLayerState(sLyrStFileName);
            }
            catch (Autodesk.AutoCAD.Runtime.Exception ex)
            {
                Application.ShowAlertDialog(ex.Message);
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("ImportLayerState")> _
    Public Sub ImportLayerState()
        '' Get the current document
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Dim acLyrStMan As LayerStateManager
        acLyrStMan = acDoc.Database.LayerStateManager
    
        Dim sLyrStFileName As String = "c:\my documents\ColorLinetype.las"
    
        If System.IO.File.Exists(sLyrStFileName) Then
            Try
                acLyrStMan.ImportLayerState(sLyrStFileName)
            Catch ex As Autodesk.AutoCAD.Runtime.Exception
                Application.ShowAlertDialog(ex.Message)
            End Try
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ImportLayerStates()
        Dim oLSM As AcadLayerStateManager
        Set oLSM = ThisDrawing.Application. _
                       GetInterfaceObject("AutoCAD.AcadLayerStateManager.25")
        oLSM.SetDatabase ThisDrawing.Database
     
        ' If the drawing you're importing to does not contain
        ' all the linetypes referenced in the saved settings,
        ' an error is returned. The import is completed, though,
        ' and the default linetype is used.
        On Error Resume Next
        oLSM.Import "c:\my documents\ColorLType.las"
     
        If Err.Number = -2145386359 Then
           ' Error indicates a linetype is not defined
           MsgBox ("One or more linetypes specified in the imported " + _
                   "settings is not defined in your drawing")
        End If
     
        On Error GoTo 0
    End Sub
