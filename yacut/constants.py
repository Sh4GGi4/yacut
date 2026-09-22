import string

ORIGINAL_MAX_LENGTH = 2048
SHORT_MAX_LENGTH = 16
SHORT_AUTO_LENGTH = 6
SHORT_CHARS = string.ascii_letters + string.digits
SHORT_PATTERN = r'^[A-Za-z0-9]+$'
RESERVED_SHORTS = ('files',)
SHORT_GENERATION_ATTEMPTS = 10

INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
DUPLICATE_SHORT_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
LONG_ORIGINAL_MESSAGE = 'Указана слишком длинная ссылка'
SHORT_GENERATION_FAILED_MESSAGE = (
    'Не удалось сгенерировать уникальную короткую ссылку'
)
