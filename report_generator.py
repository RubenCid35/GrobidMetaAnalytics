

from os import path, listdir, mkdir

from xml.etree import ElementTree
from grobid_client.grobid_client import GrobidClient

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode

from collections import Counter

def create_pdf() -> FPDF:
    """Crea un objeto para la edición de PDF

    Returns:
        FPDF: Objeto PDF creado
    """
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font('Times', 'B', 16)

    return pdf    

def crear_histograma(figures):
    fig, ax = plt.subplots()
    
    # Obtener los títulos y números de figuras
    titulos = [item[0] for item in figures]
    num_figuras = [item[1] for item in figures]
    
    # Limitar el tamaño de los títulos si son muy largos
    titulos = [titulo[:30] + '...' if len(titulo) > 30 else titulo for titulo in titulos]
    
    # Graficar el histograma horizontal
    ax.barh(titulos, num_figuras, color='skyblue')
    ax.set_xlabel('Número de Figuras')
    ax.set_ylabel('Título de la Publicación')
    ax.set_title('Número de Figuras por Publicación')

    return fig

def create_enumeration(table, row, title, found_links):
    if len(found_links) == 0: 
        row.cell("")
        return 
    
    chunks = 30
    bullet = "\u00b7"
    for i in range(0, len(found_links), chunks):
        if i != 0:
            row = table.row()
            row.cell(title)

        cell_links = found_links[i:i+chunks]
        row_text = ""
        for link in cell_links:
            row_text += bullet + " " + link + "\n"
        style = FontFace(color=0, size_pt=12, fill_color=255)
        row.cell(row_text, style = style)

