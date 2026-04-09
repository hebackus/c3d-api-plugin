<!-- Developer's Guide > API Developer's Guide > Sections Overview > Sections -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-95139A97-8B1D-4A70-AB96-D8B0349B5268.htm -->

# Sections

Sections represent terrain elevations that cut across surfaces, including corridor surfaces, pipe networks, and grading, which are associated with a specified sample line group. Sections are "sampled" from a source (a surface or corridor shape). In the .NET API the sources for sections are exposed by the SectionSource object. A SampleLineGroup contains a collection of SectionSources, which can be accessed by the SampleLineGroup.GetSectionSources() method.
