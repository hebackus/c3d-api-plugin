<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Root Objects > Creating a Survey Project -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1318F8E8-2EDE-480E-9A7D-6CA9FE86998F.htm -->

# Creating a Survey Project

The survey database is the high-level construct that contains collections of networks and figures, and provides access to survey points. Throughout the API, survey databases are called “projects.” The collection of all projects in a document are held in the AeccSurveyDocument.Projects property. Once created, a project cannot be removed from this collection using API methods. The only way to remove a survey project is to delete the Project folder and refresh the collection. When a new project is created, a unique GUID identifying the project is generated.

This sample creates a new survey project with the name “Proj01”:
    
    
    Dim oSurveyProject As AeccSurveyProject
    Set oSurveyProject = oSurveyDocument.Projects.Create("Proj01")
     
    ' Print the next available survey point Id available.
    Debug.Print "Next available Id:"; _
      oSurveyProject.GetNextWritablePointNumber()