def main():
    # Extract Information from the publications
    grobid_client = GrobidClient(config_path="./config/python/config.json")
    grobid_client.process("processFulltextDocument", "./papers", output = "./tmp/", n=10, 
                           consolidate_citations = False, include_raw_citations = False,  )

    abstracts = ""
    figures   = []
    links     = []
    
    ns = "{http://www.tei-c.org/ns/1.0}"
    text = lambda obj: obj.text
    for file_path in listdir("tmp"):

        # Parse the results
        if not file_path.endswith('.xml'): continue
        file_path = path.join("./tmp", file_path)
        tree = ElementTree.parse(file_path)
        root = tree.getroot()

        # Get title
        tag = ".//" + ns + "teiHeader/" + ns + "fileDesc/" + ns + "titleStmt/" + ns + "title"
        title = next(map(text, root.findall(tag)))
        # Extract Abstract
        tag = ".//" + ns + "abstract/" + ns + "div/" + ns + "p"
        abstract = "".join(map(text, root.findall(tag)))
        abstracts += abstract

        # Count figures
        tag = ".//" + ns + "figure"
        figs = root.findall(tag)
        figures.append((title, len(figs)))

        # list of links
        # arxiv links

        found_links = []
        tag = ".//" + ns + 'idno[@type]'
        for link in root.findall(tag):
            link_type = link.attrib.get("type")
            if link_type == "MD5" or link_type == 'grant-number': continue
            
            if link_type == "DOI":
                link = "https://doi.org/" + link.text
            elif link_type == 'arXiv':
                link = link.text.split("[")[0]
                link = link.replace("arXiv:", "https://arxiv.org/abs/")
            elif link_type == 'ISSN':
                link = "https://portal.issn.org/resource/ISSN/" + link.text
            else:
                link = link.text

            found_links.append(link)

        tag = ".//" + ns + "biblStruct/" + ns + "monogr/" + ns + "ptr"
        found_links +=  list(map(lambda ob: ob.attrib.get("target"), root.findall(tag)))
        links.append((title, found_links))

    mkdir("results")

    # Generate Report
    pdf = create_pdf()
    pdf.set_auto_page_break(auto=True, margin=25.4)
    pdf.set_margins(top = 25.4, left = 25.4, right = 25.4)

    title = "Reporte de Estadísticas de Publicaciones"
    pdf.set_font("Times", size=30)
    title_width = pdf.get_string_width(title)
    pdf.set_xy((pdf.w - title_width) / 2, 100)
    pdf.cell(0, 0, title, new_x="LMARGIN", new_y="NEXT")

    pdf.add_page()
    pdf.set_font("Times", size=12)
    # Add section title
    pdf.set_font("Times", "B", size=20)
    pdf.cell(20, 1, text="1. Palabras del abstracto", align="L")
    pdf.ln(10)  # Add some space after the title
    pdf.set_font("Times", "", size=12)

    # WordCloud Figure
    image = WordCloud(stopwords=STOPWORDS, max_font_size=50, max_words=150, background_color="white").generate(abstracts)
    fig = plt.figure()
    ax  = fig.gca()
    ax.imshow(image)
    plt.axis('off')
    fig.tight_layout()
    fig.savefig("./results/abstract-wordcloud.png", bbox_inches='tight')

    # Adding Image to report
    image_width = pdf.w - 2 * pdf.l_margin
    pdf.image("./results/abstract-wordcloud.png", w=image_width, keep_aspect_ratio=True)

    pdf.add_page()
    pdf.set_font("Times", "B", size=20)
    pdf.cell(20, 1, text="2. Distribución del Número de Figuras", align="L")
    pdf.ln(10)  # Add some space after the title

    # Create Visualization
    fig = crear_histograma(figures)
    fig.tight_layout()
    fig.savefig("./results/num-figures.png", bbox_inches='tight')
    image_width = pdf.w - 2 * pdf.l_margin
    pdf.image("./results/num-figures.png", w=image_width, keep_aspect_ratio=True)

    # Calcular el número más común de figuras y el promedio de figuras
    num_figuras = [num for _, num in figures]

    # Calcular el número más común de figuras y el promedio de figuras
    mas_comun = max(set(num_figuras), key=num_figuras.count)
    promedio = sum(num_figuras) / len(num_figuras)
    mas_figuras = max(num_figuras)

    # Agregar párrafo describiendo el histograma
    pdf.set_font("Times", "", size=12)
    descripcion = f"Usando este histograma como referencia, se puede concluir que la mayoría de las publicaciones contienen {mas_comun} figuras. Además, el número de figuras de las publicaciones tiene un promedio de {promedio:.2f}. Y la mayor cantidad de figuras que apareció en una publicación fueron {mas_figuras}."
    pdf.multi_cell(0, 5, descripcion)
    
     # - Draw a keyword cloud based on the abstract information
    # - Create a visualization showing the number of figures per article.
    # - Create a list of the links found in each paper.
    pdf.ln(20)
    pdf.set_font("Times", "B", size=20)
    pdf.cell(20, 1, text="3. Links de Cada Publicación", align="L")
    pdf.set_font("Times", "", size=12)
    pdf.ln(10)  # Add some space after the title
    pdf.multi_cell(0, 5, "A continuación, se muesta en una tabla los links detectados en cada una de las publicaciones. Los link pertenecen principalmente a la referencias y citaciones de las publicaciones. ")

    pdf.add_page()

    with pdf.table(
        col_widths=(int(pdf.w * .4), int(pdf.w * .5)),
        headings_style=FontFace(emphasis="BOLD", color=0, fill_color=255),

        line_height=6,
        text_align=("LEFT", "LEFT"),
        width=158,

    ) as table:
        links = [("Publicación", "Links Encontrados")] + links
        for (title, found_links) in links:
            row = table.row()
            row.cell(title)

            if isinstance(found_links, str):
                row.cell(found_links)
                continue 
            else:
                create_enumeration(table, row, title, found_links)
                #for link in found_links:
                #    row.cell(link)
                #    continue


    pdf.output("./results/report.pdf")
        
        



if '__main__' == __name__: main()