<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Sample VB.NET Subassembly  -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-03ADCEE6-5B64-4BD2-96A2-79A9EC16F73D.htm -->

# Sample VB.NET Subassembly 

The following class module defines the BasicLaneTransition subassembly provided in the Stock Subassemblies catalog. The original source code for this and all other subassemblies that come with Autodesk Civil 3D can be found in the _< Autodesk Civil 3D Install Directory>\Sample\Civil 3D API\C3DStockSubAssemblies\Subassemblies_ directory.

Before reviewing the code you should familiarize yourself with the subassembly, how it behaves in the cut and fill conditions, the point and link codes to be assigned, and the point and link numbers specified in the subassembly coding diagram. Refer to the BasicLaneTransition subassembly Help for this information.
    
    
    Option Explicit On
    Option Strict Off
    Imports System.Math
    Imports DBTransactionManager = Autodesk.AutoCAD.DatabaseServices.TransactionManager
    ' *************************************************************************
    ' *************************************************************************
    ' *************************************************************************
    '          Name: BasicLaneTransition
    '
    '   Description: Creates a simple cross-sectional representation of a corridor
    '                lane composed of a single closed shape.  Attachment origin
    '                is at top, most inside portion of lane.  The lane can
    '                transition its width and cross-slope based on the position
    '                supplied by an optional horizontal and vertical alignment.
    '
    ' Logical Names: Name        Type     Optional   Default value    Description
    '                --------------------------------------------------------------
    '                TargetHA    Alg      yes        none             Horizontal alignment to transition to
    '                TargetVA    Profile  yes        none             Vertical alignment to transition to
    '
    '    Parameters: Name            Type     Optional    Default Value    Description
    '                ------------------------------------------------------------------
    '                Side            long     yes        Right           specifies side to place SA on
    '                Width           double   yes        12.0             width of lane
    '                Depth           double   yes         0.667           depth of coarse
    '                Slope           double   yes        -0.02               cross-slope of lane
    '                TransitionType  long     yes        2                hold grade, move to offset HA
    '                InsertionPoint  long     yes        kCrown           Specifies insertion point of the lane either at (a) Crown or (b) Edge of Travel Way
    '                CrownPtOnInside Long     no         g_iTrue         Specifies that inside edge of travelway to be coded as Crown
    ' *************************************************************************
    Public Class BasicLaneTransition
        Inherits SATemplate
        Private Enum InsertionPoint
            kCrown = 0
            kEdgeOfTravelWay = 1
        End Enum
        Private Enum TransitionTypes ' Transition types supported
            kHoldOffsetAndElevation = 0
            kHoldElevationChangeOffset = 1
            kHoldGradeChangeOffset = 2
            kHoldOffsetChangeElevation = 3
            kChangeOffsetAndElevation = 4
        End Enum
        ' --------------------------------------------------------------------------
        ' Default values for input parameters
        Private Const SideDefault = Utilities.Right
        Private Const InsertionPointDefault = InsertionPoint.kCrown
        Private Const CrownPtOnInsideDefault = Utilities.IFalse
        Private Const LaneWidthDefault = 12.0#
        Private Const LaneDepthDefault = 0.667
        Private Const LaneSlopeDefault = -0.02    '0.25 inch per foot
        Private Const HoldOriginalPositionDefault = TransitionTypes.kHoldOffsetAndElevation
        Protected Overrides Sub GetLogicalNamesImplement(ByVal corridorState As CorridorState)
            MyBase.GetLogicalNamesImplement(corridorState)
            ' Retrieve parameter buckets from the corridor state
            Dim oParamsLong As ParamLongCollection
            oParamsLong = corridorState.ParamsLong
            ' Add the logical names we use in this script
            Dim oParamLong As ParamLong
            oParamLong = oParamsLong.Add("TargetHA", ParamLogicalNameType.OffsetTarget)
            oParamLong.DisplayName = "690"
            oParamLong = oParamsLong.Add("TargetVA", ParamLogicalNameType.ElevationTarget)
            oParamLong.DisplayName = "691"
        End Sub
        Protected Overrides Sub GetInputParametersImplement(ByVal corridorState As CorridorState)
            MyBase.GetInputParametersImplement(corridorState)
            ' Retrieve parameter buckets from the corridor state
            Dim oParamsLong As ParamLongCollection
            oParamsLong = corridorState.ParamsLong
            Dim oParamsDouble As ParamDoubleCollection
            oParamsDouble = corridorState.ParamsDouble
            ' Add the input parameters we use in this script
            oParamsLong.Add(Utilities.Side, SideDefault)
            oParamsLong.Add("InsertionPoint", InsertionPointDefault)
            oParamsLong.Add("CrownPtOnInside", CrownPtOnInsideDefault)
            oParamsDouble.Add("Width", LaneWidthDefault)
            oParamsDouble.Add("Depth", LaneDepthDefault)
            oParamsDouble.Add("Slope", LaneSlopeDefault)
            oParamsLong.Add("TransitionType", HoldOriginalPositionDefault)
        End Sub
        Protected Overrides Sub DrawImplement(ByVal corridorState As CorridorState)
            ' Retrieve parameter buckets from the corridor state
            Dim oParamsDouble As ParamDoubleCollection
            oParamsDouble = corridorState.ParamsDouble
            Dim oParamsLong As ParamLongCollection
            oParamsLong = corridorState.ParamsLong
            Dim oParamsOffsetTarget As ParamOffsetTargetCollection
            oParamsOffsetTarget = corridorState.ParamsOffsetTarget
            Dim oParamsElevationTarget As ParamElevationTargetCollection
            oParamsElevationTarget = corridorState.ParamsElevationTarget
            '---------------------------------------------------------
            ' flip about Y-axis
            Dim vSide As Long
            Try
                vSide = oParamsLong.Value(Utilities.Side)
            Catch
                vSide = SideDefault
            End Try
            Dim dFlip As Double
            dFlip = 1.0#
            If vSide = Utilities.Left Then
                dFlip = -1.0#
            End If
            '---------------------------------------------------------
            ' Transition type
            Dim vTransitionType As Long
            Try
                vTransitionType = oParamsLong.Value("TransitionType")
            Catch
                vTransitionType = HoldOriginalPositionDefault
            End Try
            '---------------------------------------------------------
            ' Insertion Ponit
            Dim vInsertionPoint As Long
            Try
                vInsertionPoint = oParamsLong.Value("InsertionPoint")
            Catch
                vInsertionPoint = InsertionPointDefault
            End Try
            Dim vCrownPtOnInside As Long
            Try
                vCrownPtOnInside = oParamsLong.Value("CrownPtOnInside")
            Catch
                vCrownPtOnInside = CrownPtOnInsideDefault
            End Try
            '---------------------------------------------------------
            ' BasicLaneTransition dimensions
            Dim vWidth As Double
            Try
                vWidth = oParamsDouble.Value("Width")
            Catch
                vWidth = LaneWidthDefault
            End Try
            Dim vDepth As Double
            Try
                vDepth = oParamsDouble.Value("Depth")
            Catch
                vDepth = LaneDepthDefault
            End Try
            Dim vSlope As Double
            Try
                vSlope = oParamsDouble.Value("Slope")
            Catch
                vSlope = LaneSlopeDefault
            End Try
            '-------------------------------------------------------
            ' Get version, and convert values if necessary
            Dim sVersion As String
            sVersion = Utilities.GetVersion(corridorState)
            If sVersion <> Utilities.R2005 Then
                'need not change
            Else
                'R2005
                'convert %slope to tangent value
                vSlope = vSlope / 100
            End If
            Dim nVersion As Integer
            nVersion = Utilities.GetVersionInt(corridorState)
            If nVersion < 2010 Then
                vCrownPtOnInside = Utilities.ITrue
            End If
            '---------------------------------------------------------
            ' Check user input
            If vWidth <= 0 Then
                Utilities.RecordError(corridorState, CorridorError.ValueShouldNotBeLessThanOrEqualToZero, "Width", "BasicLaneTransition")
                vWidth = LaneWidthDefault
            End If
            If vDepth <= 0 Then
                Utilities.RecordError(corridorState, CorridorError.ValueShouldNotBeLessThanOrEqualToZero, "Depth", "BasicLaneTransition")
                vDepth = LaneDepthDefault
            End If
            ' Calculate the current alignment and origin according to the assembly offset
            Dim oCurrentAlignmentId As ObjectId
            Dim oOrigin As New PointInMem
            Utilities.GetAlignmentAndOrigin(corridorState, oCurrentAlignmentId, oOrigin)
            '---------------------------------------------------------
            ' Define codes for points, links and shapes
            Dim sPointCodeArray(0 To 4, 0) As String
            Dim sLinkCodeArray(0 To 2, 0 To 1) As String
            Dim sShapeCodeArray(0 To 1) As String
            FillCodesFromTable(sPointCodeArray, sLinkCodeArray, sShapeCodeArray, vCrownPtOnInside)
            '---------------------------------------------------------
            ' Get alignment and profile we're currently working from
            Dim offsetTarget As WidthOffsetTarget 'width or offset target
            offsetTarget = Nothing
            Dim elevationTarget As SlopeElevationTarget 'slope or elvation target
            elevationTarget = Nothing
            Dim dOffsetToTargetHA As Double
            Dim dOffsetElev As Double
            If corridorState.Mode = CorridorMode.Layout Then
                vTransitionType = TransitionTypes.kHoldOffsetAndElevation
            End If
            Dim dXOnTarget As Double
            Dim dYOnTarget As Double
            Select Case vTransitionType
                Case TransitionTypes.kHoldOffsetAndElevation
                Case TransitionTypes.kHoldElevationChangeOffset
                    'oHA must exist
                    Try
                        offsetTarget = oParamsOffsetTarget.Value("TargetHA")
                    Catch
                        'Utilities.RecordError(corridorState, CorridorError.ParameterNotFound, "Edge Offset", "BasicLaneTransition")
                        'Exit Sub
                    End Try
                    'get offset to targetHA
                    If False = Utilities.CalcAlignmentOffsetToThisAlignment(oCurrentAlignmentId, corridorState.CurrentStation, offsetTarget, Utilities.GetSide(vSide), dOffsetToTargetHA, dXOnTarget, dYOnTarget) Then
                        Utilities.RecordWarning(corridorState, CorridorError.LogicalNameNotFound, "TargetHA", "BasicLaneTransition")
                        dOffsetToTargetHA = vWidth + oOrigin.Offset
                    Else
                        If (dOffsetToTargetHA = oOrigin.Offset) Or ((dOffsetToTargetHA > oOrigin.Offset) And (vSide = Utilities.Left)) Or _
                            ((dOffsetToTargetHA < oOrigin.Offset) And (vSide = Utilities.Right)) Then
                            Utilities.RecordWarning(corridorState, CorridorError.ValueInABadPosition, "TargetHA", "BasicLaneTransition")
                            dOffsetToTargetHA = vWidth + oOrigin.Offset
                        End If
                    End If
                Case TransitionTypes.kHoldGradeChangeOffset
                    'oHA must exist
                    Try
                        offsetTarget = oParamsOffsetTarget.Value("TargetHA")
                    Catch
                        'Utilities.RecordError(corridorState, CorridorError.ParameterNotFound, "Edge Offset", "BasicLaneTransition")
                        'Exit Sub
                    End Try
                    'get offset to targetHA
                    If False = Utilities.CalcAlignmentOffsetToThisAlignment(oCurrentAlignmentId, corridorState.CurrentStation, offsetTarget, Utilities.GetSide(vSide), dOffsetToTargetHA, dXOnTarget, dYOnTarget) Then
                        Utilities.RecordWarning(corridorState, CorridorError.LogicalNameNotFound, "TargetHA", "BasicLaneTransition")
                        dOffsetToTargetHA = vWidth + oOrigin.Offset
                    Else
                        If (((dOffsetToTargetHA > oOrigin.Offset) And (vSide = Utilities.Left)) Or _
                            ((dOffsetToTargetHA < oOrigin.Offset) And (vSide = Utilities.Right))) Then
                            Utilities.RecordWarning(corridorState, CorridorError.ValueInABadPosition, "TargetHA", "BasicLaneTransition")
                            dOffsetToTargetHA = vWidth + oOrigin.Offset
                        End If
                    End If
                Case TransitionTypes.kHoldOffsetChangeElevation
                    'oVA must exist
                    Try
                        elevationTarget = oParamsElevationTarget.Value("TargetVA")
                    Catch
                        'Utilities.RecordError(corridorState, CorridorError.ParameterNotFound, "Edge Elevation", "BasicLaneTransition")
                        'Exit Sub
                    End Try
                    Dim db As Database = HostApplicationServices.WorkingDatabase
                    Dim tm As DBTransactionManager = db.TransactionManager
                    Dim oProfile As Profile = Nothing
                    'get elevation on elevationTarget
                    Try
                        dOffsetElev = elevationTarget.GetElevation(oCurrentAlignmentId, corridorState.CurrentStation, Utilities.GetSide(vSide))
                    Catch
                        Utilities.RecordWarning(corridorState, CorridorError.LogicalNameNotFound, "TargetHA", "BasicLaneTransition")
                        dOffsetElev = corridorState.CurrentElevation + vWidth * vSlope
                    End Try
                Case TransitionTypes.kChangeOffsetAndElevation
                    'both oHA and oVA must exist
                    Try
                        offsetTarget = oParamsOffsetTarget.Value("TargetHA")
                    Catch
                        'Utilities.RecordError(corridorState, CorridorError.ParameterNotFound, "Edge Offset", "BasicLaneTransition")
                        'Exit Sub
                    End Try
                    Try
                        elevationTarget = oParamsElevationTarget.Value("TargetVA")
                    Catch
                        'Utilities.RecordError(corridorState, CorridorError.ParameterNotFound, "Edge Elevation", "BasicLaneTransition")
                        'Exit Sub
                    End Try
                    'get elevation on elevationTarget
                    Try
                        dOffsetElev = elevationTarget.GetElevation(oCurrentAlignmentId, corridorState.CurrentStation, Utilities.GetSide(vSide))
                    Catch
                        Utilities.RecordWarning(corridorState, CorridorError.LogicalNameNotFound, "TargetHA", "BasicLaneTransition")
                        dOffsetElev = corridorState.CurrentElevation + vWidth * vSlope
                    End Try
                    'get offset to targetHA
                    If False = Utilities.CalcAlignmentOffsetToThisAlignment(oCurrentAlignmentId, corridorState.CurrentStation, offsetTarget, Utilities.GetSide(vSide), dOffsetToTargetHA, dXOnTarget, dYOnTarget) Then
                        Utilities.RecordWarning(corridorState, CorridorError.LogicalNameNotFound, "TargetHA", "BasicLaneTransition")
                        dOffsetToTargetHA = vWidth + oOrigin.Offset
                    Else
                        If (dOffsetToTargetHA = oOrigin.Offset) Or ((dOffsetToTargetHA > oOrigin.Offset) And (vSide = Utilities.Left)) Or _
                            ((dOffsetToTargetHA < oOrigin.Offset) And (vSide = Utilities.Right)) Then
                            Utilities.RecordWarning(corridorState, CorridorError.ValueInABadPosition, "TargetHA", "BasicLaneTransition")
                            dOffsetToTargetHA = vWidth + oOrigin.Offset
                        End If
                    End If
            End Select
            '---------------------------------------------------------
            ' Create the subassembly points
            Dim corridorPoints As PointCollection
            corridorPoints = corridorState.Points
            Dim dX As Double
            Dim dy As Double
            dX = 0.0#
            dy = 0.0#
            Dim oPoint1 As Point
            oPoint1 = corridorPoints.Add(dX, dy, "")
            ' compute outside position of lane
            Select Case vTransitionType
                Case TransitionTypes.kHoldOffsetAndElevation
                    ' hold original position (always used in layout mode)
                    dX = vWidth
                    dy = Abs(vWidth) * vSlope
                Case TransitionTypes.kHoldElevationChangeOffset
                    ' hold original elevation, move offset to that of TargetHA
                    'dX = Abs(dOffsetToTargetHA - corridorState.CurrentSubassemblyOffset)
                    dX = Abs(dOffsetToTargetHA - oOrigin.Offset)
                    dy = Abs(vWidth) * vSlope
                Case TransitionTypes.kHoldGradeChangeOffset
                    ' hold original grade, move offset to that of TargetHA
                    ' (also used if TargetVA is not defined)
                    'dX = Abs(dOffsetToTargetHA - corridorState.CurrentSubassemblyOffset)
                    dX = Abs(dOffsetToTargetHA - oOrigin.Offset)
                    dy = Abs(dX) * vSlope
                Case TransitionTypes.kHoldOffsetChangeElevation
                    ' hold original offset, but change elevation to that of TargetVA
                    dX = vWidth
                    'dY = dOffsetElev - corridorState.CurrentSubassemblyElevation
                    dy = dOffsetElev - oOrigin.Elevation
                Case TransitionTypes.kChangeOffsetAndElevation
                    ' move position to that of TargetHA, and elevation to that of TargetVA
                    dX = Abs(dOffsetToTargetHA - oOrigin.Offset)
                    dy = dOffsetElev - oOrigin.Elevation
            End Select
            '------------------------------------------------------------------
            Dim dActualWidth As Double
            dActualWidth = dX
            Dim dActualSlope As Double
            If 0 = dActualWidth Then
                dActualSlope = 0.0#
            Else
                dActualSlope = dy / Abs(dActualWidth)
            End If
            '------------------------------------------------------------------
            Dim oPoint2 As Point
            oPoint2 = corridorPoints.Add(dX * dFlip, dy, "")
            dX = dX - 0.001
            dy = dy - vDepth
            Dim oPoint3 As Point
            oPoint3 = corridorPoints.Add(dX * dFlip, dy, "")
            dX = 0.0#
            dy = -vDepth
            Dim oPoint4 As Point
            oPoint4 = corridorPoints.Add(dX, dy, "")
            If vInsertionPoint = InsertionPoint.kCrown Then
                Utilities.AddCodeToPoint(1, corridorPoints, oPoint1.Index, sPointCodeArray)
                Utilities.AddCodeToPoint(2, corridorPoints, oPoint2.Index, sPointCodeArray)
                Utilities.AddCodeToPoint(3, corridorPoints, oPoint3.Index, sPointCodeArray)
                Utilities.AddCodeToPoint(4, corridorPoints, oPoint4.Index, sPointCodeArray)
            Else
                Utilities.AddCodeToPoint(2, corridorPoints, oPoint1.Index, sPointCodeArray)
                Utilities.AddCodeToPoint(1, corridorPoints, oPoint2.Index, sPointCodeArray)
                Utilities.AddCodeToPoint(4, corridorPoints, oPoint3.Index, sPointCodeArray)
                Utilities.AddCodeToPoint(3, corridorPoints, oPoint4.Index, sPointCodeArray)
            End If
            '---------------------------------------------------------
            ' Create the subassembly links
            Dim oCorridorLinks As LinkCollection
            oCorridorLinks = corridorState.Links
            Dim oPoint(1) As Point
            Dim oLink(3) As Link
            oPoint(0) = oPoint1
            oPoint(1) = oPoint2
            oLink(0) = oCorridorLinks.Add(oPoint, "") 'L1
            oPoint(0) = oPoint2
            oPoint(1) = oPoint3
            oLink(1) = oCorridorLinks.Add(oPoint, "") 'L2
            oPoint(0) = oPoint3
            oPoint(1) = oPoint4
            oLink(2) = oCorridorLinks.Add(oPoint, "") 'L3
            oPoint(0) = oPoint4
            oPoint(1) = oPoint1
            oLink(3) = oCorridorLinks.Add(oPoint, "") 'L4
            Utilities.AddCodeToLink(1, oCorridorLinks, oLink(0).Index, sLinkCodeArray)
            Utilities.AddCodeToLink(2, oCorridorLinks, oLink(2).Index, sLinkCodeArray)
            '---------------------------------------------------------
            ' Create the subassembly shapes
            Dim corridorShapes As ShapeCollection
            corridorShapes = corridorState.Shapes
            corridorShapes.Add(oLink, sShapeCodeArray(1))
            '---------------------------------------------------------
            '---------------------------------------------------------
            ' Write back all the Calculated values of the input parameters into the RoadwayState object.
            ' Because they may be different from the default design values,
            ' we should write them back to make sure that the RoadwayState object
            ' contains the Actual information of the parameters.
            oParamsLong.Add(Utilities.Side, vSide)
            oParamsLong.Add("InsertionPoint", vInsertionPoint)
            oParamsLong.Add("CrownPtOnInside", vCrownPtOnInside)
            oParamsDouble.Add("Width", Math.Abs(dActualWidth))
            oParamsDouble.Add("Depth", vDepth)
            oParamsDouble.Add("Slope", dActualSlope)
            oParamsLong.Add("TransitionType", vTransitionType)
        End Sub
        Protected Sub FillCodesFromTable(ByVal sPointCodeArray(,) As String, ByVal sLinkCodeArray(,) As String, ByVal sShapeCodeArray() As String, ByVal CrownPtOnInside As Long)
            If CrownPtOnInside = Utilities.ITrue Then
                sPointCodeArray(1, 0) = Codes.Crown.Code
            Else
                sPointCodeArray(1, 0) = ""
            End If
            sPointCodeArray(2, 0) = Codes.ETW.Code
            sPointCodeArray(3, 0) = Codes.ETWSubBase.Code 'P4
            If CrownPtOnInside = Utilities.ITrue Then
                sPointCodeArray(4, 0) = Codes.CrownSubBase.Code 'P3
            Else
                sPointCodeArray(4, 0) = "" 'P3
            End If
            sLinkCodeArray(1, 0) = Codes.Top.Code
            sLinkCodeArray(1, 1) = Codes.Pave.Code
            sLinkCodeArray(2, 0) = Codes.Datum.Code
            sLinkCodeArray(2, 1) = Codes.SubBase.Code
            sShapeCodeArray(1) = Codes.Pave1.Code
        End Sub
    End Class
