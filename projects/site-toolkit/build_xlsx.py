"""Builds the Site Estimation Toolkit .xlsx (all live formulas). Usage: build_xlsx.py OUT.xlsx"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
HDR = PatternFill("solid", fgColor="3B2A6B"); INP = PatternFill("solid", fgColor="FFF8D6"); TOT = PatternFill("solid", fgColor="E6E0F5")
thin = Side(style="thin", color="BBBBBB"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

def sheet(name, widths, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = name
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = w
    return ws

def head(ws, row, labels):
    for c, t in enumerate(labels, 1):
        x = ws.cell(row, c, t); x.font = Font(bold=True, color="FFFFFF"); x.fill = HDR
        x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = BOX

def title(ws, text, note=None):
    ws["A1"] = text; ws["A1"].font = Font(bold=True, size=14, color="3B2A6B")
    if note: ws["A2"] = note; ws["A2"].font = Font(italic=True, color="666666")

def inputs(ws, rng):
    for row in ws[rng]:
        for c in row: c.fill = INP; c.border = BOX

# ---------- 0 START ----------
ws = sheet("START HERE", [110], True)
lines = ["SITE ESTIMATION TOOLKIT: BOQ, BBS, Rate Analysis & RA Bill", "",
 "Peele (yellow) cells = aapko bharna hai. Baaki sab formula hai, mat badlo.",
 "1. Measurement: Nos x L x B x D se quantity (Deduct choose karo to minus ho jayega).",
 "2. BBS: bar ka dia, nos aur length daalo; weight = d x d / 162 kg/m se apne aap. Neeche dia-wise summary.",
 "3. Stirrup: beam/column size aur cover daalo, cutting length mil jayega.",
 "4. Rate Analysis: mix ratio, labour aur material rate apne shehar ke daalo; per m3 rate banta hai.",
 "5. BOQ: item quantity x rate, contingency, GST, grand total. Material requirement bhi niche.",
 "6. RA Bill: upto-date quantity daalo; this bill = upto date - previous; retention, GST, TDS, net payable.",
 "7. Material Tracker aur Project Summary: stock aur total ek nazar mein.", "",
 "ZAROORI: Sab rate, hook allowance, bend deduction, wastage aur % sirf EXAMPLE hain. Apne shehar ke rate / DSR / IS code aur drawing se check karke badlo.",
 "Ye toolkit calculation ka madadgaar hai; final estimate aur bill ki zimmedari aapki (engineer/contractor) ki hai.",
 "Google Sheets mein bhi chalta hai (File > Import)."]
for i, t in enumerate(lines, 1):
    ws.cell(i, 1, t).alignment = Alignment(wrap_text=True)
ws["A1"].font = Font(bold=True, size=15, color="3B2A6B")

# ---------- 1 MEASUREMENT ----------
ws = sheet("Measurement", [8, 34, 8, 10, 10, 10, 10, 11, 9])
title(ws, "Measurement Sheet", "Qty = Nos x L x B x D (blank dimension = 1). Deduct = minus.")
head(ws, 4, ["Sr", "Description", "Nos", "L (m)", "B (m)", "D/H (m)", "Add/Deduct", "Qty", "Unit"])
data = [("Excavation for footings", 4, 1.5, 1.5, 1.2, "Add", "m3"), ("PCC 1:4:8 under footings", 4, 1.7, 1.7, 0.1, "Add", "m3"),
        ("Brick masonry in superstructure", 1, 20, 0.23, 3, "Add", "m3"), ("Deduct door opening", 2, 1.0, 0.23, 2.1, "Deduct", "m3"),
        ("Plaster (both faces)", 2, 20, None, 3, "Add", "m2")]
for r in range(5, 25):
    ws.cell(r, 1, r - 4)
    if r - 5 < len(data):
        d = data[r - 5]
        for c, v in zip([2, 3, 4, 5, 6, 7, 9], [d[0], d[1], d[2], d[3], d[4], d[5], d[6]]): ws.cell(r, c, v)
    ws.cell(r, 8, f'=IF(C{r}="","",ROUND(IF(G{r}="Deduct",-1,1)*C{r}*IF(D{r}="",1,D{r})*IF(E{r}="",1,E{r})*IF(F{r}="",1,F{r}),3))')
inputs(ws, "B5:G24"); inputs(ws, "I5:I24")
dv = DataValidation(type="list", formula1='"Add,Deduct"', allow_blank=True); ws.add_data_validation(dv); dv.add("G5:G24")
ws["G26"] = "Total (same unit only)"; ws["H26"] = "=SUM(H5:H24)"; ws["H26"].fill = TOT

# ---------- 2 BBS ----------
ws = sheet("BBS", [8, 24, 9, 9, 11, 13, 11, 12])
title(ws, "Bar Bending Schedule", "Weight per metre = d x d / 162 (d in mm).")
head(ws, 4, ["Mark", "Member", "Dia (mm)", "Nos", "Cut length (m)", "Total length (m)", "Wt/m (kg)", "Weight (kg)"])
bb = [("B1", "Beam bottom bars", 16, 8, 4.8), ("B2", "Beam top bars", 12, 6, 4.8), ("S1", "Stirrups", 8, 30, 1.2), ("C1", "Column main bars", 20, 12, 3.6)]
for r in range(5, 35):
    if r - 5 < len(bb):
        for c, v in enumerate(bb[r - 5], 1): ws.cell(r, c, v)
    ws.cell(r, 6, f'=IF(D{r}="","",D{r}*E{r})'); ws.cell(r, 7, f'=IF(C{r}="","",ROUND(C{r}*C{r}/162,4))')
    ws.cell(r, 8, f'=IF(D{r}="","",ROUND(F{r}*G{r},2))')
inputs(ws, "A5:E34")
ws["G36"] = "Total steel (kg)"; ws["H36"] = "=SUM(H5:H34)"; ws["H36"].fill = TOT
ws["G37"] = "Total (quintal)"; ws["H37"] = "=ROUND(H36/100,3)"
ws["J4"], ws["K4"], ws["L4"] = "Dia-wise", "Weight (kg)", "Wt (tonne)"
for c in "JKL": ws[f"{c}4"].font = Font(bold=True, color="FFFFFF"); ws[f"{c}4"].fill = HDR
for i, d in enumerate([6, 8, 10, 12, 16, 20, 25, 32]):
    r = 5 + i; ws[f"J{r}"] = d; ws[f"K{r}"] = f"=SUMIF($C$5:$C$34,J{r},$H$5:$H$34)"; ws[f"L{r}"] = f"=ROUND(K{r}/1000,3)"
ws["J14"] = "Total"; ws["K14"] = "=SUM(K5:K12)"; ws["K14"].fill = TOT
ws["J15"] = "Check (must be 0)"; ws["K15"] = "=ROUND(K14-H36,2)"
for c, w in zip("JKL", [18, 12, 12]): ws.column_dimensions[c].width = w
# stirrup calculator
ws["A40"] = "Stirrup cutting length calculator (inputs are EXAMPLES, confirm with your engineer / IS 2502 / SP 34)"; ws["A40"].font = Font(bold=True, color="3B2A6B")
rows = [("Member width (mm)", 230), ("Member depth (mm)", 450), ("Clear cover (mm)", 25), ("Stirrup dia d (mm)", 8),
        ("Hook allowance per hook (x d)", 10), ("Bend deduction per 90 deg bend (x d)", 1), ("Bend deduction per 135 deg bend (x d)", 1.5),
        ("No. of 90 deg bends", 3), ("No. of 135 deg bends", 2)]
for i, (k, v) in enumerate(rows):
    r = 41 + i; ws[f"A{r}"] = k; ws[f"E{r}"] = v; ws.merge_cells(f"A{r}:D{r}")
inputs(ws, "E41:E49")
ws["A51"] = "Inner width a (mm)"; ws["E51"] = "=E41-2*E43"
ws["A52"] = "Inner depth b (mm)"; ws["E52"] = "=E42-2*E43"
ws["A53"] = "Cutting length (mm)"; ws["E53"] = "=2*(E51+E52)+2*E45*E44-(E48*E46+E49*E47)*E44"
ws["A54"] = "Cutting length (m)"; ws["E54"] = "=ROUND(E53/1000,3)"; ws["E54"].fill = TOT
for r in range(51, 55): ws.merge_cells(f"A{r}:D{r}")

# ---------- 3 RATE ANALYSIS ----------
ws = sheet("Rate Analysis", [40, 12, 12, 14])
title(ws, "Rate Analysis: concrete per m3 (all rates are EXAMPLES: put your city's rates)")
rows = [("Mix ratio: cement", 1), ("Mix ratio: sand", 1.5), ("Mix ratio: aggregate", 3), ("Dry volume factor (example 1.54)", 1.54),
        ("Cement density (kg/m3)", 1440), ("Cement bag (kg)", 50)]
for i, (k, v) in enumerate(rows):
    ws[f"A{3+i}"] = k; ws[f"B{3+i}"] = v
inputs(ws, "B3:B8")
ws["A10"] = "Material per 1 m3 concrete"; ws["A10"].font = Font(bold=True)
head(ws, 11, ["Item", "Qty", "Unit", "Rate (Rs)"])
ws["D11"].value = "Rate (Rs/unit)"; ws.cell(11, 5, "Amount (Rs)").font = Font(bold=True, color="FFFFFF"); ws["E11"].fill = HDR; ws.column_dimensions["E"].width = 14
ws["A12"], ws["C12"], ws["D12"] = "Cement", "bag", 400
ws["B12"] = "=ROUND(B3/SUM(B3:B5)*B6*B7/B8,2)"
ws["A13"], ws["C13"], ws["D13"] = "Sand", "m3", 1800
ws["B13"] = "=ROUND(B4/SUM(B3:B5)*B6,3)"
ws["A14"], ws["C14"], ws["D14"] = "Aggregate", "m3", 1500
ws["B14"] = "=ROUND(B5/SUM(B3:B5)*B6,3)"
ws["A15"], ws["B15"], ws["C15"], ws["D15"] = "Mason (skilled)", 0.5, "day", 900
ws["A16"], ws["B16"], ws["C16"], ws["D16"] = "Mazdoor (unskilled)", 2, "day", 600
ws["A17"], ws["B17"], ws["C17"], ws["D17"] = "Water, mixer, misc.", 1, "LS", 250
for r in range(12, 18): ws[f"E{r}"] = f"=ROUND(B{r}*D{r},2)"
inputs(ws, "D12:D17"); inputs(ws, "B15:B17")
ws["A18"], ws["E18"] = "Direct cost", "=SUM(E12:E17)"
ws["A19"], ws["B19"], ws["E19"] = "Overhead %", 10, "=ROUND(E18*B19/100,2)"
ws["A20"], ws["B20"], ws["E20"] = "Contractor profit %", 10, "=ROUND((E18+E19)*B20/100,2)"
ws["A21"], ws["E21"] = "RATE PER m3 (Rs)", "=ROUND(E18+E19+E20,2)"
ws["A21"].font = Font(bold=True); ws["E21"].fill = TOT; ws["E21"].font = Font(bold=True)
inputs(ws, "B19:B20")

# ---------- 4 BOQ ----------
ws = sheet("BOQ", [7, 38, 8, 12, 13, 16])
title(ws, "Bill of Quantities", "Rate for concrete links to Rate Analysis; other rates are EXAMPLES.")
head(ws, 4, ["Sr", "Item", "Unit", "Qty", "Rate (Rs)", "Amount (Rs)"])
boq = [("Earthwork excavation", "m3", 24, 250), ("PCC 1:4:8", "m3", 1.2, 4800), ("RCC M20 (rate from Rate Analysis)", "m3", 18, "='Rate Analysis'!E21"),
       ("Reinforcement steel (qty from BBS, kg)", "kg", "=BBS!H36", 78), ("Brick masonry", "m3", 12, 5500), ("Plastering 12 mm", "m2", 120, 260)]
for r in range(5, 25):
    ws.cell(r, 1, r - 4)
    if r - 5 < len(boq):
        _, *_ = boq[r - 5]
        for c, v in zip([2, 3, 4, 5], boq[r - 5]): ws.cell(r, c, v)
    ws.cell(r, 6, f'=IF(D{r}="","",ROUND(D{r}*E{r},2))')
inputs(ws, "B5:E24")
ws["E26"], ws["F26"] = "Sub-total", "=SUM(F5:F24)"
ws["D27"], ws["E27"], ws["F27"] = 3, "Contingency %", "=ROUND(F26*D27/100,2)"
ws["D28"], ws["E28"], ws["F28"] = 18, "GST %", "=ROUND((F26+F27)*D28/100,2)"
ws["E29"], ws["F29"] = "GRAND TOTAL", "=F26+F27+F28"; ws["F29"].fill = TOT; ws["F29"].font = Font(bold=True)
inputs(ws, "D27:D28")
ws["A31"] = "Material requirement (from concrete + steel quantities above)"; ws["A31"].font = Font(bold=True, color="3B2A6B")
ws["B32"], ws["D32"] = "RCC/PCC concrete volume (m3)", "=D7+D6"
ws["B33"], ws["D33"] = "Wastage % (example)", 5; ws["D33"].fill = INP
ws["B34"], ws["D34"] = "Cement (bags)", "=ROUNDUP(D32*'Rate Analysis'!B12*(1+D33/100),0)"
ws["B35"], ws["D35"] = "Sand (m3)", "=ROUND(D32*'Rate Analysis'!B13*(1+D33/100),2)"
ws["B36"], ws["D36"] = "Aggregate (m3)", "=ROUND(D32*'Rate Analysis'!B14*(1+D33/100),2)"
ws["B37"], ws["D37"] = "Steel (kg)", "=ROUND(BBS!H36*(1+D33/100),0)"
ws["B38"] = "Note: PCC uses the same mix as RCC here for simplicity; use its own ratio for exact PCC."

# ---------- 5 RA BILL ----------
ws = sheet("RA Bill", [6, 32, 8, 11, 12, 12, 12, 15, 15, 15])
title(ws, "Running Account Bill", "This bill = upto date - previous. Amounts = qty x rate.")
head(ws, 4, ["Sr", "Item", "Unit", "Rate", "Qty upto date", "Qty previous", "Qty this bill", "Amt upto date", "Amt previous", "Amt this bill"])
ra = [("Earthwork excavation", "m3", 250, 24, 10), ("RCC M20", "m3", "=BOQ!E7", 9, 0), ("Brick masonry", "m3", 5500, 6, 0)]
for r in range(5, 21):
    ws.cell(r, 1, r - 4)
    if r - 5 < len(ra):
        for c, v in zip([2, 3, 4, 5, 6], ra[r - 5]): ws.cell(r, c, v)
    ws.cell(r, 7, f'=IF(E{r}="","",E{r}-F{r})'); ws.cell(r, 8, f'=IF(E{r}="","",ROUND(E{r}*D{r},2))')
    ws.cell(r, 9, f'=IF(E{r}="","",ROUND(F{r}*D{r},2))'); ws.cell(r, 10, f'=IF(E{r}="","",H{r}-I{r})')
inputs(ws, "B5:F20")
ws["G22"] = "Gross"; 
for c in "HIJ": ws[f"{c}22"] = f"=SUM({c}5:{c}20)"
ws["I23"], ws["J23"] = "Retention %", "=ROUND(-J22*H23/100,2)"; ws["H23"] = 5
ws["I24"], ws["J24"] = "GST % (on this bill)", "=ROUND((J22+J23)*H24/100,2)"; ws["H24"] = 18
ws["I25"], ws["J25"] = "TDS % (on this bill, excl. GST)", "=ROUND(-(J22+J23)*H25/100,2)"; ws["H25"] = 2
ws["I26"], ws["J26"] = "NET PAYABLE (Rs)", "=J22+J23+J24+J25"; ws["J26"].fill = TOT; ws["J26"].font = Font(bold=True)
ws["A28"] = "Check: negative 'Qty this bill' means upto-date qty is less than previous. Rates for TDS/GST/retention are examples; use your contract terms."
inputs(ws, "H23:H25")

# ---------- 6 MATERIAL TRACKER ----------
ws = sheet("Material Tracker", [24, 9, 12, 12, 12, 12, 14])
title(ws, "Material Tracker")
head(ws, 3, ["Material", "Unit", "Required", "Received", "Used", "Balance in stock", "Still to order"])
mt = [("Cement", "bag", "=BOQ!D34", 120, 80), ("Sand", "m3", "=BOQ!D35", 10, 6), ("Aggregate", "m3", "=BOQ!D36", 12, 8), ("Steel", "kg", "=BOQ!D37", 1000, 700)]
for r in range(4, 16):
    if r - 4 < len(mt):
        for c, v in zip([1, 2, 3, 4, 5], mt[r - 4]): ws.cell(r, c, v)
    ws.cell(r, 6, f'=IF(A{r}="","",D{r}-E{r})'); ws.cell(r, 7, f'=IF(A{r}="","",MAX(0,C{r}-D{r}))')
inputs(ws, "A4:E15")

# ---------- 7 PROJECT SUMMARY ----------
ws = sheet("Project Summary", [34, 20])
title(ws, "Project Summary")
rows = [("Project name", "Sample G+0 house"), ("BOQ grand total (Rs)", "=BOQ!F29"), ("Total steel (kg)", "=BBS!H36"), ("Cement required (bags)", "=BOQ!D34"),
        ("Billed upto date, gross (Rs)", "='RA Bill'!H22"), ("Net paid/payable this bill (Rs)", "='RA Bill'!J26"),
        ("Balance work value vs BOQ before GST (Rs)", "=BOQ!F26-'RA Bill'!H22"), ("Progress % (billed / BOQ sub-total)", "=IF(BOQ!F26=0,0,ROUND('RA Bill'!H22/BOQ!F26*100,1))")]
for i, (k, v) in enumerate(rows):
    ws[f"A{3+i}"] = k; ws[f"B{3+i}"] = v
ws["B3"].fill = INP
ws["A12"] = "Disclaimer: example data only. Replace with your project numbers and check against your drawings, IS codes and contract."
for w in wb.worksheets:
    w.sheet_view.showGridLines = True
wb.save(sys.argv[1])
