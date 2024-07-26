- Required python version is 3.10

- clients folder contains synchronous client for ws, I started with sync client because most cases could be covered without async
- helpers folder generally contains only one helper for service start/stop during testrun
- models folder contains dataclasses for request/response parsing
- tests  folder contains tests.... generally for add_user endpoint and 1-2 cases for delete and select

all tests marked as skipped are skipped because of bug and skip reason contains description

Run tests and display all skip reasons:
```
pytest -rs
```

Skip Reasons:

```
SKIPPED [1] tests/test_add_user.py:91: Failure message for duplicate user creation case does not contain reason of failure (reason field is missing)
SKIPPED [1] tests/test_add_user_validation.py:14: buffer overflow (based on logs) when whole message is bigger then > 1024 symbols
SKIPPED [1] tests/test_add_user_validation.py:333: Overflow of unsigned int64 for age field
SKIPPED [1] tests/test_add_user_validation.py:375: float age is truncated to 3
SKIPPED [1] tests/test_add_user_validation.py:375: float age is truncated to 0
SKIPPED [1] tests/test_select_user.py:9: status field  contains failed status instead of success when search is successful
SKIPPED [1] tests/test_select_user.py:29: response does not contain users field when no matches in search
```