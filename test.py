from __future__ import print_function

from mailmerge import MailMerge

template = "project/static/docx/book_template.docx"

document = MailMerge(template)
print(document.get_merge_fields())

document.merge(
    Name="Justna & Karol",
    Date="15.03.2023",
    City="Katowice",
    Guest="Ciocia Asia",
    Picture_path="https://www.exceldemy.com/wp-content/uploads/2022/06/How-to-Mail-Merge-Pictures-from-Excel-to-Word-22.png")

document.write('test-output.docx')
