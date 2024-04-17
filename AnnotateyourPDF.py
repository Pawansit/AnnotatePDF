#!/usr/bin/env python3

############################################################
####	Author : Pawan Kumar
#### 	Email  : pawan.kumar@ibdc.rcb.res.in
####	Annotating the pdf file using the input text. 
####	This program will seach the input text in each pdf page and if found 
####	will be annotated with golden background color and red dotted lines.
####	
####	Uses: python AnnotateyourPDF.py --input_pdf <pdf file name> --Text_list <"text1", "text2", "text3", "text4">
#### 	Program will output the pdf file with __annot.pdf extention. 



from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import fitz




def list_of_strings(arg):
    return arg.split(',')


def NLPpipeline(pdffile, text_list):
	
	file_data = fitz.open(pdffile)
	red = (1, 0, 0)
	gold = (1, 1, 0)
	
	for page in file_data:
		page_text=page.get_text()
		print("Annotating the Page number", page)
		for text in text_list:
			text_instances = page.search_for(text)
			current_page = page
			if text_instances is not None:
				for inst in text_instances:
					x0,x1,x2,x3 = inst
					rect = (x0,x1,x2,x3)
					annot = current_page.add_rect_annot(rect)
					annot.set_colors(stroke=red, fill=gold)
					annot.set_border(width=1, dashes=[1, 2])
					annot.update(opacity=0.3)
		file_data.save(pdffile.replace(".pdf", "_annot.pdf"))


if __name__ == '__main__':
    parser = ArgumentParser(description="", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input_pdf",   type=str, default="No", help="")
    parser.add_argument("--Text_list", type=list_of_strings, default="No", help="")

    commandline_args = vars(parser.parse_args())
    NLPpipeline(commandline_args['input_pdf'], commandline_args['Text_list'] )