from unittest.mock import MagicMock, patch
from xml.etree import cElementTree as ET

from ngx_task import utils

SAMPLE_DOCUMENT = (
    b'<root><var name="id" value="some uuid" /><var name="level" value="2" />'
    b'<objects><object name="object1" /><object name="object2" /></objects></root>'
)


@patch('ngx_task.utils.uuid4')
@patch('ngx_task.utils.random')
@patch('ngx_task.utils.make_name')
def test_generate_document(mname_mock, random_mock, uuid_mock):
    random_mock.randint.return_value = 2
    uuid_mock.return_value = 'some uuid'
    mname_mock.side_effect = ['object1', 'object2', 'object3']

    document = utils.generate_document()
    uuid_mock.assert_called_once_with()
    assert len(mname_mock.mock_calls) == 2
    assert len(random_mock.mock_calls) == 2
    assert ET.tostring(document) == SAMPLE_DOCUMENT
