<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > The Subassembly Tool Catalog > Creating a Tool Catalog ATC File > Sample Tool Catalog ATC Files -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1D0CC1CE-DB5E-427B-A2C2-485075145D5B.htm -->

# Sample Tool Catalog ATC Files

The sample tool catalog _.atc_ files define the contents and organization of an Autodesk subassembly tool catalog. These are generally split into separate files to keep files manageable: one listing all categories of tools and others listing tools within a single category.

Note:

XML tags in ATC files are case-sensitive. Make sure the tags in your files match the case of the tags defined in this chapter.

## Main Catalog File Example

The following is a portion of the file “ _Autodesk Civil 3D Metric Corridor Catalog.atc_.” It contains a list of tool categories. See the table following the sample for descriptions of the contents. This excerpt only contains the “Getting Started” category of tools.
    
    
    1)  <Catalog option="0">
    2)     <ItemID idValue="{0D75EF58-D86B-44DF-B39E-CE39E96077EC}"/>
    3)     <Properties>
    4)        <ItemName resource="9250" src="AeccStockSubassemblyScriptsRC.dll"/>
    5)        <Images option="0">
    6)           <Image cx="93" cy="123" src=".\Images\AeccCorridorModel.png"/>
    7)        </Images>
    8)        <Description resource="9201" src="AeccStockSubassemblyScriptsRC.dll"/>
    9)        <AccessRight>1</AccessRight>
    10)       <Time createdUniversalDateTime="2003-01-22T00:31:56" modifiedUniversalDateTime="2006-09-04T13:28:12"/>
    11)    </Properties>
    12)    <Source>
    13)       <Publisher>
    14)          <PublisherName>Autodesk</PublisherName>
    15)       </Publisher>
    16)    </Source>
    17)    <Tools/>
    18)    <Palettes/>
    19)    <Packages/>
    20)    <Categories>
    21)       <Category option="0">
    22)          <ItemID idValue="{4F5BFBF8-11E8-4479-99E0-4AA69B1DC292}"/>
    23)          <Url href=".\\C3D Metric Getting Started Subassembly Catalog.atc"/>
    24)          <Properties>
    25)             <ItemName resource="9212" src="AeccStockSubassemblyScriptsRC.dll"/>
    26)             <Images option="0">
    27)                <Image cx="93" cy="123" src=".\Images\AeccGenericSubassemblies.png"/>
    28)             </Images>
    29)             <Description resource="9213" src="AeccStockSubassemblyScriptsRC.dll"/>
    30)             <AccessRight>1</AccessRight>
    31)          </Properties>
    32)          <Source/>
    33)       </Category>
    34)  
    35) <!-- Other category items omitted -->
    36)  
    37)    </Categories>
    38)    <StockTools/>
    39)    <Catalogs/>
    40) </Catalog>
    

