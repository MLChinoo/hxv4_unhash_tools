import importlib
import pkgutil
from collections.abc import Callable
from typing import Any


Provider = Callable[..., Any]

_loaded = False
_providers: dict[str, Provider] = {}


def register(function: Provider | None = None, *, name: str | None = None):
    """Register a plaintext provider under its public chain-method name."""

    def decorator(provider: Provider) -> Provider:
        provider_name = name or provider.__name__
        if not provider_name.isidentifier():
            raise ValueError(f"非法 Provider 名称：{provider_name}")
        if provider_name in _providers:
            previous = _providers[provider_name]
            raise ValueError(
                f"Provider 重复注册：{provider_name}\n"
                f"已有：{previous.__module__}.{previous.__name__}\n"
                f"新增：{provider.__module__}.{provider.__name__}"
            )
        _providers[provider_name] = provider
        return provider

    if function is None:
        return decorator
    return decorator(function)


def get_provider(name: str) -> Provider | None:
    return _providers.get(name)


def get_all_providers() -> dict[str, Provider]:
    return _providers.copy()


def load_all_providers() -> None:
    """Import every provider module once so its decorator can register it."""
    global _loaded
    if _loaded:
        return

    for module_info in pkgutil.iter_modules(__path__):
        module_name = module_info.name
        if module_name.startswith("_"):
            continue
        importlib.import_module(f"{__name__}.{module_name}")

    _loaded = True
