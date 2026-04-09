<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Hatches (.NET) > Associate a Hatch (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D3B9A37A-6A78-49C0-B02B-0C62B7F0714F.htm -->

# Associate a Hatch (.NET)

You can create associative or nonassociative hatches. Associative hatches are linked to their boundaries and updated when the boundaries are modified. Nonassociative hatches are independent of their boundaries. 

To make a hatch associative, set the Associative property of the hatch object created to TRUE. To make a hatch nonassociative, set the Associative property to FALSE. 

Associativity for hatch must be set before appending the hatch loop. If a hatch object is nonassociative, you can make it associative again by setting the Associative property to TRUE and re-appending the hatch loop.
