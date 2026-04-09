<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Save and Restore Layer States (.NET) > Use the LayerStateManager to Manage Layer States (.NET) > Restore Layer States (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-0C21B797-40E0-472C-91C0-522F3F6EB859.htm -->

# Restore Layer States (.NET)

The RestoreLayerState method resets the layer settings in a layer state and requires four values. The first value is the name of the layer state to restore, and the second value is the object id of the viewport whose layer settings you want to restore. The third value is an integer that defines how layers not in the layer state are handled. The fourth value determines which layer settings are restored. 

The following values determine how layers not in a layer state are handled: 

  * 0 - Layers not in the layer state are left unchanged 
  * 1 - Layers not in the layer state are turned Off 
  * 2 - Layers not in the layer state are frozen in the current viewport 
  * 4 - Layer settings are restored as viewport overrides 

Note: You can use the sum of multiple values previous listed to define the restore behavior of layers not in a layer state. For example, you can turn off and freeze the layers that are not saved with a layer state. 

For example, if you save the color and linetype settings under the name “ColorLinetype” and subsequently change those settings, restoring “ColorLinetype” resets the layers to the colors and linetypes they had when “ColorLinetype” was saved. If you add new layers to the drawing after saving “ColorLinetype,” those new layers are not affected when you restore “ColorLinetype.” 

## Restore the color and linetype settings of a drawing's layers

Assuming that the color and linetype settings of the layers in the current drawing were previously saved under the name “ColorLinetype,” the following code restores the color and linetype settings of each layer in the drawing to the value they had when “ColorLinetype” was saved. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("RestoreLayerState")]
    public static void RestoreLayerState()
    {
        // Get the current document
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
        LayerStateManager acLyrStMan;
        acLyrStMan = acDoc.Database.LayerStateManager;
     
        string sLyrStName = "ColorLinetype";
     
        if (acLyrStMan.HasLayerState(sLyrStName) == true)
        {
            acLyrStMan.RestoreLayerState(sLyrStName,
                                         ObjectId.Null,
                                         1,
                                         LayerStateMasks.Color |
                                         LayerStateMasks.LineType);
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("RestoreLayerState")> _
    Public Sub RestoreLayerState()
        '' Get the current document
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
        Dim acLyrStMan As LayerStateManager
        acLyrStMan = acDoc.Database.LayerStateManager
     
        Dim sLyrStName As String = "ColorLinetype"
     
        If acLyrStMan.HasLayerState(sLyrStName) = True Then
            acLyrStMan.RestoreLayerState(sLyrStName, _
                                         ObjectId.Null, _
                                         1, _
                                         LayerStateMasks.Color + _
                                         LayerStateMasks.LineType)
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub RestoreLayerState()
        Dim oLSM As AcadLayerStateManager
        Set oLSM = ThisDrawing.Application. _
                       GetInterfaceObject("AutoCAD.AcadLayerStateManager.25")
     
        oLSM.SetDatabase ThisDrawing.Database
        oLSM.Restore "ColorLinetype"
    End Sub
