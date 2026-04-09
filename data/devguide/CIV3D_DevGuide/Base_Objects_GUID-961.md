<!-- Developer's Guide > API Developer's Guide > Getting Started > Migrating COM code to .NET > Base Objects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-961D5F38-92D6-40B9-9D23-56E5523017F2.htm -->

# Base Objects

The COM API requires that you access the AcadApplication object (via the ThisDrawing.Application object), get the interface object for the AeccApplication object, and from that get the active document. In the .NET API you import Autodesk.Civil.ApplicationServices namespace, and get the active document from the CivilApplication class:
    
    
    g_oDocument = CivilApplication.ActiveDocument()
    

There is a single root document object, CivilDocument, instead of four domain-specific root objects for Land, Pipe, Roadway and Survey.
