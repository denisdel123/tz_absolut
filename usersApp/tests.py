import pytest
from unittest.mock import patch
from usersApp.services import all_send_mail, create_secret_code, send_secret_code, confirm_email


@pytest.fixture
def mock_send_mail():
    with patch('usersApp.services.send_mail') as mock:
        yield mock


def test_all_send_mail_success(mock_send_mail):

    mock_send_mail.return_value = 1
    result = all_send_mail('Test Subject', 'Test Message', ['denis_belenko@mail.ru'])
    assert result is True

    mock_send_mail.assert_called_once_with(
        subject='Test Subject',
        message='Test Message',
        recipient_list=['denis_belenko@mail.ru'],
        from_email='denis_belenko@mail.ru'
    )


def test_all_send_mail_failure(mock_send_mail):
    mock_send_mail.side_effect = Exception('Failed to send')
    result = all_send_mail('Test Subject', 'Test Message', ['denis_belenko@mail.ru'])
    assert result is False
    mock_send_mail.assert_called_once_with(
        subject='Test Subject',
        message='Test Message',
        recipient_list=['denis_belenko@mail.ru'],
        from_email='denis_belenko@mail.ru'
    )


def test_create_secret_code():
    code = create_secret_code()
    assert len(code) == 4
    assert code.isdigit()


@patch('usersApp.services.all_send_mail')
def test_send_secret_code(mock_all_send_mail):
    email = 'denis_belenko@mail.ru'
    code = '1234'
    send_secret_code(email, code)
    mock_all_send_mail.assert_called_once_with(
        'Подтверждение Почты',
        'ваше код-слово 1234',
        [email]
    )


def test_confirm_email_success():
    result = confirm_email('1234', '1234')
    assert result is True


def test_confirm_email_failure():
    result = confirm_email('1234', '4321')
    assert result is False
