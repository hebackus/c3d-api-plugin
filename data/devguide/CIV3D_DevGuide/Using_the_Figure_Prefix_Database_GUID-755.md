<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures > Using the Figure Prefix Database -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-75549086-4C7B-49A2-BE9C-4D893AB31BE7.htm -->

# Using the Figure Prefix Database

A figure read from a fieldbook file can have a letter prefix signifying what object or concept the figure represents. This figure prefix describes the style and property settings to use with the figure. A list of figure prefixes is stored in AeccSurveyFigurePrefixDatabase objects. The collection of all databases in the document are stored in the AeccSurveyDocument.FigurePrefixDatabases property. New figure prefixes and databases are added through the parent collection’s Create method. Once a prefix or database is created, it becomes a permanent part of the figure prefix database and it is not lost upon loading a new document or running a new instance of Autodesk Civil 3D. Because of this, it is important to check for existing prefix databases and prefixes by name before trying to create new ones. The AeccSurveyFigurePrefixDatabases.FindItem method can be used to search for an existing database id or name. 

Note:

The similarly named AeccSurveyFigurePrefixDatabase.FindItem can only be used to search for the identification numbers of prefixes within a database - to find a prefix by name, use the AeccSurveyFigurePrefixDatabase.GetMatchedFigurePrefix method.

This sample creates a new figure prefix database and a new figure prefix. It switches the current database to the newly created one, and sets an existing figure to use the new prefix’s style.
    
    
    ' Get a reference to all the prefix databases.
    Dim oPrefixDatabases As AeccSurveyFigurePrefixDatabases
    Set oPrefixDatabases = oSurveyDocument.FigurePrefixDatabases
     
    ' See if our database already exists. If it does not, 
    ' create a new one.
    Dim oPrefixDatabase As AeccSurveyFigurePrefixDatabase
    Set oPrefixDatabase = oPrefixDatabases.FindItem("NewDB")
    If (oPrefixDatabase Is Nothing) Then
        Set oPrefixDatabase = oPrefixDatabases.Create("NewDB")
    End If
     
    ' See if our figure prefix already exists. If it does not,
    ' create a new figure prefix.
    Dim oSurveyFigurePrefix As AeccSurveyFigurePrefix
    On Error Resume Next
    Set oSurveyFigurePrefix = _
      oPrefixDatabase.GetMatchedFigurePrefix("BV")
    On Error GoTo 0
    If (oSurveyFigurePrefix Is Nothing) Then
        Set oSurveyFigurePrefix = oPrefixDatabase.Create("BV")
    End If
     
    ' Set the properties of the prefix.
    oSurveyFigurePrefix.Style = _
      oSurveyDocument.FigureStyles(0).Name
    oSurveyFigurePrefix.IsLotLine = True
    oSurveyFigurePrefix.IsBreakline = True
    oSurveyFigurePrefix.Layer = "0"
    oSurveyFigurePrefix.Save
    

You can set a figure to use a prefix style manually by using the AeccSurveyFigure.InitializeFromFigurePrefix method. It searches through the current prefix database for a prefix name that matches the first part of the name of the figure. For example, a figure with the name “BV 01” matches a prefix with the name “BV”. The current prefix database can be determined through the CurrentFigurePrefixDatabase property of the document’s survey user settings. The following code shows the correct method for doing this:
    
    
    Dim oUserSettings  As AeccSurveyUserSettings
    Dim CurrentDatabase As String
    Set oUserSettings = oSurveyDocument.GetUserSettings
    CurrentDatabase = oUserSettings.CurrentFigurePrefixDatabase
    

You can change the current database by setting the CurrentFigurePrefixDatabase property to the new name and then updating the survey user settings: 
    
    
    oUserSettings.CurrentFigurePrefixDatabase = "NewDB"
    oSurveyDocument.UpdateUserSettings oUserSettings
