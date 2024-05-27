#!/usr/bin/env python3

############################################################
####    Author : Pawan Kumar
####    Email  : pawan.kumar@ibdc.rcb.res.in
####    Annotating the pdf file using the input text. 
####    This program will seach the input text in each pdf page and if found 
####    will be annotated with golden background color and red dotted lines.
####    
####    Uses: python GeneralPdf_Annotation.py --input_pdf <pdf file name> --Text_list <"text1", "text2", "text3", "text4">
####    program will output the pdf file with __annot.pdf extention. 




from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import fitz
from matplotlib import colors
from pathlib import Path


def RGBcolor(text_list):
    #ColorList = random.sample(list(fitz.pdfcolor.keys()), len(list(fitz.pdfcolor.keys())))
    ColorList = ['lime','blue','magenta','maroon','olive','green','teal','navy','coral','salmon','orange','gold','dark green','royal blue','yellow','saddle brown','peru','slate gray']
    color_rgb = []
    for Co in ColorList:
        try :
            if Co == "white":continue
            color_rgb.append(colors.hex2color(colors.cnames[Co]))
        except KeyError:
            continue
    return(color_rgb[:len(text_list)])

def PDFAnnotation(pdffile, text_list, RGBcolors):
    
    SumDict = {}
    file_data = fitz.open(pdffile)
    red = (1, 0, 0)
    for text, color in zip(text_list, RGBcolors):
        textwithSpace =  " "+str(text)+" "
        Textsum = []
        for page in file_data:
            text_instances = page.search_for(textwithSpace)
            Textsum.append(len(text_instances))
            current_page = page
            if text_instances is None: continue
            for inst in text_instances:
                x0,x1,x2,x3 = inst
                rect = (x0,x1,x2,x3)
                annot = current_page.add_rect_annot(rect)
                annot.set_colors(stroke=red, fill=color)
                annot.set_border(width = 1, dashes = [1,2])
                annot.update(opacity=0.4)
            SumDict[text] = (Textsum)
            file_data.save(pdffile.replace(".pdf", "_annot.pdf"))
    return(SumDict)


   
def SearchCountSummary(S, RGBcolors):
    Text = list(S.keys())
    Count = [m for m in list(S.values())]
    
    doc = fitz.open()
    page = doc.new_page()
    rect = fitz.Rect(50, 50, 500, 600)
    Field_Column = len(Count)
    Value_Rows = len(Count[0])
    CELLS = fitz.make_table(rect, cols=Field_Column+1, rows=Value_Rows+1)
    Black = fitz.pdfcolor['black']
    shape = page.new_shape() 
    ReshapeArray = []
    for i in range(Value_Rows):
        ReshapeArray1 = []
        for j in range(len(Count)):
            ReshapeArray1.append(str(Count[j][i]))
        ReshapeArray.append(ReshapeArray1)

    Text.insert(0,"PageNumber")
    RGBcolors.insert(0,colors.hex2color(colors.cnames['black']))

    for j in range(len(Text)):           #### Insert the Search Field Name in first row
        shape.draw_rect(CELLS[0][j])
        shape.insert_textbox(CELLS[0][j], str(Text[j]), color=RGBcolors[j], fontname="hebo", align=1 )

    for i in range(1, len(CELLS)):      #### Insert the Field value by Page number
        shape.draw_rect(CELLS[i][0])
        shape.insert_textbox(CELLS[i][0], str(i+1),  fontname="hebo", align=1)
        for z in range(0, Field_Column):
            shape.draw_rect(CELLS[i][z+1])
            shape.insert_textbox(CELLS[i][z+1], ReshapeArray[i-1][z],  fontname="hebo", align=1 )            

    shape.finish(width=0.3, color=Black)
    shape.commit()
    doc.save("text.pdf")


def list_of_strings(arg):
    return arg.split(',')

if __name__ == '__main__':
    parser = ArgumentParser(description="", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input_pdf",   type=str, help="")
    parser.add_argument("--Text_list", type=list_of_strings, default="No", help="")

    commandline_args = vars(parser.parse_args())
    TextColor = RGBcolor(commandline_args['Text_list'])
    TextStats = PDFAnnotation(pdffile=commandline_args['input_pdf'],text_list=commandline_args['Text_list'],RGBcolors=TextColor )
    SearchCountSummary(S=TextStats,RGBcolors=TextColor)
    result = fitz.open()
    
for pdf in [str(Path.cwd())+"/"+"text.pdf", str(Path.cwd())+"/"+commandline_args['input_pdf'].split(".")[0]+"_annot.pdf"]:
    with fitz.open(pdf) as mfile:
        result.insert_pdf(mfile)
result.save(str(Path.cwd())+"/"+"AnnotatePDF.pdf")

Path("text.pdf").unlink()
Path(commandline_args['input_pdf'].split(".")[0]+"_annot.pdf").unlink()
