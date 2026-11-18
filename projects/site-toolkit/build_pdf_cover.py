"""Builds guide PDF (7 pages, Hinglish) and cover PNG. Usage: build_pdf_cover.py OUT_DIR"""
import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]
ss = getSampleStyleSheet()
H = ParagraphStyle("H", parent=ss["Heading1"], textColor=colors.HexColor("#3B2A6B"), fontSize=18)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10.5, leading=15)
def tbl(rows, w=None):
    t = Table(rows, colWidths=w)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3B2A6B")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), .4, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 9)]))
    return t
P = lambda t: Paragraph(t, B)
pages = [
 [Paragraph("Site Estimation Toolkit: Guide", H), P("Ye guide Excel toolkit ke har sheet ko worked example ke saath samjhati hai. Peele cells aapke input hain, baaki formula. Sab rate, wastage aur % <b>sirf example</b> hain: apne shehar ke rate, DSR aur IS code se check karke badlein."),
  Spacer(1, 8), tbl([["Sheet", "Kaam"], ["Measurement", "Nos x L x B x D se quantity"], ["BBS", "Steel weight, dia-wise summary, stirrup length"], ["Rate Analysis", "Concrete ka per m3 rate"],
  ["BOQ", "Qty x rate, contingency, GST, material requirement"], ["RA Bill", "Upto date / previous / this bill, net payable"], ["Material Tracker", "Required, received, used, balance"], ["Project Summary", "Sab ka total ek jagah"]], [120, 330])],
 [Paragraph("1. Measurement sheet", H), P("Formula: Qty = Nos x L x B x D. Jo dimension nahi hai (jaise plaster mein thickness) use khaali chhodein, wo 1 maana jayega."),
  P("<b>Example:</b> 4 footing, 1.5 m x 1.5 m x 1.2 m deep. Qty = 4 x 1.5 x 1.5 x 1.2 = <b>10.8 m3</b>. Darwaza ka khula hissa minus karna ho to 'Deduct' chunein: 2 x 1.0 x 0.23 x 2.1 = 0.966, sheet mein -0.966 dikhega."),
  P("Tip: har item ka unit (m3, m2, m) sahi likhein. Total sirf ek hi unit ke items ka jodein.")],
 [Paragraph("2. BBS: steel weight", H), P("Steel ka weight per metre = d x d / 162 (d mm mein). <b>Example:</b> 16 mm bar: 16 x 16 / 162 = 1.58 kg/m. 8 bars, 4.8 m lambi: total length 38.4 m, weight = 38.4 x 1.58 = <b>60.7 kg</b>."),
  P("Sheet mein Mark, Member, Dia, Nos, Cut length daalein. Weight apne aap banta hai. Dia-wise summary (6 se 32 mm) neeche side mein hai aur ek 'Check' cell hai jo 0 aana chahiye. Total steel BOQ mein apne aap jaata hai.")],
 [Paragraph("3. Stirrup cutting length", H), P("Cutting length = 2 x (a + b) + hook allowance - bend deduction, jahan a, b andar ki size hai (member size - 2 x cover)."),
  P("<b>Example:</b> beam 230 x 450 mm, cover 25 mm, stirrup 8 mm. a = 180, b = 400. Perimeter = 2 x 580 = 1160 mm. Hook: 2 x 10d = 160 mm. Bend deduction: 3 bends x 1d + 2 bends x 1.5d = 48 mm. Cutting length = 1160 + 160 - 48 = <b>1272 mm = 1.272 m</b>."),
  P("<b>Dhyan:</b> hook (10d) aur bend deduction ki values toolkit mein example hain, editable. Apne engineer / IS 2502 / SP 34 se confirm karke badlein.")],
 [Paragraph("4. Rate Analysis (concrete)", H), P("Mix ratio 1 : 1.5 : 3 aur dry volume factor 1.54 ke saath, 1 m3 concrete ke liye: cement = 1/5.5 x 1.54 = 0.28 m3 x 1440 kg/m3 = 403 kg = <b>8.06 bag</b> (50 kg). Sand = 1.5/5.5 x 1.54 = <b>0.42 m3</b>. Gitti = 3/5.5 x 1.54 = <b>0.84 m3</b>."),
  P("Phir apne shehar ka rate daalein (cement bag, sand, gitti, mason, mazdoor). Direct cost + overhead % + profit % = <b>rate per m3</b>. Toolkit ke example rates se ~Rs 8,639/m3 aata hai: ye sirf example hai, apna rate daalein.")],
 [Paragraph("5. BOQ aur Material requirement", H), P("Har item: Qty x Rate = Amount. Neeche sub-total, contingency %, GST % aur <b>Grand total</b>. RCC ka rate Rate Analysis se apne aap aata hai aur steel ki qty BBS se."),
  P("Material requirement: concrete volume x per m3 material x (1 + wastage %). <b>Example:</b> 19.2 m3 concrete, 5% wastage: cement = 19.2 x 8.06 x 1.05 = <b>163 bag</b>."),
  P("Note: PCC aur RCC ka mix alag ho to PCC ko alag Rate Analysis se calculate karein.")],
 [Paragraph("6. RA Bill, Material Tracker, Summary", H), P("RA Bill mein 'Qty upto date' aur 'Qty previous' daalein; 'this bill' = upto date - previous. Amount = qty x rate."),
  P("Gross this bill se retention % minus, phir GST % jod, TDS % minus (toolkit mein TDS GST ke bina value par). <b>Net payable</b> last mein. Rates (retention, GST, TDS) apne contract ke hisaab se badlein."),
  P("Material Tracker: Required (BOQ se), Received, Used daalein. Balance = Received - Used, 'Still to order' = Required - Received. Project Summary mein BOQ total, billed value aur progress % milta hai."),
  Spacer(1, 10), P("<b>Disclaimer:</b> Ye toolkit calculation ka madadgaar hai. Final estimate aur bill ki zimmedari aapki hai: apni drawing, IS codes, DSR aur contract se check karein.")],
]
doc = SimpleDocTemplate(os.path.join(out, "Site-Estimation-Toolkit-Guide.pdf"), pagesize=A4, title="Site Estimation Toolkit Guide")
fl = []
for i, p in enumerate(pages):
    fl += p + ([PageBreak()] if i < len(pages) - 1 else [])
doc.build(fl)
# cover 1280x720
im = Image.new("RGB", (1280, 720), "#3B2A6B"); d = ImageDraw.Draw(im)
f = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
d.rectangle([60, 60, 1220, 660], outline="#FFCA3A", width=6)
d.text((110, 120), "SITE ESTIMATION", font=f(86), fill="white"); d.text((110, 225), "TOOLKIT", font=f(86), fill="#FFCA3A")
d.text((110, 360), "BOQ  |  BBS  |  Rate Analysis  |  RA Bill", font=f(40), fill="white")
d.text((110, 440), "Excel + Hinglish PDF guide", font=f(36), fill="#8AC926")
d.text((110, 560), "Site engineers, contractors, civil students", font=f(30), fill="#dddddd")
im.save(os.path.join(out, "cover.png"))