Line Number | Description  
---|---  
1-40 | The <Catalog> section contains the entire contents of the catalog file.  
2 | This <ItemID> defines the GUID for the catalog. The same GUID must be used in the registry file to identify this catalog.  
3-11 | This section defines general properties of the catalog.  
4 | <ItemName> defines the name that appears beneath the catalog icon in the catalog browser. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<ItemName>_Name_ </ItemName>”.  
5-7 | <Images> defines the image file for the icon that appears for the catalog in the catalog browser. Images used for catalogs and subassemblies should be a 64-by-64 pixel image. Valid image file types include _.bmp_ , _.gif_ , _.jpg_ , and _.png_.  
8 | <Description> contains the string description for the catalog. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<Description>_String_ </Description>”.  
10 | <Time> defines the time and date the catalog was created in the universal date/time format. This information is required, but not used. Any date or time may be given.  
12-16 | <Source> defines the source or creator of the catalog.  
17-19 | Empty definitions for Tools, Palettes, and Packages.  
20-36 | The <Categories> group defines a list of categories, each of which may contain sub-categories or subassembly tools.  
21-33 | Definition of the “Getting Started“ category. This block has been designed to load all category information from a separate file. Category information can also be placed within this file if you only want one _.atc_ file by using a <Category> section as described in the [Tool File Example](<GUID-1D0CC1CE-DB5E-427B-A2C2-485075145D5B.htm#GUID-1D0CC1CE-DB5E-427B-A2C2-485075145D5B__WS1A9193826455F5FF1D61FE411049ED455E-6F3B>)  
22 | <ItemID> defines the unique GUID for this category. It must be the same GUID as in the separate category _.atc_ file.  
23 | <Url> specifies the location of the category _.atc_ file.  
24-31 | The properties of a category.  
25 | <ItemName> defines the name of this category of tools. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<ItemName>_Name_ </ItemName>”.  
26-28 | Sets the image used to identify the category to users.  
29 | <Description> contains the string description for the category. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<Description>_String_ </Description>”.  
32 | Empty definition for Source.  
39 | Empty definition for StockTools  
  
## Tool File Example

The following is a portion of the “ _Autodesk Metric Getting Started Subassembly Catalog.atc_ ” file. It contains all the tools in the “Getting Started” catalog. This excerpt only contains the “BasicBarrier” tool.
    
    
    1)  <Category>
    2)     <ItemID idValue="{4F5BFBF8-11E8-4479-99E0-4AA69B1DC292}"/>
    3)     <Properties>
    4)        <ItemName src="AeccStockSubassemblyScriptsRC.dll" resource="9212"/>
    5)        <Images>
    6)           <Image cx="93" cy="123" src=".\Images\AeccGenericSubassemblies.png"/>
    7)        </Images>
    8)             <Description src="AeccStockSubassemblyScriptsRC.dll" resource="9213"/>
    9)        <AccessRight>1</AccessRight>
    10)       <Time createdUniversalDateTime="2002-09-16T14:23:31" modifiedUniversalDateTime="2004-06-17T07:08:09"/>
    11)    </Properties>
    12)    <CustomData/>
    13)    <Source/>
    14)    <Palettes/>
    15)    <Packages/>
    16) <Tools>
    17) <Tool>
    18)    <ItemID idValue="{F6F066F4-ABF2-4838-B007-17DFDDE2C869}"/>
    19)    <Properties>
    20)            <ItemName resource="101" src="AeccStockSubassemblyScriptsRC.dll"/>
    21)       <Images>
    22)          <Image cx="64" cy="64" src=".\Images\AeccBasicBarrier.png"/>
    23)       </Images>
    24)       <Description resource="102" src="AeccStockSubassemblyScriptsRC.dll"/>
    25)       <Keywords>_barrier subassembly</Keywords>
    26)       <Help>
    27)          <HelpFile>.\Help\C3DStockSubassemblyHelp.chm</HelpFile>
    28)          <HelpCommand>HELP_HHWND_TOPIC</HelpCommand>
    29)          <HelpData>SA_BasicBarrier.htm</HelpData>
    30)       </Help>
    31)       <Time createdUniversalDateTime="2002-04-05T21:58:00" modifiedUniversalDateTime="2002-04-05T21:58:00"/>
    32)    </Properties>
    33)    <Source/>
    34)    <StockToolRef idValue="{7F55AAC0-0256-48D7-BFA5-914702663FDE}"/>
    35)    <Data>
    36)       <AeccDbSubassembly>
    37)          <GeometryGenerateMode>UseDotNet</GeometryGenerateMode>
    38)          <DotNetClass Assembly=".\C3DStockSubassemblies.dll">Subassembly.BasicBarrier</DotNetClass>
    39)          <Resource Module="AeccStockSubassemblyScriptsRC.dll"/>
    40)          <Content DownloadLocation="http://www.autodesk.com/subscriptionlogin"/>
    41)          <Params>
    42)             <Version DataType="String" DisplayName="Version" Description="Version">R2007</Version>
    43)             <TopWidth     DataType="Double" TypeInfo="16" DisplayName="105" Description="106">0.15</TopWidth>
    44)             <MiddleWidth  DataType="Double" TypeInfo="16" DisplayName="107" Description="108">0.225</MiddleWidth>
    45)             <CurbWidth    DataType="Double" TypeInfo="16" DisplayName="109" Description="110">0.57</CurbWidth>
    46)             <BottomWidth  DataType="Double" TypeInfo="16" DisplayName="111" Description="112">0.6</BottomWidth>
    47)             <TopHeight    DataType="Double" TypeInfo="16" DisplayName="113" Description="114">0.9</TopHeight>
    48)             <MiddleHeight DataType="Double" TypeInfo="16" DisplayName="115" Description="116">0.45</MiddleHeight>
    49)             <CurbHeight   DataType="Double" TypeInfo="16" DisplayName="117" Description="118">0.075</CurbHeight>
    50)          </Params>
    51)       </AeccDbSubassembly>
    52)       <Units>m</Units>
    53)    </Data>
    54) </Tool>
    55)  
    56) <!-- Other tool items omitted -->
    57)  
    58) </Tools> 
    59) <StockTools/>
    60) </Category> 
    

