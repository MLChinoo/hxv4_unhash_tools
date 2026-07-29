from functools import wraps
from typing import TYPE_CHECKING

from config import Config
from plaintext_providers import (
    get_all_providers,
    get_provider,
    load_all_providers,
)

if TYPE_CHECKING:
    from plaintext_providers._typing import PlainDictProviders
else:
    class PlainDictProviders:
        pass


class PlainDict(PlainDictProviders):
    def __init__(self, config: Config, pathnames=None, filenames=None):
        self.config = config
        self.pathname_plaintexts = set(pathnames or ())
        self.filename_plaintexts = set(filenames or ())
        load_all_providers()

    def __getattr__(self, name):
        provider = get_provider(name)
        if provider is None:
            raise AttributeError(
                f"{type(self).__name__} 没有属性或 Provider：{name!r}"
            )

        @wraps(provider)
        def chained_provider(*args, **kwargs):
            result = provider(self, *args, **kwargs)
            if result is not None and result is not self:
                raise TypeError(
                    f"Provider {name!r} 不应返回其他对象，实际返回：{result!r}"
                )
            return self

        return chained_provider

    def __dir__(self):
        names = set(super().__dir__())
        names.update(get_all_providers())
        return sorted(names)
