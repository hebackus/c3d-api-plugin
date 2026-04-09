<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-99425C70-15B1-48E8-8DCF-3E4831DDB773.htm -->

# Corridor Surfaces

Corridor surfaces can represent the base upon which the corridor is constructed, the top of the finished roadway, or other aspects of the corridor. Such surfaces are represented by the TinSurface class and by a related CorridorSurface class. CorridorSurface objects contain corridor-specific information about the surfaces, such as which feature line, point, and link codes were used to create it. CorridorSurface objects always have a corresponding Surface object in the CivilDocument surfaces collection that exposes surface-related functionality. 

Removing a CorridorSurface also removes the corresponding TinSurface object. See [xref to section:] Creating a Surface from a CorridorSurface to create an independent Surface object.
