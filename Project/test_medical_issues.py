from medical_issues import get_medical_issues

def create_test_xml(tmp_path):
    xml_content = """\
<medical>
    <issue>Diabetes</issue>
    <issue>Asthma</issue>
    <issue>Blood Pressure</issue>
</medical>
"""
    file_path = tmp_path / "note.xml"
    file_path.write_text(xml_content)
    return file_path


def test_get_medical_issues_valid_file(tmp_path):
    xml_file = create_test_xml(tmp_path)
    result = get_medical_issues(xml_file)

    expected = ["Asthma", "Blood Pressure", "Diabetes"]
    assert result == expected


def test_get_medical_issues_not_empty(tmp_path):
    xml_file = create_test_xml(tmp_path)
    result = get_medical_issues(xml_file)

    assert len(result) > 0


def test_get_medical_issues_type(tmp_path):
    xml_file = create_test_xml(tmp_path)
    result = get_medical_issues(xml_file)

    assert isinstance(result, list)
