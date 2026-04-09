<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Stations > Creating Station Sets -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FA715167-53BC-41C1-A185-3D795BC219CE.htm -->

# Creating Station Sets

Alignment stations are usually labeled at regular intervals. You can compute the number, location, and geometry of stations taken at regular spacings by using the AeccAlignment.GetStations method. This function returns a collection of stations based on the desired interval of major and minor stations and the type of station requested. Unless the type of station requested is aeccEquation, station values ignore any station equations.
    
    
    Dim oStations As AeccAlignmentStations
     
    ' If we were to label major stations placed every 100 units
    ' and minor stations placed every 20, how many labels 
    ' would this alignment have?
    Set oStations = oAlignment.GetStations(aeccAll, 100#, 20#)
    Debug.Print "Number of labels: " & oStations.Count
     
    ' Print the location of each major station in the set.
    Dim i as Integer
    For i = 0 To oStations.Count - 1
        If (oStations.Item(i).Type = aeccMajor) Then
            Dim j As Integer
            Dim x As Integer
            Dim y As Integer
            j = oStations.Item(i).Station
            x = oStations.Item(i).Easting
            y = oStations.Item(i).Northing
            Debug.Print "Station " & j & " is at:" & x & ", " & y
        End If
    Next i
