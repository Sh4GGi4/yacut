import re
import string

ORIGINAL_MAX_LENGTH = 2048
SHORT_MAX_LENGTH = 16
SHORT_AUTO_LENGTH = 6
SHORT_CHARS = string.ascii_letters + string.digits
SHORT_PATTERN = f'^[{re.escape(SHORT_CHARS)}]+$'
RESERVED_SHORTS = ('files',)
SHORT_GENERATION_ATTEMPTS = 10

REDIRECT_VIEW = 'redirect_view'