Line Number | Description  
---|---  
1-59 | A <Category> is a list of subassemblies.  
2 | <ItemID> defines the unique GUID for this category. It must be the same GUID as in the parent catalog _.atc_ file.  
3-11 | The properties of a category.  
4 | <ItemName> defines the name of this category of tools. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<ItemName>_Name_ </ItemName>”.  
5-7 | Sets the image used to identify the category to users.  
8 | <Description> contains the string description for the category. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<Description>_String_ </Description>”.  
12-15 | Empty definitions for Custom Data, Source, Palettes, Packages.  
16-57 | <Tools> contains all the separate subassemblies.  
17-53 | <Tool> represents a single subassembly.  
18 | <ItemID> defines the unique GUID for this subassembly.   
19-32 | The properties of the subassembly.  
20 | <ItemName> defines the name of this subassembly. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<ItemName>_Name_ </ItemName>”.  
21-23 | Sets the image used to identify the subassembly to users.  
24 | <Description> defines the name of this subassembly. In this case, we use a string resource to support localization. You can also specify a constant string by using the line “<Description>_String_ </Description>”.  
25 | Keywords describing the subassembly.  
27 | <HelpFile> defines the filename and path of the help file.  
28 | <HelpCommand> defines the command used to display the help file.  
29 | <HelpData> is the particular topic in the help file to display.  
31 | <Time> defines the time and date the catalog was created in the universal date/time format. This information is required, but not used. Any date or time may be given.  
33 | Empty Source tag.  
34 | <StockToolRef> defines a GUID specifically for catalog tools. This must use the idVlaue of {7F55AAC0-0256-48D7-BFA5-914702663FDE}  
35-52 | Describes the nature of the subassembly.  
36-50 | Identifies the tool as a subassembly.   
37 | <GeometryGenerateMode> is a new tag that describes the source code of the subassembly. It can either have a value of “UseDotNet” or “UseVBA”. If this tag is not used, “UseVBA” is assumed.  
38 | <DotNetClass> is a new tag that lists the .NET assembly and class which contains the subassembly. The VBA equivalent is the <Macro> tag. Note that all paths specified in the ATC file must be relative paths to the ATC file itself.   
39 | The ._dll_ containing the resource strings and images used by the subassembly tool.  
40 | <Content> is a new tag that specifies a location where you can download the subassembly if it isn’t located on the local machine. If the subassembly hasn’t been downloaded, the location contained in the DownloadLocation attribute is displayed in the event viewer.  
41-50 | <Params> defines the names of the input parameters associated with the subassembly tool. This list appears in the Properties page of the subassembly, in the order they appear in the _.atc_ file. Each parameter is defined on a single line.  
42-49 |  Each parameter is described with the following: Parameter name - The internal name of the parameter (e.g., “CrownHeight”). This is the name that must be used when saving or retrieving parameters to the parameter buckets. DataType – Defines the type of variable used to store the parameter value, such as Long, Double, or String. For more information, see [Tool Catalog Data Type Information](<GUID-870042BA-5ED8-4E71-96C8-4A44C97EA5FE.htm>). DisplayName – Defines the name that is displayed for the parameter in the subassembly Properties page. This is what the user sees to identify each parameter. Description – Provides a description of the input parameter. When a parameter name is highlighted in the subassembly Properties page, the description appears at the bottom of the page. value – The default value for the parameter. This is the value that appears for the parameter in the subassembly Properties page.  
52 | <Units> describes the type of units the subassembly expects. Valid values are “m” for meters of ‘foot” for feet.
