
小小总结器：具有三种总结方法的文本总结器

使用：
在python下运行NLPfinalUI.py 即可
cd to the directory of this work, then
run python NLPfinalUI.py 
that's all

功能：
支持三种不同总结方法
支持中英文
支持网页输入总结
支持总结句子数量选择
支持N-rouge对总结的文本评分
支持浏览文件夹选择文件
支持多页面切换
支持NER方法中，确定故事主人公之后，加入了后台实时搜索并显示主人公图片的功能

注意事项：
1.总结中文文本的时候，语言选项要改成Chinese，不然会崩溃
2.不要输入太大的文本，不然会崩溃
3.要用N-rouge评估文本的话，需要用到参考文本，在textdata/has_reference 文件夹中有一些


还没搞定：
1.HMM的训练没时间做了
2.文本框需要点击一下才能出现文字


