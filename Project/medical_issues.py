import xml.etree.ElementTree as ET

def get_medical_issues(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    issues = []
    for issue in root.findall("issue"):
        if issue.text:
            issues.append(issue.text.strip())

    issues.sort()
    return issues
