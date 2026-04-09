<!-- Developer's Guide > API Developer's Guide > Root Objects and Common Concepts > Root Objects > Accessing and Using the Database Object -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8FA8B9C4-F95A-43AE-9739-3957085E51F8.htm -->

# Accessing and Using the Database Object

CivilDocument class does not expose the underlying database associated with the document. However, you can access the database from the AutoCAD Application.DocumentManager.MdiActiveDocument.Database object. The Database object contains references to Autodesk Civil 3D entities, as well as base AutoCAD entities. See the ObjectARX Managed Class Reference in the ObjectARX SDK for information.
