<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Creating a Data Band Set > Creating Data Band Sets for Profile Views -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A2AF30B5-5AA2-4687-BB97-4BC3A142133D.htm -->

# Creating Data Band Sets for Profile Views

Individual band styles can be grouped together into a set, which can then be assigned to a graph. Profile band sets are AeccProfileViewBandStyleSet objects stored in the AeccDocument.ProfileViewBandStyleSet collection.

The following example demonstrates creating a profile band style set and adding a band style to it:
    
    
    Dim oProfileViewBandStyleSet As AeccProfileViewBandStyleSet
    Set oProfileViewBandStyleSet = _
      oDocument.ProfileViewBandStyleSets.Add("Profile Band set")
     
    ' Add a band style we have already created to the
    ' band set.
    Call oProfileViewBandStyleSet.Add(oBandProfileDataStyle)
     
    ' Now we have a band set consisting of one band.
    

Data band sets are used when profile views are first created. The following sample code is taken from the topic [Creating a Profile View](<GUID-8B62A6B6-32CC-4289-89B0-EFDFDB3B04C8.htm>), but this time a data band set is passed in the last parameter.
    
    
    Set oProfileView = oAlignment.ProfileViews.Add( _
       "Profile Style 01", _
       "0", _
       dOriginPt, _
       oProfileViewStyle, _
       oProfileViewBandStyleSet)
