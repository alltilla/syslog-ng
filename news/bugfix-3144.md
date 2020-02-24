`python`: Now we store key-values in UTF-8 `str` instead of `byte`,
which was enforcing the user to put an extra `.decode()` call in `send()` with `python3`.
