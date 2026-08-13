# hxv4_unhash_tools

**Q1: 这是什么？**

A1: 帮助你还原经 hxv4 hash 后的文件名的一系列实用脚本，实测反哈希率可达到 90% 以上。

**Q2: 支持的范围？**

A2: 支持从 hxv4 crypted 游戏（举例：魔女的夜宴 Steam版、星光咖啡馆与死神之蝶 Steam版、天使嚣嚣 原版及 Hikari Field 版、Limelight Lemonade Jam 体验版及原版等）中还原以下文件名和目录名信息：

- 目录结构
- 场景文件（scn）
- 语音文件（voice）
- 音效文件（sound）
- 背景图片文件（bgimage）
- 背景音乐文件（bgm）
- 静态cg文件（evimage）
- 动态cg文件（sd）
- 人物立绘文件（fgimage）
- 视频文件（video）
- …………

项目当前针对 Dracu-Riot! Steam 版进行开发，因此对于其他游戏的支持可能有所欠缺。

若你完善了对其他游戏的支持，欢迎创建 Pull Request 来帮助这个项目变得更好！😘

**Q3: 如何使用？**

A3: 使用如下，请自行尝试：

1. 使用 KrkrExtractForCxdecV2（或 GARBro2 ，若支持目标游戏）提取 xp3 ；
2. 在 main.py 开头处更改目录配置及添加明文字典来源，具体使用方法可参照 main.py 中的注释；
3. 运行 main.py ，即可还原文件名并自动重命名文件名和目录名；
4. 运行后生成的 HxNames.lst 可供 GARbro 等工具使用。

    - 若做发布用途，建议使用 tools/generate_clean_hxnames.py 再生成一份干净的文件。

**注意：**项目在 Python 3.12 版本上开发，最低兼容 Python 3.10 版本，使用前请先确认你的 Python 版本是否满足条件。

**使用此项目生成：**

- [天使☆嚣嚣 RE-BOOT!（Hikari Field版） - ten_sz_hxnames](https://github.com/MLChinoo/ten_sz_hxnames)
- [Limelight Lemonade Jam - lllj_hxnames](https://github.com/MLChinoo/lllj_hxnames)
- [Dracu-Riot!（Steam版） - dracu_hxnames](https://github.com/MLChinoo/dracu_hxnames)
- [ガマンができない童貞兄キと、スナオになれない反抗妹』（略称：童貞兄妹) - HxNames-DTKD.lst](https://github.com/2778995958/gal_tachie_ai/blob/main/krkr/HxNames-DTKD.lst)
- [魔女的夜宴（Steam版） - sanoba_hxnames](https://github.com/MLChinoo/sanoba_hxnames)

**特别感谢：**

- [UlyssesWu/FreeMote](https://github.com/UlyssesWu/FreeMote)
- [YuriSizuku/GalgameReverse](https://github.com/YuriSizuku/GalgameReverse)
- [crskycode/GARbro](https://github.com/crskycode/GARbro)
- [YeLikesss/KrkrExtractForCxdecV2](https://github.com/YeLikesss/KrkrExtractForCxdecV2)
- [crskycode/KrkrDump](https://github.com/crskycode/KrkrDump)
- [UserUnknownFactor/GARbro2](https://github.com/UserUnknownFactor/GARbro2)
- [lictex/atri-composite](https://github.com/lictex/atri-composite)
- [MishaIac/KrkrHxv4Hash](https://github.com/MishaIac/KrkrHxv4Hash)
- [MLChinoo/TjsParser](https://github.com/MLChinoo/TjsParser)
- [2778995958/gal_tachie_ai](https://github.com/2778995958/gal_tachie_ai)
