<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Remove Objects From a Selection Set (.NET) > Specify Multiple Criteria in a Selection Filter (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-BE8B5EE4-9B5A-4D1F-B2D8-7DC013BFC6C0.htm -->

# Specify Multiple Criteria in a Selection Filter (.NET)

A selection filter can contain filtering criteria for more than just one property or object. You define the total number of conditions to filter on by declaring an array containing enough elements to represent each of the filter criterion. 

## Select objects that meet three criterion

The following example specifies three criterion to filter selected objects by: the object must be a circle, is blue in color, and must reside on layer 0. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("FilterBlueCircleOnLayer0")]
    public static void FilterBlueCircleOnLayer0()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Create a TypedValue array to define the filter criteria
        TypedValue[] acTypValAr = new TypedValue[3];
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Color, 5), 0);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Start, "CIRCLE"), 1);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.LayerName, "0"), 2);
    
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
     
    <CommandMethod("FilterBlueCircleOnLayer0")> _
    Public Sub FilterBlueCircleOnLayer0()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Create a TypedValue array to define the filter criteria
        Dim acTypValAr(2) As TypedValue
        acTypValAr.SetValue(New TypedValue(DxfCode.Color, 5), 0)
        acTypValAr.SetValue(New TypedValue(DxfCode.Start, "CIRCLE"), 1)
        acTypValAr.SetValue(New TypedValue(DxfCode.LayerName, "0"), 2)
    
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
    
    
    Sub FilterBlueCircleOnLayer0()
        Dim sset As AcadSelectionSet
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        ' Define the filter list, only blue Circle objects
        ' on layer 0
        Dim FilterType(2) As Integer
        Dim FilterData(2) As Variant
     
        FilterType(0) = 62: FilterData(0) = 5
        FilterType(1) = 0: FilterData(1) = "Circle"
        FilterType(2) = 8: FilterData(2) = "0"
     
        ' Prompt the user to select objects
        ' and add them to the selection set
        sset.SelectOnScreen FilterType, FilterData
     
        MsgBox "Number of objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub
