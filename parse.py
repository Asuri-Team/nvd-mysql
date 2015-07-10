__author__ = 'Usual'

import logging
import MySQLdb

from config import xml

from database import conn
from database import cur

from database import INSERT_NVD
from database import INSERT_PRODUCT
from database import INSERT_REFERENCE
from database import INSERT_LOGICAL_TEST

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

# XML namespace defined in xml header
namespace = {
    'vuln': 'http://scap.nist.gov/schema/vulnerability/0.4',
    'cvss': 'http://scap.nist.gov/schema/cvss-v2/0.2',
    'cpe-lang': 'http://cpe.mitre.org/language/2.0',
    'xmlns': 'http://scap.nist.gov/schema/feed/vulnerability/2.0'
}

def getText(dom, tag, default=None):
    """
    Get text of specific node.
    :param dom: parent node for search
    :param tag: XPath tag for search
    :param default: default value to return
    :return: text or default
    """
    child = dom.find(tag, namespace)
    return  MySQLdb.escape_string(child.text) if child is not None else default

def getAttrib(dom, tag, attr, default=None):
    """
    Get attribute of specific node.
    :param dom: parent node for search
    :param tag: XPath tag for search
    :param attr: attribute name
    :param default: default value to return
    :return: attribute or default
    """
    child = dom.find(tag, namespace)
    return MySQLdb.escape_string(child.attrib[attr]) if child is not None else default

def genDatas(root):
    for entry in root.findall('xmlns:entry', namespace):
        # NVD basic information
        nvdResult = {}
        nvdResult['cve_id'] = getText(entry, 'vuln:cve-id')
        nvdResult['published_datetime'] = getText(entry, 'vuln:published-datetime')
        nvdResult['last_modified_datetime'] = getText(entry, 'vuln:last-modified-datetime')

        nvdResult['score'] = getText(entry, './/cvss:score', 0)
        nvdResult['access_vector'] = getText(entry, './/cvss:access-vector')
        nvdResult['access_complexity'] = getText(entry, './/cvss:access-complexity')
        nvdResult['authentication'] = getText(entry, './/cvss:authentication')
        nvdResult['confidentiality_impact'] = getText(entry, './/cvss:confidentiality-impact')
        nvdResult['integrity_impact'] = getText(entry, './/cvss:integrity-impact')
        nvdResult['availability_impact'] = getText(entry, './/cvss:availability-impact')
        nvdResult['source'] = getText(entry, './/cvss:source')
        nvdResult['generated_on_datetime'] = getText(entry, './/cvss:generated-on-datetime')

        nvdResult['cwe_id'] = getAttrib(entry, 'vuln:cwe', 'id')
        nvdResult['summary'] = getText(entry, 'vuln:summary')

        # Influenced vulnerable product
        products = entry.findall('.//vuln:product', namespace)
        productResult = [getText(_, '.') for _ in products]

        # Vulnerability references
        references = entry.findall('vuln:references', namespace)
        referenceResult = []
        for reference in references:
            _ = {}
            _['type'] = getAttrib(reference, '.', 'reference_type')
            _['source'] = getText(reference, 'vuln:source')
            _['reference'] = getText(reference, 'vuln:reference')
            _['url'] = getAttrib(reference, 'vuln:reference', 'href')
            referenceResult.append(_)

        # logical tests
        logicalTests = entry.findall('.//cpe-lang:fact-ref', namespace)
        logicalTestResult = [MySQLdb.escape_string(getAttrib(_, '.', 'name')) for _ in logicalTests]

        yield (nvdResult, productResult, referenceResult, logicalTestResult)

def saveToDatabase(nvdResult, productResult, referenceResult, logicalTestResult):
    cur.execute(INSERT_NVD % (
        nvdResult['cve_id'],
        nvdResult['published_datetime'],
        nvdResult['last_modified_datetime'],
        nvdResult['score'],
        nvdResult['access_vector'],
        nvdResult['access_complexity'],
        nvdResult['authentication'],
        nvdResult['confidentiality_impact'],
        nvdResult['integrity_impact'],
        nvdResult['availability_impact'],
        nvdResult['source'],
        nvdResult['generated_on_datetime'],
        nvdResult['cwe_id'],
        nvdResult['summary'],
    ))

    id = cur.lastrowid

    for product in productResult:
        cur.execute(INSERT_PRODUCT % (id, product))

    for reference in referenceResult:
        cur.execute(INSERT_REFERENCE % (id, reference['type'], reference['source'], reference['reference'], reference['url']))

    for logicalTest in logicalTestResult:
        cur.execute(INSERT_LOGICAL_TEST % (id, logicalTest))

    conn.commit()

def run():
    """
    Main function of nvdParser when running from command line.
    """

    root = et.ElementTree(file=xml).getroot()
    for data in genDatas(root):
        try:
            saveToDatabase(*data)
            print '[+] %s done.' % data[0]['cve_id']
        except MySQLdb.Error as e:
            print e[1]