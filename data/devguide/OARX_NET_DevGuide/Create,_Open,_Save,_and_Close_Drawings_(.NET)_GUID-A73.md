<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Create, Open, Save, and Close Drawings (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A73E66C5-AE7F-4142-9160-705C04552C4A.htm -->

# Create, Open, Save, and Close Drawings (.NET)

The DocumentCollection, DocumentCollectionExtension, Document, and Database objects provide access to the AutoCAD® file methods. 

## VBA/ActiveX Cross Reference

VBA/ActiveX Class  | .NET API Class   
---|---  
Documents collection  | DocumentCollection and DocumentCollectionExtension  
Document  | Document and Database  
Document.Saved  | System.Convert.ToInt16(Application.GetSystemVariable("DBMOD"))
