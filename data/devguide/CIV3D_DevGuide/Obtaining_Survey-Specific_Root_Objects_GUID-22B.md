<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Root Objects > Obtaining Survey-Specific Root Objects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-22B1ADD9-96D1-401D-AFDD-725B05FAEBA5.htm -->

# Obtaining Survey-Specific Root Objects

Applications that perform survey operations require special versions of the base objects representing the application and document. The AeccSurveyApplication object is identical to the AeccApplication it is inherited from except that its AeccSurveyApplication.ActiveDocument property returns an object of type AeccSurveyDocument instead of AeccDocument. The AeccSurveyDocument object contains collections of survey-related items, such as projects and equipment databases in addition to all of the methods and properties of AeccDocument.

When using survey root objects, be sure to reference the “Autodesk Civil Engineering Survey 6.0 Object Library” (AeccXSurvey.tlb) and “Autodesk Civil Engineering UI Survey 6.0 Object Library” (AeccXUISurvey.tlb) libraries.

This sample demonstrates how to retrieve the survey root objects:
    
    
    Dim oApp As AcadApplication
    Set oApp = ThisDrawing.Application
    Dim sAppName As String
    sAppName = "AeccXUiSurvey.AeccSurveyApplication"
    Dim oSurveyApplication As AeccSurveyApplication
    Set oSurveyApplication = oApp.GetInterfaceObject(sAppName)
     
    ' Get a reference to the currently active document.
    Dim oSurveyDocument As AeccSurveyDocument
    Set oSurveyDocument = oSurveyApplication.ActiveDocument
