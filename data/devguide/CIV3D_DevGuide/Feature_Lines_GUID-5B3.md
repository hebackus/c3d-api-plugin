<!-- Developer's Guide > API Developer's Guide > Corridors > Feature Lines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5B3CC944-28CA-4B5C-B72B-D59B4B785370.htm -->

# Feature Lines

Feature lines are formed by connecting related points in each assembly along the length of a corridor baseline. These lines represent some aspect of the roadway, such as a sidewalk edge or one side of a corridor surface. Points become related by sharing a common _code_ , a string property usually describing the corridor feature.

Each baseline has two sets of feature lines, one for lines that are positioned along the main baseline and one for lines that are positioned along any of the offset baselines.

Note:

Creating feature lines from polylines is not supported in the .NET API. However, you can use the COM API IAeccLandFeatureLine:: AddFromPolyline() method.
