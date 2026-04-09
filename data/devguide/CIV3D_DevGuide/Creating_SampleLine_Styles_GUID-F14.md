<!-- Developer's Guide > API Developer's Guide > Sections Overview > Sample Lines >  Creating SampleLine Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F14A8EC7-FA4B-42AA-B7EF-97718E041804.htm -->

#  Creating SampleLine Styles

When working with SampleLines, there are three styles you need to work with to control how sample lines are displayed: 

GroupPlotStyle 
    This style controls how groups of section view graphs are drawn. The style changes the row and column orientation and spacing between multiple graphs. The collection of all GroupPlotStyle objects is contained in the CivilDocument.Styles.GroupPlotStyles collection. A GroupPlotStyle only contains settings for plan view, and settings are accessed with the GetDisplayPlan() method. 
    
    
    
    ObjectId groupPlotStyleId = _civildoc.Styles.GroupPlotStyles.Add("New GroupPlot Style");
    GroupPlotStyle groupPlotStyle = ts.GetObject(groupPlotStyleId, OpenMode.ForWrite) as GroupPlotStyle;
    groupPlotStyle.GetDisplayPlan(GroupPlotDisplayStyleType.Border).Color = Color.FromRgb(23, 54, 232);
    

SampleLineStyle 
     this style controls how sample lines are drawn on a surface. The collection of all SampleLineStyle objects is held in the CivilDocument.Styles.SampleLineStyles collection. A SampleLineStyle contains settings for both model view (via the GetDisplayStyleModel() method) and plan view (via the GetDisplayStylePlan() method). 
    
    
    
    ObjectId sampleLineStyleId = _civildoc.Styles.SampleLineStyles.Add("New SampleLine Style");
    SampleLineStyle sampleLineStyle = ts.GetObject(sampleLineStyleId, OpenMode.ForWrite) as SampleLineStyle;
    // Display lines in violet
    sampleLineStyle.GetDisplayStylePlan(SampleLineDisplayStyleType.Lines).Color = Color.FromColorIndex(ColorMethod.ByAci, 200);
    sampleLineStyle.GetDisplayStyleModel(SampleLineDisplayStyleType.Lines).Color = Color.FromColorIndex(ColorMethod.ByAci, 200);
    

SectionStyle 
    

this style controls how surface cross sections are displayed in the section view graphs. The collection of all SectionStyle objects is held in the CivilDocumet.Styles.SectionStyles collection. A SectionStyle contains settings for plan view only, accessed via the GetDisplayStyleSection() method. 

    
    
    
    ObjectId sectionStyleId = _civildoc.Styles.SectionStyles.Add("New Section Style");
    SectionStyle sectionStyle = ts.GetObject(sectionStyleId, OpenMode.ForWrite) as SectionStyle;
    sectionStyle.GetDisplayStyleSection(SectionDisplayStyleSectionType.Segments).Color = Color.FromRgb(180,0,255);
