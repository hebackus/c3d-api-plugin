<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Remove Objects From a Selection Set (.NET) > Filter for Extended Data (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FCEBA022-3F80-47BE-BC29-8DF73CA9C0B8.htm -->

# Filter for Extended Data (.NET)

External applications can attach data such as text strings, numeric values, 3D points, distances, and layer names to AutoCAD objects. This data is referred to as extended data, or xdata. You can filter entities containing extended data for a specified application. 

## Select circles that contain xdata

The following example filters for circles containing xdata added by the “MY_APP” application: 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("FilterXdata")]
    public static void FilterXdata()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Create a TypedValue array to define the filter criteria
        TypedValue[] acTypValAr = new TypedValue[2];
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Start, "Circle"), 0);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.ExtendedDataRegAppName, 
                                            "MY_APP"), 1);
    
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
     
    <CommandMethod("FilterXdata")> _
    Public Sub FilterXdata()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Create a TypedValue array to define the filter criteria
        Dim acTypValAr(1) As TypedValue
        acTypValAr.SetValue(New TypedValue(DxfCode.Start, "Circle"), 0)
        acTypValAr.SetValue(New TypedValue(DxfCode.ExtendedDataRegAppName, _
                                           "MY_APP"), 1)
    
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
    
    
    Sub FilterXdata()
        Dim sset As AcadSelectionSet
        Dim FilterType(1) As Integer
        Dim FilterData(1) As Variant
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        FilterType(0) = 0: FilterData(0) = "Circle"
        FilterType(1) = 1001: FilterData(1) = "MY_APP"
     
        sset.SelectOnScreen FilterType, FilterData
     
        MsgBox "Number of objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub
