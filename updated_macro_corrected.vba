Option Explicit

' Constants for output
Const OUTPUT_CELL As String = "A42" ' Output in cell A42
Const HTML_FILE_PATH As String = "C:\Users\Rajkumar\Downloads\output.html"

Sub GenerateBillNotes()
    Dim ws As Worksheet
    Dim agreementNumber As String
    Dim workOrderAmount As Double
    Dim uptoLastBillAmount As Double ' 17.A
    Dim thisBillAmount As Double ' 17.B
    Dim uptoDateBillAmount As Double ' 17.C (calculated)
    Dim startDate As Date
    Dim scheduleCompletion As Date
    Dim actualCompletion As Date
    Dim repairWork As String
    Dim extraItem As String
    Dim extraItemAmount As Double
    Dim excessQuantity As String
    Dim delayComment As String
    Dim percentageWorkDone As Double
    Dim timeAllowedDays As Integer
    Dim delayDays As Integer
    Dim note As String
    Dim serialNumber As Integer
    
    ' Use the active sheet (works on any sheet you copy)
    Set ws = ActiveSheet
    
    If ws Is Nothing Then
        MsgBox "No active sheet found!", vbCritical
        Exit Sub
    End If
    
    ' Extracting values from the sheet
    agreementNumber = Trim(ws.Range("C5").Value)
    
    ' Item 16: Amount of Work Order (Row 18)
    If IsNumeric(ws.Range("C18").Value) Then
        workOrderAmount = ws.Range("C18").Value
    Else
        workOrderAmount = 0
    End If
    
    ' Item 17.A: Sum of payment upto last bill (Row 19)
    If IsNumeric(ws.Range("C19").Value) Then
        uptoLastBillAmount = ws.Range("C19").Value
    Else
        uptoLastBillAmount = 0
    End If
    
    ' Item 17.B: Amount of this bill (Row 20)
    If IsNumeric(ws.Range("C20").Value) Then
        thisBillAmount = ws.Range("C20").Value
    Else
        thisBillAmount = 0
    End If
    
    ' Item 17.C: Actual expenditure upto this bill = (A + B) (Row 21)
    If IsNumeric(ws.Range("C21").Value) Then
        uptoDateBillAmount = ws.Range("C21").Value
    Else
        uptoDateBillAmount = uptoLastBillAmount + thisBillAmount
    End If
    
    ' Dates
    If IsDate(ws.Range("C13").Value) Then
        startDate = ws.Range("C13").Value
    Else
        startDate = Date
    End If
    
    If IsDate(ws.Range("C14").Value) Then
        scheduleCompletion = ws.Range("C14").Value
    Else
        scheduleCompletion = Date
    End If
    
    If IsDate(ws.Range("C15").Value) Then
        actualCompletion = ws.Range("C15").Value
    Else
        actualCompletion = scheduleCompletion
    End If
    
    ' Other fields - correct cell references after row deletions
    repairWork = ws.Range("C29").Value ' Repair/Maintenance Work
    extraItem = ws.Range("C30").Value ' Extra Item (Yes/No)
    
    ' Extra item amount
    If IsNumeric(ws.Range("C31").Value) Then
        extraItemAmount = ws.Range("C31").Value
    Else
        extraItemAmount = 0
    End If
    
    excessQuantity = ws.Range("C32").Value ' Excess Quantity
    delayComment = ws.Range("C33").Value ' Delay Comment
    
    ' Calculate percentage of work done
    If workOrderAmount > 0 Then
        percentageWorkDone = (uptoDateBillAmount / workOrderAmount) * 100
    Else
        percentageWorkDone = 0
    End If
    
    ' Calculate time allowed for execution
    timeAllowedDays = DateDiff("d", startDate, scheduleCompletion)
    
    ' Calculate delay in execution
    delayDays = DateDiff("d", scheduleCompletion, actualCompletion)
    
    ' Initialize Notes
    serialNumber = 1
    note = serialNumber & ". The work has been completed " & Format(percentageWorkDone, "0.00") & "% of the Work Order Amount." & vbNewLine
    serialNumber = serialNumber + 1
    
    ' Conditions based on work percentage
    If percentageWorkDone < 90 Then
        note = note & serialNumber & ". The execution of work at final stage is less than 90% of the Work Order Amount, the Requisite Deviation Statement is enclosed to observe check on unuseful expenditure. Approval of the Deviation is having jurisdiction under this office." & vbNewLine
        serialNumber = serialNumber + 1
    ElseIf percentageWorkDone > 100 And percentageWorkDone <= 105 Then
        note = note & serialNumber & ". Requisite Deviation Statement is enclosed. The Overall Excess is less than or equal to 5% and is having approval jurisdiction under this office." & vbNewLine
        serialNumber = serialNumber + 1
    ElseIf percentageWorkDone > 105 Then
        note = note & serialNumber & ". Requisite Deviation Statement is enclosed. The Overall Excess is more than 5% and Approval of the Deviation Case is required from the Superintending Engineer, PWD Electrical Circle, Udaipur." & vbNewLine
        serialNumber = serialNumber + 1
    End If
    
    ' Handling delay conditions
    If delayDays > 0 Then
        note = note & serialNumber & ". Time allowed for completion of the work was " & timeAllowedDays & " days. The Work was delayed by " & delayDays & " days." & vbNewLine
        serialNumber = serialNumber + 1
        
        ' Check if delay is more than 50% of allowed time
        If delayDays > (0.5 * timeAllowedDays) Then
            note = note & serialNumber & ". Approval of the Time Extension Case is required from the Superintending Engineer, PWD Electrical Circle, Udaipur." & vbNewLine
        Else
            note = note & serialNumber & ". Approval of the Time Extension Case is to be done by this office." & vbNewLine
        End If
        serialNumber = serialNumber + 1
    Else
        note = note & serialNumber & ". Work was completed in time." & vbNewLine
        serialNumber = serialNumber + 1
    End If
    
    ' Extra item conditions
    If extraItem = "Yes" Then
        Dim extraItemPercentage As Double
        If workOrderAmount > 0 Then
            extraItemPercentage = (extraItemAmount / workOrderAmount) * 100
        Else
            extraItemPercentage = 0
        End If
        
        If extraItemPercentage > 5 Then
            note = note & serialNumber & ". The amount of Extra items is Rs. " & extraItemAmount & " which is " & Format(extraItemPercentage, "0.00") & "% of the Work Order Amount; exceed 5%, require approval from the Superintending Engineer, PWD Electrical Circle, Udaipur." & vbNewLine
        Else
            note = note & serialNumber & ". The amount of Extra items is Rs. " & extraItemAmount & " which is " & Format(extraItemPercentage, "0.00") & "% of the Work Order Amount; under 5%, approval of the same is to be granted by this office." & vbNewLine
        End If
        serialNumber = serialNumber + 1
    End If
    
    ' Excess quantity conditions
    If excessQuantity = "Yes" Then
        If percentageWorkDone <= 100 Then
            Dim overallSaving As Double
            overallSaving = 100 - percentageWorkDone
            note = note & serialNumber & ". The details of the items wherein EXCESS QUANTITY has been executed during the work completion are attached. There is a saving in the work of the tune of " & Format(overallSaving, "0.00") & "%; (i.e., Overall Excess = NIL, just excess quantity items are recorded), the approval of which falls under the jurisdiction of this office." & vbNewLine
        Else
            Dim overallExcess As Double
            overallExcess = percentageWorkDone - 100
            note = note & serialNumber & ". The details of the items wherein EXCESS QUANTITY has been executed during the work completion are attached. There is an Overall excess of " & Format(overallExcess, "0.00") & "% requires approval as already narrated." & vbNewLine
        End If
        serialNumber = serialNumber + 1
    End If
    
    ' Mandatory conditions
    note = note & serialNumber & ". Quality Control (QC) test reports attached." & vbNewLine
    serialNumber = serialNumber + 1
    
    If repairWork = "No" Then
        note = note & serialNumber & ". A copy of Hand Over statement duly signed by client department representative is attached." & vbNewLine
        serialNumber = serialNumber + 1
    End If
    
    If delayComment = "Yes" Then
        note = note & serialNumber & ". The Bill is submitted very late; explanation from concerned Assistant Engineer may be sought." & vbNewLine
        serialNumber = serialNumber + 1
    End If
    
    note = note & serialNumber & ". Please peruse above details for necessary decision-making." & vbNewLine
    note = note & " " & vbNewLine
    note = note & "                      Premlata Jain" & vbNewLine
    note = note & "                     AAO- As Auditor" & vbNewLine
    
    ' Set row 42 height to 315
    ws.Rows(42).RowHeight = 315
    
    ' Output note to Excel (cell A42)
    ws.Range(OUTPUT_CELL).Value = note
    ws.Range(OUTPUT_CELL).WrapText = True
    ws.Range(OUTPUT_CELL).VerticalAlignment = xlTop
    ws.Range(OUTPUT_CELL).HorizontalAlignment = xlLeft
    
    ' Merge cells A42:D42 for the note
    ws.Range("A42:D42").Merge
    ws.Range("A42:D42").WrapText = True
    ws.Range("A42:D42").VerticalAlignment = xlTop
    
    ' Set page setup for printing A1:D40 on one A4 portrait page
    With ws.PageSetup
        .PrintArea = "$A$1:$D$40"
        .Orientation = xlPortrait
        .PaperSize = xlPaperA4
        .FitToPagesWide = 1
        .FitToPagesTall = 1
        ' No header, no footer
        .LeftHeader = ""
        .CenterHeader = ""
        .RightHeader = ""
        .LeftFooter = ""
        .CenterFooter = ""
        .RightFooter = ""
        ' Margins: Left 15mm, Right 10mm, Top 10mm, Bottom 0mm
        .LeftMargin = Application.CentimetersToPoints(1.5)   ' 15 mm = 1.5 cm
        .RightMargin = Application.CentimetersToPoints(1.0)  ' 10 mm = 1.0 cm
        .TopMargin = Application.CentimetersToPoints(1.0)    ' 10 mm = 1.0 cm
        .BottomMargin = 0                                     ' 0 mm
        .HeaderMargin = 0
        .FooterMargin = 0
        .PrintGridlines = False
        .PrintHeadings = False
        .Zoom = False  ' Use FitToPages instead
    End With
    
    ' Optional: Save as HTML file
    Dim fileNum As Integer
    fileNum = FreeFile
    Open HTML_FILE_PATH For Output As #fileNum
    Print #fileNum, "<pre>" & note & "</pre>"
    Close #fileNum
    
    MsgBox "Bill note generated successfully!" & vbNewLine & _
           "Output in cell A42" & vbNewLine & _
           "Page setup: A1:D40, A4 Portrait, No Header/Footer" & vbNewLine & _
           "Margins: Left 15mm, Right 10mm, Top 10mm, Bottom 0mm", vbInformation
End Sub
