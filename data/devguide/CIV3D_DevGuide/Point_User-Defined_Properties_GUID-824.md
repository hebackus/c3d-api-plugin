<!-- Developer's Guide > API Developer's Guide > Points > Using Points > Point User-Defined Properties -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8242CCAE-1346-4132-A8F8-31EDD2CAC093.htm -->

# Point User-Defined Properties

User-defined properties (UDPs) allow users to attach additional data to points. (UDPs can also be assigned to Parcels). UDPs are organized into groups called UDP Classifications, which in turn are assigned to PointGroups. UDPs can also be “unclassified”. When a UDPClassification is associated with a PointGroup object (using its UseCustomClassification() method), all the UDP definitions in the UDPClassification are assigned to each point in the PointGroup. UDP values are unique for each point, and can be changed individually. Each point gets a UDP’s default value (if UseDefault is true for the UDP) upon assignment. 

Each instance of a UDP is a class derived from the UDP base class, with additional properties depending on the data type. UDPDouble and UDPInteger types have upper and lower bound properties, to express a range. UDPEnumeration types have a GetEnumerationValues() method to get an array of all defined values. 

To create a UDP, you must first create and populate an AttributeTypeInfo<type> object (there is one for each UDP type), and pass it to the CreateUDP() method for an existing UDPClassification. UDPs have a GUID as well as a name, and the name+GUID combination is guaranteed to be a unique identifier. The CreateUDP() method takes an optional GUID parameter, so that you can create UDPs with a specific name+GUID combination. This allows you to create identical UDPs in multiple drawings. 

For more information about user-defined properties and classifications, see User-Defined Property Classifications in the Autodesk Civil 3D User Guide. 

This sample creates a new user-defined property classification for points called “Example”, and then adds a new user-defined property with upper and lower bounds and a default value: 
    
    
    [CommandMethod("C3DSAMPLES", "UDPExample", CommandFlags.Modal)]
    public void UDPExample()
    {
        using (Transaction tr = startTransaction())
        {
            // _civildoc is the active CivilDocument instance.
            UDPClassification udpClassification = _civildoc.PointUDPClassifications.Add("Example");
            AttributeTypeInfoInt attributeTypeInfoInt = new AttributeTypeInfoInt("Int UDP");
            attributeTypeInfoInt.DefaultValue = 15;
            attributeTypeInfoInt.UpperBoundValue = 20;
            attributeTypeInfoInt.LowerBoundValue = 10;
            UDP udp = udpClassification.CreateUDP(attributeTypeInfoInt);
    
            // assign a point group
            ObjectId pointGroupId = _civildoc.PointGroups.AllPointGroupsId;
            PointGroup pointGroup = pointGroupId.GetObject(OpenMode.ForWrite) as PointGroup;
            pointGroup.UseCustomClassification("Example");
    
    
            tr.Commit();
        }
    }

This example illustrates accessing the collection of all Point UDPClassifications in a document, and then reading each UDP in each UDPClassification. 
    
    
    [CommandMethod("C3DSAMPLES", "ListUDPs", CommandFlags.Modal)]
    public void ListUDPs()
    {
        using (Transaction tr = startTransaction())
        {
            // _civildoc is the active CivilDocument instance.
            foreach (UDPClassification udpClassification in _civildoc.PointUDPClassifications)
            {
                _editor.WriteMessage("\n\nUDP Classification: {0}\n", udpClassification.Name);
                foreach (UDP udp in udpClassification.UDPs)
                {
                    _editor.WriteMessage(" * UDP name: {0} guid: {1}, description: {2}, default value: {3}, use default? {4}\n",
                        udp.Name, udp.Guid, udp.Description, udp.DefaultValue, udp.UseDefaultValue);
    
                    _editor.WriteMessage("\tUDP type: {0}\n", udp.GetType().ToString());
    
                    var udpType = udp.GetType().Name;
                    switch (udpType)
                    {
                        // Booleans and String types do not define extra properties
                        case "UDPBoolean":
                        case "UDPString":
                            break;
    
                        case "UDPInteger":
                            UDPInteger udpInteger = (UDPInteger)udp;
                            _editor.WriteMessage("\tUpper value: {0}, inclusive? {1}, Lower bound value: {2}, inclusive? {3}\n",
                                udpInteger.UpperBoundValue, udpInteger.UpperBoundInclusive, udpInteger.LowerBoundValue, udpInteger.LowerBoundInclusive);
                            break;
    
                        case "UDPDouble":
                            UDPDouble udpDouble = (UDPDouble)udp;
                            _editor.WriteMessage("\tUpper value: {0}, inclusive? {1}, Lower bound value: {2}, inclusive? {3}\n",
                                udpDouble.UpperBoundValue, udpDouble.UpperBoundInclusive, udpDouble.LowerBoundValue, udpDouble.LowerBoundInclusive);
                            break;
    
                        case "UDPEnumeration":
                            UDPEnumeration udpEnumeration = (UDPEnumeration)udp;
                            _editor.WriteMessage("\tEnumeration values: {0}\n", udpEnumeration.GetEnumValues());
                            break;
                    }
                }
            }
    
            tr.Commit();
        }
    }
