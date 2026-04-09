<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Viewports (.NET) > Floating Viewports (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F0906774-90AD-4AD2-9894-E37ACEF8035A.htm -->

# Floating Viewports (.NET)

You cannot edit the model from Paper space. To access the model in a Viewport object, toggle from Paper space to Model space using the SwitchToModelSpace and SwitchToPaperSpace member methods of the Editor object. As a result, you can work with the model while keeping the overall layout visible. In Viewport objects, the editing and view-changing capabilities are almost the same as in ViewportTableRecord objects. 

However, you have more control over the individual views. For example, you can freeze or thaw layers in some viewports without affecting others. You can toggle the display of the geometry in a viewport on or off. You can also align views between viewports and scale the views relative to the overall layout. 

The following illustration shows how different views of a model can be displayed in Paper space. Each Paper space image represents a Viewport object with a different view. In one view, the layer for dimensions is frozen. Notice that the title block, border, and annotation, which are drawn in Paper space, do not appear in the Model space view. Also, the layer containing the viewport borders has been frozen. 

When you are working in a Viewport object, you can be in either Model or Paper space. You can determine if you are working in Model space by checking the current values of the TILEMODE and CVPORT system variables. The following table breaks down the space and layout you are working in based on the current values of TILEMODE and CVPORT. is 0 and CVPORT is a value other than 2, you are working in Paper space, and if TILEMODE is 0 and CVPORT is 2 then you are working in Model space. If TILEMODE is 1, you are working in Model space on the Model layout. 

Current space   
---  
TILEMODE  |  CVPORT  |  Status   
0  | Not equal to 2 |  Layout other than Model is active and you are working in Paper space.   
0  | 2 |  Layout other than Model is active and you are working in a floating viewport.   
1  | Any value |  Model layout is active.   
  
Note: Before switching to Model space on when on a layout, the On property for at least one Viewport object on the layout should be set to TRUE. 

When you are in paper space, AutoCAD displays the paper space user coordinate system (UCS) icon in the lower-left corner of the graphics area. The crosshairs indicate that the paper space layout area (not the views in the viewports) can be edited. 

## To toggle between Model and Paper space

This example shows how to toggle between Model and Paper space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("ToggleSpace")]
    public static void ToggleSpace()
    {
      // Get the current document
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
      // Get the current values of CVPORT and TILEMODE
      object oCvports = Application.GetSystemVariable("CVPORT");
      object oTilemode = Application.GetSystemVariable("TILEMODE");
     
      // Check to see if the Model layout is active, TILEMODE is 1 when
      // the Model layout is active
      if (System.Convert.ToInt16(oTilemode) == 0)
      {
          // Check to see if Model space is active in a viewport,
          // CVPORT is 2 if Model space is active 
          if (System.Convert.ToInt16(oCvports) == 2)
          {
              acDoc.Editor.SwitchToPaperSpace();
          }
          else
          {
              acDoc.Editor.SwitchToModelSpace();
          }
      }
      else
      {
          // Switch to the previous Paper space layout
          Application.SetSystemVariable("TILEMODE", 0);
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("ToggleSpace")> _
    Public Sub ToggleSpace()
      '' Get the current document
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
      '' Get the current values of CVPORT and TILEMODE
      Dim nCvports As Integer = Application.GetSystemVariable("CVPORT")
      Dim nTilemode As Integer = Application.GetSystemVariable("TILEMODE")
     
      '' Check to see if the Model layout is active, TILEMODE is 1 when
      '' the Model layout is active
      If nTilemode = 0 Then
          '' Check to see if Model space is active in a viewport,
          '' CVPORT is 2 if Model space is active 
          If nCvports = 2 Then
              acDoc.Editor.SwitchToPaperSpace()
          Else
              acDoc.Editor.SwitchToModelSpace()
          End If
      Else
          '' Switch to the previous Paper space layout
          Application.SetSystemVariable("TILEMODE", 0)
      End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Public Sub ToggleSpace()
        ' Check to see if the Model layout is active
        If ThisDrawing.ActiveLayout.Name <> "Model" Then
            ' Check to see if Model space is active
            If ThisDrawing.MSpace = True Then
                ThisDrawing.MSpace = False
            Else
                ThisDrawing.MSpace = True
            End If
        Else
            ' Switch to the previous Paper space layout
            ThisDrawing.ActiveSpace = acPaperSpace
        End If
    End Sub
