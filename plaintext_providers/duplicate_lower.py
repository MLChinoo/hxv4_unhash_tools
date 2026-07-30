"""
将现有pathname_plaintexts和filename_plaintexts复制一份小写副本并添加
如AppConfig.tjs则再添加一个appconfig.tjs
"""

from plain_dict import PlainDict
from plaintext_providers import register


@register(name="duplicate_lower")
def collect(self: PlainDict):
    self.pathname_plaintexts.update((_.lower() for _ in self.pathname_plaintexts.copy()))
    self.filename_plaintexts.update((_.lower() for _ in self.filename_plaintexts.copy()))
    return self
