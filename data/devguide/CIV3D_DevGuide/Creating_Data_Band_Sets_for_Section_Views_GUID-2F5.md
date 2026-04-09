<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Creating a Data Band Set > Creating Data Band Sets for Section Views -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-2F575E13-15AC-407A-98B0-EDE2F3A5AB8C.htm -->

# Creating Data Band Sets for Section Views

Individual band styles can be grouped together into a set, which can then be assigned to a graph. Band sets for section graphs are objects of type AeccSectionViewBandStyleSet, and all such sets are stored in the AeccDocument.SectionViewBandStyleSet collection. 

The following example demonstrates creating a section band style set and adding a band style to it:
    
    
    Dim oSectionViewBandStyleSet As AeccSectionViewBandStyleSet
    Set oSectionViewBandStyleSet = _
      oDocument.SectionViewBandStyleSets.Add("Section Band Set")
     
    ' Add a band style we have already created to the
    ' band set.
    Call oSectionViewBandStyleSet.Add(oBandSectionDataStyle)
     
    ' Now we have a band set consisting of one band.
    

Data band sets are used when section views are first created. The following sample code is taken from the [Creating Section Views](<GUID-62A68181-648C-4ABC-9DAB-AB36C721355D.htm>) section of the [Sections](<GUID-52FEAA8B-BE9C-4C3B-9D11-185E9818B684.htm>) chapter, but this time a data band set is passed in the last parameter:
    
    
    Set oSectionView=oSampleLines.Item(j).SectionViews.Add( _
       "Section View" & CStr(j), _
       "0", _
       dOriginPt, _
       oSectionViewStyle, _
       oSectionViewBandStyleSet)
