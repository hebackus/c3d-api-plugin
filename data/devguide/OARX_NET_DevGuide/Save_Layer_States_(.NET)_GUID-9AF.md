<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Save and Restore Layer States (.NET) > Use the LayerStateManager to Manage Layer States (.NET) > Save Layer States (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9AFCDEAB-96B1-4F03-B118-C26665BB920F.htm -->

# Save Layer States (.NET)

Use the SaveLayerState method to save a set of layer settings in a drawing. The SaveLayerState method requires three parameters. The first parameter is a string naming the layer state you are saving. The second parameter identifies the layer properties you want to save. Use the constants of the LayerStateMasks enum to identify the layer settings you want to save. The following table lists the constants that are part of the LayerStateMasks enum. 

Constants for layer state mask   
---  
Constant name  |  Layer property   
Color  |  Color   
CurrentViewport  |  Current viewport layers frozen or thawed   
Frozen  |  Frozen or thawed   
LastRestored  |  Last restored layer   
LineType  |  Linetype   
LineWeight  |  Lineweight   
Locked  |  Locked or unlocked   
NewViewport  |  New viewport layers frozen or thawed   
None  |  No layer settings   
On  |  On or off   
Plot  |  Plotting on or off   
PlotStyle  |  Plot style   
  
Add the constants together to specify multiple properties. 

The third parameter required is the object id of the viewport whose layer settings you want to save. Use ObjectId.Null to not specify a viewport. If you try to save a layer state under a name that already exists, an error is returned. You must rename or delete the existing layer state before you can reuse the name. 

## Save a layer's color and linetype settings

The following code saves the color and linetype settings of the current layers in the drawing under the name ColorLinetype. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("SaveLayerColorAndLinetype")]
    public static void SaveLayerColorAndLinetype()
    {
        // Get the current document
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
        LayerStateManager acLyrStMan;
        acLyrStMan = acDoc.Database.LayerStateManager;
     
        string sLyrStName = "ColorLinetype";
     
        if (acLyrStMan.HasLayerState(sLyrStName) == false)
        {
            acLyrStMan.SaveLayerState(sLyrStName,
                                      LayerStateMasks.Color | 
                                      LayerStateMasks.LineType,
                                      ObjectId.Null);
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("SaveLayerColorAndLinetype")> _
    Public Sub SaveLayerColorAndLinetype()
        '' Get the current document
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
        Dim acLyrStMan As LayerStateManager
        acLyrStMan = acDoc.Database.LayerStateManager
     
        Dim sLyrStName As String = "ColorLinetype"
     
        If acLyrStMan.HasLayerState(sLyrStName) = False Then
            acLyrStMan.SaveLayerState(sLyrStName, _
                                      LayerStateMasks.Color + _
                                      LayerStateMasks.LineType, _
                                      ObjectId.Null)
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SaveLayerColorAndLinetype()
        Dim oLSM As AcadLayerStateManager
     
        ' Access the LayerStateManager object
        Set oLSM = ThisDrawing.Application. _
                       GetInterfaceObject("AutoCAD.AcadLayerStateManager.25")
     
        ' Associate the current drawing database with LayerStateManager
        oLSM.SetDatabase ThisDrawing.Database
        oLSM.Save "ColorLinetype", acLsColor + acLsLineType
    End Sub
