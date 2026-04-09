<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Check Spelling (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CD978B3F-B054-4797-9D3A-3759FC2756CB.htm -->

# Check Spelling (.NET)

During a spelling check, AutoCAD matches the words in the drawing to the words in the current main dictionary. Any words you add are stored in the custom dictionary that is current at the time of the spelling check. For example, you can add proper names so that AutoCAD no longer identifies them as misspelled words. 

To check spelling in another language, you can change to a different main dictionary. 

There is no method for checking spelling provided in the AutoCAD .NET API. However, you can specify a different main dictionary using the DCTMAIN system variable, or a different custom dictionary using the DCTCUST system variable.
