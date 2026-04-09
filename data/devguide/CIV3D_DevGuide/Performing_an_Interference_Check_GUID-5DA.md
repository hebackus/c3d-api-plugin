<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Interference Checks > Performing an Interference Check -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5DA84CA6-3C9C-4ABC-858E-977099DA1FFF.htm -->

# Performing an Interference Check

An interference check is used to detect intersections between the pipe parts of two different pipe networks or of pipes of a single network with themselves. The collection of all interference checks, an object of type AeccInterferenceChecks, is contained in the document’s AeccPipeDocument.InterferenceChecks property. A new interference check is made using the AeccInterferenceChecks.Create method, which requires an AeccInterferenceCheckCreationData parameter. The creation data object holds all the information needed to perform the check, including the type of check to perform, the distance between parts required for an interference, and the pipe networks being checked. A new creation data object can only be made using the AeccInterferenceChecks.GetDefaultCreationData method. A valid check requires at least the Name, LayerName, SourceNetwork and TargetNetwork properties of the creation data object to be set. 

The following sample performs an interference check between two networks:
    
    
    ' Get the collection of all interference checks.
    Dim oInterferenceChecks As AeccInterferenceChecks
    Set oInterferenceChecks = oPipeDocument.InterferenceChecks
     
    ' Set up the creation data structure for making an
    ' interference check.
    Dim oCreationData As AeccInterferenceCheckCreationData
    Set oCreationData = oInterferenceChecks.GetDefaultCreationData
     
    ' If pipes are closer than 3.5 units apart, count it as an
    ' intersection.
    oCreationData.Criteria.ApplyProximity = True
    oCreationData.Criteria.CriteriaDistance = 3.5
    oCreationData.Criteria.UseDistanceOrScaleFactor = aeccDistance
     
    ' List the networks being tested. We will compare a network
    ' with itself, so we list it twice.
    Set oCreationData.SourceNetwork = oPipeNetwork1
    Set oCreationData.TargetNetwork = oPipeNetwork2
     
    ' Assign the check a unique name and a layer to use.
    oCreationData.Name = "Test 01"
    oCreationData.LayerName = oPipeDocument.Layers.Item(0).Name
     
    ' Create a new check of the pipe network.
    Dim oInterferenceCheck As AeccInterferenceCheck
    Set oInterferenceCheck = _
      oInterferenceChecks.Create(oCreationData)
