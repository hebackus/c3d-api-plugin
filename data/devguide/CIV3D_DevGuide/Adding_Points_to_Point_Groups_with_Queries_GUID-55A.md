<!-- Developer's Guide > API Developer's Guide > Points > Point Groups > Adding Points to Point Groups with Queries -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-55A8758C-41DF-47F6-A762-F9B87FAA1A54.htm -->

# Adding Points to Point Groups with Queries

Points can be selected and added to a PointGroup using either a standard (StandardPointGroupQuery object) or custom (CustomPointGroupQuery object) query, which both inherit from the PointGroupQuery base class. 

StandardPointGroupQuery encapsulates the “basic method” of creating a query using the GUI, which is described in the “Creating a Point Group Using the Basic Method” section of the Civil 3D User Guide. This method uses the tabs on the Create Point Group dialog to match points by raw descriptions, include or exclude specific points or ranges of points, and to include points from other point groups. To accomplish the same effect using the API, you first create an instance of a StandardPointGroupQuery object, and then set the various Include* and Exclude* properties to create the query. 

StandardPointGroupQuery has these properties for building a query: 

StandardPointGroupQuery PropertiesProperties  | Possible Values   
---|---  
IncludeElevations ExcludeElevations |  Any combination of, separated by commas: 

  * A single number 
  * An elevation range specified by a lower and upper bound separated by a hyphen (for example, 1-100) 
  * A > or < followed by a number. This specifies all elevations greater-than or less-than the number. 

**Example** : “<-100,1-100,110.01,>200” – specifies all points whose elevations meet one of the following criteria: less than -100, equal to or between 1 and 100, equal to 110.01, or greater than 200.   
IncludeFullDescriptions ExcludeFullDescriptions IncludeRawDescriptions ExcludeRawDescriptions |  One or more descriptions, separated by commas. The * is a wildcard matching any string.  **Example** : “IP*” matches all descriptions that start with IP   
IncludeNames ExcludeNames |  One or more point names separated by commas. The * is a wildcard matching any string.   
IncludeNumbers ExcludeNumbers |  Any combination of, separated by commas: 

  * An individual point number 
  * A Point number range specified by a lower and upper bound separated by a hyphen (for example, 100-105). 

  
  
All of the Include* properties are ORed together, and all the Exclude* properties are ORed together to create the final query string. The example below illustrates how the query string is built from properties: 
    
    
    // _civildoc is the active CivilDocument instance.
    ObjectId pointGroupId = _civildoc.PointGroups.Add("Example Point Group1");
    PointGroup pointGroup = pointGroupId.GetObject(OpenMode.ForWrite) as PointGroup;
    
    StandardPointGroupQuery standardQuery = new StandardPointGroupQuery();
    standardQuery.IncludeElevations = "100-200";
    standardQuery.IncludeFullDescriptions = "FLO*";
    standardQuery.IncludeNumbers = ">2200";
    standardQuery.ExcludeElevations = "150-155";
    standardQuery.ExcludeNames = "BRKL";
    standardQuery.UseCaseSensitiveMatch = true;
    
    pointGroup.SetQuery(standardQuery);
    pointGroup.Update();
    
    _editor.WriteMessage("Number of points selected: {0}\n  Query string: {1}\n\n",
        pointGroup.PointsCount, standardQuery.QueryString);
    
    // output:
    // Query string: (FullDescription='FLO*' OR PointElevation=100-200 OR 
    // PointNumber>2200) AND '' NOT (Name='BRKL' OR PointElevation=150-155)

The CustomPointGroupQuery lets you specify a query string directly, and requires a more advanced knowledge of query operators. This method of query creation allows you to create nested queries that cannot be specified using the StandardPointGroupQuery object. 

Custom queries are made up of expressions, and expressions have three parts: 

  1. A property 
  2. A comparison operator: > < >= <= = 
  3. A value 

Multiple expressions are separated by logical set operators: AND, OR and NOT. Precedence of expressions and expression sets can be specified using parentheses. 

The precedence of evaluation in queries is: 

  1. Expressions in parentheses, with the innermost expressions evaluated first. 
  2. NOT 
  3. Comparisons 
  4. AND 
  5. OR 

The example below illustrates creating a point group and adding a custom query to it: 
    
    
    ObjectId pointGroupId2 = _civildoc.PointGroups.Add("Example Point Group2");
    PointGroup pointGroup2 = pointGroupId2.GetObject(OpenMode.ForWrite) as PointGroup;
    CustomPointGroupQuery customQuery = new CustomPointGroupQuery();
    string queryString = "(RawDescription='GR*') AND (PointElevation>=100 AND PointElevation<=300)";
    customQuery.QueryString = queryString;
    pointGroup2.SetQuery(customQuery);
    pointGroup2.Update();
    _editor.WriteMessage("PointGroup2: \n # points selected: {0}\n",
        pointGroup2.PointsCount);

Pending changes for a PointGroup can be accessed from the PointGroup.GetPendingChanges() method, which returns a PointGroupChangeInfo object. The pending change information for a PointGroup is updated when: 

  * A new point is added to the drawing that matches the query for the PointGroup.
  * An existing point in the PointGroup is removed. 

Note that changes are not registered when the query itself is changed. 

The example below adds a point that matches the custom query illustrated above, and removes a point from the PointGroup, registering both an added and removed point change in the PointGroupChangeInfo for the PointGroup.
    
    
    Point3d point3d = new Point3d(100,200,225); // elevation will be matched
    string rawDesc = "GRND"; // raw description will be matched
    _civildoc.CogoPoints.Add(point3d, rawDesc);
    
    // Point # 779 is in the point group:
    _civildoc.CogoPoints.Remove(779);
    
    PointGroupChangeInfo pointGroupChangeInfo = pointGroup2.GetPendingChanges();
    _editor.WriteMessage("Point group {0} pending changes: \n add: {1} \n remove: {2}\n",
        pointGroup2.Name, pointGroupChangeInfo.PointsToAdd.Length, pointGroupChangeInfo.PointsToRemove.Length);
    
    // changes are applied with update:
    pointGroup2.Update();

For more information about point group queries, see [Point Group Queries Reference](<https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/guidcrossbook/?v=2026&p=CIV3D&l=ENU&accessmode=live&guid=GUID-19866B57-C670-4638-95EE-15657E54F8FE>).
