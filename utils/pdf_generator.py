from fpdf import FPDF
from datetime import datetime

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'LUXESTAY HOTEL - INVOICE', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Thank you for staying with LuxeStay!', 0, 0, 'C')

def create_invoice_pdf(booking_data):
    pdf = InvoicePDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Guest Info
    pdf.cell(200, 10, txt=f"Guest ID: {booking_data['guest_id']}", ln=True)
    pdf.cell(200, 10, txt=f"Room: {booking_data['room_id']}", ln=True)
    pdf.cell(200, 10, txt=f"Stay: {booking_data['stay_dates']}", ln=True)
    pdf.ln(5)

    # Table Header
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(130, 10, "Description", 1, 0, 'C', True)
    pdf.cell(60, 10, "Amount (R)", 1, 1, 'C', True)

    # Room Charge
    pdf.cell(130, 10, "Base Room Charge", 1)
    pdf.cell(60, 10, f"{booking_data['room_charge']:.2f}", 1, 1, 'R')

    # Extra Services
    for service in booking_data.get('extras', []):
        pdf.cell(130, 10, service['service'], 1)
        pdf.cell(60, 10, f"{service['amount']:.2f}", 1, 1, 'R')

    # Total
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(130, 10, "GRAND TOTAL", 1)
    pdf.cell(60, 10, f"{booking_data['grand_total']:.2f}", 1, 1, 'R')

    filename = f"invoice_{booking_data['room_id']}.pdf"
    pdf.output(filename)
    return filename