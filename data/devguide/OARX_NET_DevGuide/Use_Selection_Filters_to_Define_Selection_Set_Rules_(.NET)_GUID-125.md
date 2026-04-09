<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Remove Objects From a Selection Set (.NET) > Use Selection Filters to Define Selection Set Rules (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-125398A5-184C-4114-9212-A2FF28FC1F1D.htm -->

# Use Selection Filters to Define Selection Set Rules (.NET)

Selection filters are composed of pairs of arguments in the form of TypedValues. The first argument of a TypedValue identifies the type of filter (for example, an object), and the second argument specifies the value you are filtering on (for example, circles). The filter type is a DXF group code that specifies which filter to use. A few of the most common filter types are listed here. 

DXF codes for common filters   
---  
DXF code  |  Filter type   
0 (or DxfCode.Start)  |  Object Type (String)  Such as “Line,” “Circle,” “Arc,” and so forth.   
2 (or DxfCode.BlockName)  |  Block Name (String)  The block name of an insert reference.   
8 or (DxfCode.LayerName)  |  Layer Name (String)  Such as “Layer 0.”   
60 (DxfCode.Visibility)  |  Object Visibility (Integer)  Use 0 = visible, 1 = invisible.   
62 (or DxfCode.Color)  |  Color Number (Integer)  Numeric index values ranging from 0 to 256.  Zero indicates BYBLOCK. 256 indicates BYLAYER. A negative value indicates that the layer is turned off.   
67  |  Model/paper space indicator (Integer)  Use 0 or omitted = model space, 1 = paper space.   
  
## Specify a single selection criterion for a selection set

The following code prompts users to select objects to be included in a selection set, and filters out all objects except for circles. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("FilterSelectionSet")]
    public static void FilterSelectionSet()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Create a TypedValue array to define the filter criteria
        TypedValue[] acTypValAr = new TypedValue[1];
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Start, "CIRCLE"), 0);
    
        // Assign the filter criteria to a SelectionFilter object
        SelectionFilter acSelFtr = new SelectionFilter(acTypValAr);
    
        // Request for objects to be selected in the drawing area
        PromptSelectionResult acSSPrompt;
        acSSPrompt = acDocEd.GetSelection(acSelFtr);
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            SelectionSet acSSet = acSSPrompt.Value;
    
            Application.ShowAlertDialog("Number of objects selected: " +
                                        acSSet.Count.ToString());
        }
        else
        {
            Application.ShowAlertDialog("Number of objects selected: 0");
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("FilterSelectionSet")> _
    Public Sub FilterSelectionSet()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Create a TypedValue array to define the filter criteria
        Dim acTypValAr(0) As TypedValue
        acTypValAr.SetValue(New TypedValue(DxfCode.Start, "CIRCLE"), 0)
    
        '' Assign the filter criteria to a SelectionFilter object
        Dim acSelFtr As SelectionFilter = New SelectionFilter(acTypValAr)
    
        '' Request for objects to be selected in the drawing area
        Dim acSSPrompt As PromptSelectionResult
        acSSPrompt = acDocEd.GetSelection(acSelFtr)
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            Dim acSSet As SelectionSet = acSSPrompt.Value
    
            Application.ShowAlertDialog("Number of objects selected: " & _
                                        acSSet.Count.ToString())
        Else
            Application.ShowAlertDialog("Number of objects selected: 0")
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FilterSelectionSet()
        ' Create a new selection set
        Dim sset As AcadSelectionSet
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        ' Define the filter list, only Circle objects
        ' will be selectable
        Dim FilterType(0) As Integer
        Dim FilterData(0) As Variant
        FilterType(0) = 0
        FilterData(0) = "Circle"
     
        ' Prompt the user to select objects
        ' and add them to the selection set
        sset.SelectOnScreen FilterType, FilterData
     
        MsgBox "Number of objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub
