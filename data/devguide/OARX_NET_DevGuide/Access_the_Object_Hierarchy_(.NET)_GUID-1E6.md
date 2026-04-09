<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Access the Object Hierarchy (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-1E64D6B9-F522-4245-AACE-FEF35F8A7BD7.htm -->

# Access the Object Hierarchy (.NET)

While the Application is the root object in the AutoCAD .NET API, you commonly will be working with the database of the current drawing. The DocumentManager property of the Application object allows you to access the current document with the MdiActiveDocument property. From the Document object returned by the MdiActiveDocument property, you can access its database with the Database property. 

## C#
    
    
    Application.DocumentManager.MdiActiveDocument.Database.Clayer;

## VB.NET
    
    
    Application.DocumentManager.MdiActiveDocument.Database.Clayer

## VBA/ActiveX Code Reference
    
    
    ThisDrawing.ActiveLayer
