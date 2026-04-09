<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Sections > Using Sections -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-847201E7-CF67-453F-841B-8AF8291F49DE.htm -->

# Using Sections

Each sample line contains a collection of sections that were based on that sample line. Each section is represented by object of type AeccSection and contains methods for retrieving statistics of the surface along the section. While sections initially have styles based on the AeccSectionStyle style passed to the AeccSampledSurfaces.Add method, you can also set the style for each section individually through the AeccSection.Style property.
    
    
    Dim oSampleLines as AeccSampleLines
    Set oSampleLines = oSampleLineGroup.SampleLines
     
    ' For each sample line, go through all the sections that
    ' were created based on it.
    Dim i As Integer
    Dim j As Integer
    For i = 0 To oSampleLines.Count - 1
       Dim oSections As AeccSections
       Set oSections = oSampleLines.Item(i).Sections
     
       ' For each section, print its highest elevation and set
       ' some of its properties.
       Dim oSection as AeccSection
       For Each oSection in oSections
          Debug.Print "Max Elevation of "; oSection.Name;
          Debug.Print " is: "; oSection.ElevationMax
           oSection.DataType = aeccSectionDataTIN
          oSection.StaticDynamic = aeccSectionStateDynamic
       Next
    Next i
