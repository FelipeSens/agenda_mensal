from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime, timedelta
from database import obter_responsabilidades_do_mes, obter_estatisticas
import io
import os

# Esse módulo gera um PDF com as responsabilidades do mês.
# A função principal retorna bytes de PDF, que o Flask usa para enviar
# o arquivo ao navegador.
# A função secundária `salvar_relatorio_pdf` grava o arquivo em disco.

def gerar_relatorio_pdf(ano=None, mes=None):
    """
    Gera um relatório em PDF das responsabilidades
    Se ano/mês não forem fornecidos, usa o mês atual
    """
    if ano is None:
        ano = datetime.now().year
    if mes is None:
        mes = datetime.now().month
    
    # Obter dados do banco de dados a partir das funções do módulo database.
    responsabilidades = obter_responsabilidades_do_mes(ano, mes)
    estatisticas = obter_estatisticas()
    
    # Criar buffer em memória para o PDF. O ReportLab escreve os bytes aqui.
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Estilos
    styles = getSampleStyleSheet()
    style_titulo = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00bcd4'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    style_subtitulo = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#00bcd4'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Conteúdo do PDF
    elements = []
    
    # Título
    elements.append(Paragraph("Relatório Mensal de Responsabilidades", style_titulo))
    elements.append(Paragraph(f"Mês: {mes:02d}/{ano}", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Estatísticas
    elements.append(Paragraph("Estatísticas Gerais", style_subtitulo))
    stats_data = [
        ['Métrica', 'Quantidade'],
        ['Total de Responsabilidades', str(estatisticas['total'])],
        ['Pendentes', str(estatisticas['pendentes'])],
        ['Em Progresso', str(estatisticas['em_progresso'])],
        ['Concluídas', str(estatisticas['concluidos'])],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00bcd4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Responsabilidades do mês
    if responsabilidades:
        elements.append(Paragraph("Responsabilidades do Mês", style_subtitulo))
        
        resp_data = [
            ['Data', 'Descrição', 'Situação']
        ]
        
        for resp in responsabilidades:
            data_obj = datetime.strptime(resp['data_execucao'], '%Y-%m-%d')
            data_formatada = data_obj.strftime('%d/%m/%Y')
            
            situacao_display = {
                'pendente': 'Pendente',
                'em_progresso': 'Em Progresso',
                'concluido': 'Concluído'
            }.get(resp['situacao'], resp['situacao'])
            
            resp_data.append([
                data_formatada,
                resp['descricao'][:40],  # Limitar tamanho
                situacao_display
            ])
        
        resp_table = Table(resp_data, colWidths=[1.2*inch, 3*inch, 1.3*inch])
        resp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00bcd4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WRAP', (1, 0), (1, -1), True),
        ]))
        
        elements.append(resp_table)
    else:
        elements.append(Paragraph("Nenhuma responsabilidade registrada para este mês.", styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Rodapé com data e hora de geração
    elements.append(Paragraph(
        f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10, textColor=colors.grey, alignment=1)
    ))
    
    # Gera o PDF de fato e posiciona o buffer no início para leitura.
    doc.build(elements)
    buffer.seek(0)
    
    return buffer.getvalue()

def salvar_relatorio_pdf(ano=None, mes=None):
    """Salva o relatório em PDF no disco"""
    if ano is None:
        ano = datetime.now().year
    if mes is None:
        mes = datetime.now().month
    
    pdf_content = gerar_relatorio_pdf(ano, mes)
    
    # Criar pasta de relatórios se não existir
    if not os.path.exists('relatorios'):
        os.makedirs('relatorios')
    
    # Salvar arquivo
    filename = f'relatorios/relatorio_{ano}_{mes:02d}.pdf'
    with open(filename, 'wb') as f:
        f.write(pdf_content)
    
    return filename

if __name__ == '__main__':
    import os
    pdf = gerar_relatorio_pdf()
    with open('relatorio_teste.pdf', 'wb') as f:
        f.write(pdf)
    print("Relatório gerado com sucesso!")
