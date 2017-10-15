from docxlib import *

remove_comment_timestamps('../testdata/test.docx', '../testdata/testout.docx')

comments = get_changes_metadata('../testdata/test.docx')

newtimestamps = [(t[0], t[1], t[2] - datetime.timedelta(days=500)) for t in comments]
set_comment_timestamps('../testdata/test.docx', '../testdata/testout.docx', newtimestamps)
