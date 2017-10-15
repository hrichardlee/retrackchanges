import zipfile
import lxml.etree as etree
import datetime
import io
import itertools

namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
author_attrib = namespace + 'author'
date_attrib = namespace + 'date'
date_format = '%Y-%m-%dT%H:%M:%SZ'
doc_filename = 'word/document.xml'
comments_filename = 'word/comments.xml'


_CHANGE_TYPE_TO_FILENAME = {
    'change': doc_filename,
    'comment': comments_filename
}


def remove_comment_timestamps(inf, outf):
    modify(inf, outf,
           lambda info: info.filename == doc_filename or info.filename == comments_filename,
           lambda info, xmltree: _remove_comment_timestamps(xmltree))


def set_comment_timestamps(inf, outf, timestamps):
    """
    timestamps should be an iterable [(change type, author, date), ...]
    """
    timestamps_per_file = {
        filename: [t[2] for t in group] for (filename, group) in
        itertools.groupby(timestamps, lambda t: _CHANGE_TYPE_TO_FILENAME[t[0]])
    }
    modify(inf, outf,
           lambda info: info.filename in timestamps_per_file,
           lambda info, xmltree: _set_comment_timestamps(xmltree, timestamps_per_file[info.filename]))


def modify(inf, outf, predicate, transform):
    """
    inf is a file-like object or filename representing a docx,
    outf is a file-like object or filename that will be written to
    predicate is ZipInfo -> bool that returns true if a file should be transformed
    and transform is (ZipInfo, etree) -> () that transforms the etree in place
    """
    with zipfile.ZipFile(inf, mode='r') as inzipfile, \
            zipfile.ZipFile(outf, mode='w') as outzipfile:
        for info in inzipfile.infolist():
            with inzipfile.open(info.filename) as f:
                if predicate(info):
                    xmltree = etree.parse(f)
                    transform(info, xmltree)
                    with io.BytesIO() as buffer:
                        xmltree.write(buffer, encoding='UTF-8', xml_declaration=True)
                        result = buffer.getvalue()
                else:
                    result = f.read()
                    
                outzipfile.writestr(info, result)


def get_changes_metadata(docx):
    """
    Expects a file-like object or filename representing a docx.
    Returns an iterable [(change type, author, date), ...]
    These represent changes in the overall docx file. change type can be 'change' or 'comment'
    """
    with zipfile.ZipFile(docx, mode='r') as docxzipfile:
        with docxzipfile.open(doc_filename) as docfile, \
                docxzipfile.open(comments_filename) as commentfile:
            return sorted(
                itertools.chain(
                    (('change', author, date) for (author, date) in _get_changes_metadata(etree.parse(docfile))),
                    (('comment', author, date) for (author, date) in _get_changes_metadata(etree.parse(commentfile)))),
                key=lambda m: m[2])  # sort by date


def _get_changes_metadata(document):
    """
    Expects a xml.etree.ElementTree and returns an iterator of
    (author, date as naive datetime) tuples
    """
    return ((el.get(author_attrib),
             datetime.datetime.strptime(el.get(date_attrib), date_format))
            for el in _get_comments(document))


def _set_comment_timestamps(document, new_timestamps):
    """
    Expects a xml.etree.ElementTree and an iterable of naive datetimes.
    Modifies document in place to use the new timestamps. The number of
    timestamps in the document and the length of new_timestamps must be the same
    """
    for (el, ts) in zip(_get_comments(document), new_timestamps):
        el.set(date_attrib, ts.strftime(date_format))


def _remove_comment_timestamps(document, authors=None):
    for el in _get_comments(document):
        del el.attrib[date_attrib]


def _get_comments(document):
    return (el for el in document.iter()
            if date_attrib in el.attrib and author_attrib in el.attrib)
