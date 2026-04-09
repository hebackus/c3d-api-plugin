<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Using Data Bands > Adding Data Bands to a Section View -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FE5DD719-6680-4FDB-8FCF-0BAFB44FA818.htm -->

# Adding Data Bands to a Section View

Every section view contains a collection of bands in its AeccSectionView.BandSet property, an object of type AeccSectionViewBandSet. When a section view is first created, all band styles from the AeccSectionViewBandStyleSet parameter are added to this collection. Individual band styles can be added to a section view through the AeccSectionViewBandSet collection using its Add or Insert methods. Both of these methods take an AeccSectionDataBandStyle style and two AeccSection objects, allowing comparison between sections. 

Tip:

If you only want to display a single section in the band, pass the same section object to both parameters.

The order of bands in the band set is also the order in which the bands are displayed. AeccSectionViewBandSet.Add places the new band at the bottom of the list while AeccSectionViewBandSet.Insert places the new band at the specified index. 

Tip:

You can swap the location of two bands with the AeccSectionViewBandSet.Swap method.

This sample adds a data band to a section view that describes the single section “oSection”:
    
    
    Dim oSectionViewBandSetItem As AeccSectionViewBandSetItem
    Set oSectionViewBandSetItem = oSectionView.BandSet.Add( _
      oBandSectionDataStyle, _
      oSection, _
      oSection)
      
    ' Now oSectionView has another data band.
