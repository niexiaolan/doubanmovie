from urllib import parse
# 将中文分类标签转换为url编码
typelist = ['热门', '最新', '经典', '冷门佳片', '华语', '欧美', '韩国', '日本', '喜剧', '爱情', '科幻', '悬疑', '恐怖', '文艺']
codetypelist = []
for a in typelist:
    a = parse.quote(a)
    codetypelist.append(a)
print(codetypelist)
