from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

source = Path(r'c:/Users/xps/Desktop/SHAMSE/docs/project_documentation.md')
out = Path(r'c:/Users/xps/Desktop/SHAMSE/docs/GlowBook_Uganda_Project_Documentation.pdf')
text = source.read_text(encoding='utf-8')

styles = getSampleStyleSheet()
doc = SimpleDocTemplate(str(out), pagesize=letter)
story = []

for line in text.splitlines():
    if not line.strip():
        continue
    if line.startswith('# '):
        story.append(Paragraph(line[2:], styles['Title']))
        story.append(Spacer(1, 10))
    elif line.startswith('## '):
        story.append(Paragraph(line[3:], styles['Heading2']))
        story.append(Spacer(1, 8))
    elif line.startswith('### '):
        story.append(Paragraph(line[4:], styles['Heading3']))
        story.append(Spacer(1, 6))
    else:
        story.append(Paragraph(line, styles['BodyText']))
        story.append(Spacer(1, 4))

doc.build(story)
print(f'PDF generated at: {out}')
