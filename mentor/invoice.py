from __future__ import unicode_literals

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO


class TableWithHeader(Table):
    def __init__(self, data, horizontal_align=None, style=None, **kwargs):
        Table.__init__(self, data, hAlign=horizontal_align, **kwargs)

        default_style = [
            ('INNERGRID', (0, 0), (-1, -1), .25, colors.black),
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]
        if (len(data) <= 24 or 'rowHeights' in kwargs) and data[0][0] == '#':
            default_style.append(
                ('BACKGROUND', (0, 0), (-1, -len(data)), colors.lightgrey))

        if style and isinstance(style, list):
            default_style.extend(style)

        self.setStyle(TableStyle(default_style))


class PDFInfo(object):
    def __init__(self, title=None, author=None, subject=None):
        self.title = title
        self.author = author
        self.subject = subject


class SimpleInvoice(SimpleDocTemplate):
    """Generates the Invoice"""
    default_pdf_info = PDFInfo(title='Invoice', author='tonymontaro', subject='Invoice')

    def __init__(self, invoice_path, pdf_info=None):
        if not pdf_info:
            pdf_info = self.default_pdf_info

        SimpleDocTemplate.__init__(
            self,
            invoice_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch,
            **pdf_info.__dict__
        )

        self._story = []
        self.invoice_info = None
        self.mentor_info = {
            'name': '',
            'address': '',
            'address_more': '',
            'city': '',
        }
        self.code_institute_info = {
            'address': '1st Floor, Block 8,',
            'address_more': 'Blackrock Business Park, Carysfort Ave,',
            'city': 'Blackrock, Co Dublin',
        }
        self.totals = {
            'hours': '',
            'hourly_fee': '',
            'total_amount': '',
        }
        self.date_and_number = {
            'date': '',
            'invoice_number': ''
        }
        self.session_data = []

        self._defined_styles = getSampleStyleSheet()
        self._defined_styles.add(
            ParagraphStyle('RightHeading1',
                           parent=self._defined_styles.get('Heading1'),
                           alignment=TA_RIGHT)
        )
        self._defined_styles.add(
            ParagraphStyle('TableParagraph',
                           parent=self._defined_styles.get('Normal'),
                           alignment=TA_CENTER)
        )
        self._defined_styles.add(
            ParagraphStyle('RightParagraph',
                           parent=self._defined_styles.get('Normal'),
                           alignment=TA_RIGHT)
        )

    def _build_mentor_details(self):
        info = self.mentor_info
        dnum = self.date_and_number
        table_data = [
            [
                Paragraph(info['name'], self._defined_styles.get('Heading1')),
                '',
                '',
                Paragraph('INVOICE', self._defined_styles.get('RightHeading1')),
                ''
            ],
            [
                Paragraph(
                    '{}<br />{}<br />{}'.format(
                        info['address'], info['address_more'], info['city']),
                    self._defined_styles.get('Normal')), '', '',
                Paragraph(
                    '<b>DATE:</b> {} <br /><br /> <b>INVOICE NO:</b> {}'.format(
                        dnum['date'], dnum['number']),
                    self._defined_styles.get('RightParagraph')), ''
            ],
            ['', '', '', '', '']
        ]
        table_style = [
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (3, 0), (4, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (3, 1), (4, 1)),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ]

        self._story.append(
            Table(table_data, style=table_style)
        )

    def _build_code_institute_details(self):
        table_data = [
            [
                Paragraph('<b>BILL TO</b>', self._defined_styles.get('Normal')),
                '', '', '', ''
            ]
        ]
        table_style = [
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (3, 0), (4, 0)),
            ('LINEBELOW', (0, 0), (1, 0), 1, colors.gray),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ]
        self._story.append(Table(table_data, style=table_style))
        self._story.append(Paragraph('Code Institute Limited',
                                     self._defined_styles.get('Heading1')))
        info = self.code_institute_info
        self._story.append(Paragraph(
            '{} <br />{} <br />{} <br /><br /><br />'.format(
                info['address'], info['address_more'], info['city']),
            self._defined_styles.get('Normal')))

    def _build_table_data(self):
        item_data = []
        style = []
        item_data.append(
            ('#',
             Paragraph('STUDENT', self._defined_styles.get('TableParagraph')),
             '3', '4', 'TIME SPENT (hh:mm:ss)')
        )
        item_data.extend(self.session_data)

        for y_index in range(0, len(item_data)):
            style.append(('SPAN', (1, y_index), (3, y_index)))
        self._story.append(
            TableWithHeader(item_data, horizontal_align='LEFT', style=style))

    def _build_totals(self):
        table_data = [
            ['', '', '', '', ''],
            [
                '', '',
                Paragraph('Total Time (Hours)',
                          self._defined_styles.get('TableParagraph')), '',
                '  {}'.format(self.totals['hours']),
            ],
            [
                '', '',
                Paragraph('Hourly Fee',
                          self._defined_styles.get('TableParagraph')), '',
                '€ {}'.format(self.totals['hourly_fee']),
            ],
            [
                '', '',
                Paragraph('<b>Total Amount Owed</b>',
                          self._defined_styles.get('TableParagraph')), '',
                Paragraph('<b>€ {}</b>'.format(self.totals['total_amount']),
                          self._defined_styles.get('Normal'))
            ]
        ]
        table_style = [
            ('SPAN', (2, 1), (3, 1)),
            ('SPAN', (2, 2), (3, 2)),
            ('SPAN', (2, 3), (3, 3)),
            ('LINEBELOW', (2, 2), (4, 2), 1, colors.gray)
        ]

        self._story.append(
            Table(table_data, style=table_style)
        )

    def finish(self):
        self._build_mentor_details()
        self._build_code_institute_details()
        self._build_table_data()
        self._build_totals()

        self.build(self._story)


def generate_invoice(mentor_info, date_and_number, totals, session_data):
    buffer = BytesIO()
    doc = SimpleInvoice(buffer)

    doc.date_and_number = date_and_number
    doc.mentor_info = mentor_info
    doc.totals = totals
    doc.session_data = session_data
    
    doc.finish()
    return buffer.getvalue()
