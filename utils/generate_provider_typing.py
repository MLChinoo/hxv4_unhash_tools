import ast
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
PROVIDER_DIR = PROJECT_DIR / "plaintext_providers"
OUTPUT_FILE = PROVIDER_DIR / "_typing.py"


def _registered_name(function: ast.FunctionDef) -> str | None:
    for decorator in function.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "register":
            return function.name
        if not isinstance(decorator, ast.Call):
            continue
        if not isinstance(decorator.func, ast.Name):
            continue
        if decorator.func.id != "register":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
        return function.name
    return None


def _format_parameter(
    argument: ast.arg,
    default: ast.expr | None = None,
) -> str:
    result = argument.arg
    if argument.annotation is not None:
        result += f": {ast.unparse(argument.annotation)}"
    if default is not None:
        result += f" = {ast.unparse(default)}"
    return result


def _format_signature(function: ast.FunctionDef) -> str:
    positional = [
        *function.args.posonlyargs,
        *function.args.args,
    ]
    if not positional:
        raise TypeError(
            f"{function.name} 缺少 PlainDict 参数"
        )

    positional = positional[1:]
    defaults = [None] * (
        len(positional) - len(function.args.defaults)
    ) + list(function.args.defaults)

    parameters = ["self"]
    parameters.extend(
        _format_parameter(argument, default)
        for argument, default in zip(positional, defaults)
    )

    if function.args.vararg is not None:
        parameters.append(
            f"*{_format_parameter(function.args.vararg)}"
        )
    elif function.args.kwonlyargs:
        parameters.append("*")

    parameters.extend(
        _format_parameter(argument, default)
        for argument, default in zip(
            function.args.kwonlyargs,
            function.args.kw_defaults,
        )
    )

    if function.args.kwarg is not None:
        parameters.append(
            f"**{_format_parameter(function.args.kwarg)}"
        )

    return ", ".join(parameters)


def _discover_methods():
    methods = []

    for filepath in sorted(PROVIDER_DIR.glob("*.py")):
        if filepath.name.startswith("_"):
            continue

        tree = ast.parse(
            filepath.read_text(encoding="utf-8"),
            filename=str(filepath),
        )
        registered_functions = [
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and _registered_name(node) is not None
        ]

        if len(registered_functions) != 1:
            raise ValueError(
                f"{filepath.name} 必须包含且仅包含一个注册的 Provider"
            )

        function = registered_functions[0]
        methods.append(
            (
                _registered_name(function),
                _format_signature(function),
            )
        )

    return sorted(methods)


def generate():
    method_lines = []
    for name, signature in _discover_methods():
        method_lines.extend(
            [
                f"    def {name}({signature}) -> PlainDict:",
                "        ...",
                "",
            ]
        )

    content = "\n".join(
        [
            "# 此文件由 utils/generate_provider_typing.py 自动生成，请勿手动修改。",
            "from __future__ import annotations",
            "",
            "from collections.abc import Iterable",
            "from pathlib import Path",
            "from typing import TYPE_CHECKING, Any",
            "",
            "if TYPE_CHECKING:",
            "    from plain_dict import PlainDict",
            "",
            "",
            "class PlainDictProviders:",
            *method_lines,
        ]
    )
    OUTPUT_FILE.write_text(content.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate()
