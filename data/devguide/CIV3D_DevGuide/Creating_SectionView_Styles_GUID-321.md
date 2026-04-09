<!-- Developer's Guide > API Developer's Guide > Sections Overview > Sections >  Creating SectionView Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-321A87EF-2604-4CA2-B678-3DAB84590319.htm -->

#  Creating SectionView Styles

The SectionViewStyle object governs all aspects of how the graph axes, text, and titles are drawn. Within SectionViewStyle are settings dealing with the top, bottom, left, center vertical, and right axes, and with the graph as a whole. All section view styles are stored in the CivilDocument.Styles.SectionViewStyles collection. 

Note that there is a naming ambiguity between Autodesk.Civil.DatabaseServices.Styles.SecitonViewStyle and Autodesk.AutoCAD.DatabaseServices.SectionViewStyle. You can resolve this by fully qualifying the class name in your code, or disambiguiate the reference with a using alias statement such as: 
    
    
    using SectionViewStyle = Autodesk.Civil.DatabaseServices.Styles.SectionViewStyle;

New styles are created with the Add() method with the name of the new style. This style is only used in the plan view direction, and component display settings are accessed with the SectionViewStyle.GetDisplayStylePlan(). This method takes a SectionViewDisplayStyleType enum that specifies the component to get. Other style settings are accessed via properties for the SectionViewStyle object, such as BottomAxis and GraphStyle.

In this example, a new SectionViewStyle is created, and the Graph Title display component line type is set to "DOT": 
    
    
    ObjectId sectionViewStyleId = _civildoc.Styles.SectionViewStyles.Add("New SectionView Style");
    SectionViewStyle sectionViewStyle = ts.GetObject(sectionViewStyleId, OpenMode.ForWrite) as SectionViewStyle;
    sectionViewStyle.GetDisplayStylePlan(SectionViewDisplayStyleType.GraphTitle).Linetype = "DOT";
    

The title of the graph is controlled by the SectionViewStyle.GraphStyle.TitleStyle property, an object of type GraphTitleStyle. The title style object can adjust the position, style, and border of the title. The text of the title can include any of the following property fields: 

<[Section View Description(CP)]>  
---  
<[Section View Name(CP)]>  
<[Parent Alignment(CP)]>  
<[Section View Station(Uft|FS|P3|RN|Sn|OF|AP|B2|TP|EN|W0|DZY)]>  
<[Section View Datum Value(Uft|P3|RN|AP|Sn|OF)]>  
<[Section View Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Left Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Right Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Drawing Scale(P3|RN|AP|OF)]>  
<[Graph View Vertical Scale(P3|RN|AP|OF)]>  
<[Graph View Vertical Exageration(P3|RN|AP|OF)]>  
<[Sample Line Name(CP)]>  
<[Sample Line Group(CP)]>  
<[Sample Line Number(Sn)]>  
  
All axis styles are based on the AxisStyle class. The axis style object controls the display style of the axis itself, tick marks and text placed along the axis, and a text annotation describing the purpose of the axis. The annotation text, location, and size is set through the AxisStyle.TitleStyle property, an object of type AxisTitleStyle. The annotation text can use any of the following property fields:   
  
---  
**Valid property fields for AeccAxisTitleStyle.Text** |  **Axes**  
<[Section View Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]> |  top, bottom   
<[Section View Width(Uft|P2|RN|AP|Sn|OF)]> |  top, bottom   
<[Left Width(Uft|P2|RN|AP|Sn|OF)]> |  top, bottom   
<[Right Width(Uft|P2|RN|AP|Sn|OF)]> |  top, bottom   
<[Elevation Range(Uft|P2|RN|AP|Sn|OF)]> |  left, right, center   
<[Minimum Elevation(Uft|P2|RN|AP|Sn|OF)]> |  left, right, center   
<[Maximum Elevation(Uft|P2|RN|AP|Sn|OF)]> |  left, right, center   
  
Within each axis style are properties for specifying the tick marks placed along the axis. Both major tick marks and minor tick marks are represented by objects of type AxisTickStyle manages the location, size, and visual style of tick marks through its Interval, and Size properties. 

Note: While most style properties use drawing units, the Interval property uses surface units. 

The AxisTickStyle object also sets what text is displayed at each tick, including any of the following property fields: 

<[Section View Point Offset Side(CP)]>  
---  
<[Section View Point Offset(Uft|P3|RN|Sn|OF|AP)]>  
<[Graph View Abscissa Value(Uft|P3|RN|AP|Sn|OF)]>
