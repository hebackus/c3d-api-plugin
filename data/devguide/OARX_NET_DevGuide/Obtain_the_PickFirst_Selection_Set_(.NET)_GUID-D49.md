<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Obtain the PickFirst Selection Set (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D4987D00-1164-4217-A82E-B8B49FFB7A29.htm -->

# Obtain the PickFirst Selection Set (.NET)

The PickFirst selection set is created when you select objects prior to starting a command. Several conditions must be present in order to obtain the objects of a PickFirst selection set, these conditions are: 

  * PICKFIRST system variable must be set to 1 
  * UsePickSet command flag must be defined with the command that should use the PickFirst selection set 
  * Call the SelectImplied method to obtain the PickFirst selection set 

The SetImpliedSelection method is used to clear the current PickFirst selection set. 

## Get the Pickfirst selection set

This example displays the number of objects in the PickFirst selection set and then requests the user to select additional objects. Before requesting the user to select objects, the current PickFirst selection set is cleared with the SetImpliedSelection method. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("CheckForPickfirstSelection", CommandFlags.UsePickSet)]
    public static void CheckForPickfirstSelection()
    {
        // Get the current document
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Get the PickFirst selection set
        PromptSelectionResult acSSPrompt;
        acSSPrompt = acDocEd.SelectImplied();
    
        SelectionSet acSSet;
    
        // If the prompt status is OK, objects were selected before
        // the command was started
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            acSSet = acSSPrompt.Value;
    
            Application.ShowAlertDialog("Number of objects in Pickfirst selection: " +
                                        acSSet.Count.ToString());
        }
        else
        {
            Application.ShowAlertDialog("Number of objects in Pickfirst selection: 0");
        }
    
        // Clear the PickFirst selection set
        ObjectId[] idarrayEmpty = new ObjectId[0];
        acDocEd.SetImpliedSelection(idarrayEmpty);
    
        // Request for objects to be selected in the drawing area
        acSSPrompt = acDocEd.GetSelection();
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            acSSet = acSSPrompt.Value;
    
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
     
    <CommandMethod("CheckForPickfirstSelection", CommandFlags.UsePickSet)> _
    Public Sub CheckForPickfirstSelection()
        '' Get the current document
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Get the PickFirst selection set
        Dim acSSPrompt As PromptSelectionResult
        acSSPrompt = acDocEd.SelectImplied()
    
        Dim acSSet As SelectionSet
    
        '' If the prompt status is OK, objects were selected before 
        '' the command was started
        If acSSPrompt.Status = PromptStatus.OK Then
            acSSet = acSSPrompt.Value
    
            Application.ShowAlertDialog("Number of objects in Pickfirst selection: " & _
                                        acSSet.Count.ToString())
        Else
            Application.ShowAlertDialog("Number of objects in Pickfirst selection: 0")
        End If
    
        '' Clear the PickFirst selection set
        Dim idarrayEmpty() As ObjectId
        acDocEd.SetImpliedSelection(idarrayEmpty)
    
        '' Request for objects to be selected in the drawing area
        acSSPrompt = acDocEd.GetSelection()
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            acSSet = acSSPrompt.Value
    
            Application.ShowAlertDialog("Number of objects selected: " & _
                                        acSSet.Count.ToString())
        Else
            Application.ShowAlertDialog("Number of objects selected: 0")
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CheckForPickfirstSelection()
        ' Get the Pickfirst selection set
        Dim acSSet As AcadSelectionSet
        Set acSSet = ThisDrawing.PickfirstSelectionSet
     
        ' Display the number of selected objects
        MsgBox "Number of objects in Pickfirst selection set: " & acSSet.Count
     
        ' Create a new selection set
        Dim acSSetUser As AcadSelectionSet
        Set acSSetUser = ThisDrawing.SelectionSets.Add("User")
     
        ' Select objects in the drawing
        acSSetUser.SelectOnScreen
     
        ' Display the number of selected objects
        MsgBox "Number of objects selected: " & acSSetUser.Count
        ' Remove the new named selection set
        acSSetUser.Delete
    End Sub
