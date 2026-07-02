# hxv4_unhash_tools

**Q1: 这是什么？**

A1: 帮助你还原经hxv4 hash后的文件名的一系列实用脚本，实测反哈希率可达到90%以上。

**Q2: 支持的范围？**

A2: 支持从hxv4 crypted游戏（举例：魔女的夜宴 Steam版、星光咖啡馆与死神之蝶 Steam版、天使嚣嚣 原版及Hikari Field版、Limelight Lemonade Jam 体验版及原版等）中还原以下文件名和目录名信息：

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

项目当前针对Limelight Lemonade Jam进行开发，因此对于其他游戏的支持可能有所欠缺。

若你完善了对其他游戏的支持，欢迎创建Pull Request来帮助这个项目变得更好！😘

**Q3: 如何使用？**

A3: 使用如下，请自行尝试：

1. 使用KrkrExtractForCxdecV2（或GARBro2，若支持目标游戏）提取xp3；

2. [可选]使用utils/restore_dir_structure.py初步整理提取出的文件夹结构；

3. 在main.py开头处更改目录配置及添加明文字典来源，具体使用方法可参照main.py及plain_dict.py中的注释；

4. 运行main.py，即可还原文件名并自动重命名文件名和目录名；

5. 运行后生成的HxNames.lst可供GARbro等工具使用。

    - 若做发布用途，建议使用utils/generate_clean_hxnames.py再生成一份干净的文件。

**使用此项目生成：**

- [天使☆嚣嚣 RE-BOOT!（Hikari Field版） - ten_sz_hxnames](https://github.com/MLChinoo/ten_sz_hxnames)
- [Limelight Lemonade Jam - lllj_hxnames](https://github.com/MLChinoo/lllj_hxnames)
- [Dracu-Riot!（Steam版） - HxNames-DR.lst](https://github.com/2778995958/gal_tachie_ai/blob/main/yuzu/HxNames-DR.lst)
- [ガマンができない童貞兄キと、スナオになれない反抗妹』（略称：童貞兄妹) - HxNames-DTKD.lst](https://github.com/2778995958/gal_tachie_ai/blob/main/krkr/HxNames-DTKD.lst)
- [魔女的夜宴（Steam版） - sanoba_hxnames](https://github.com/MLChinoo/sanoba_hxnames)

**特别感谢：**

- [UlyssesWu/FreeMote](https://github.com/UlyssesWu/FreeMote)
- [YuriSizuku/GalgameReverse](https://github.com/YuriSizuku/GalgameReverse)
- [~~crskycode/GARbro~~](https://github.com/crskycode/GARbro)（已被删除，[Fork](https://github.com/MLChinoo/GARbro)）
- [YeLikesss/KrkrExtractForCxdecV2](https://github.com/YeLikesss/KrkrExtractForCxdecV2)
- [~~crskycode/KrkrDump~~](https://github.com/crskycode/KrkrDump)（已被删除，[Fork](https://github.com/MLChinoo/KrkrDump-Hasher)）
- [UserUnknownFactor/GARbro2](https://github.com/UserUnknownFactor/GARbro2)
- [lictex/atri-composite](https://github.com/lictex/atri-composite)
- [MishaIac/KrkrHxv4Hash](https://github.com/MishaIac/KrkrHxv4Hash)
