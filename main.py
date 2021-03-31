import XiaoHongShuSlider
import time



def read():
    pass

def startId(id):
    xiaohongshu = XiaoHongShuSlider.XiaoHongShu(id)
    xiaohongshu.download()

def startUrl(url):
    xiaohongshu = XiaoHongShuSlider.XiaoHongShu('',url)
    xiaohongshu.download()


if __name__ == '__main__':
    list = ['http://xhslink.com/UNtLQb','http://xhslink.com/WnBLQb','http://xhslink.com/KOFLQb','http://xhslink.com/hIOLQb',
            'http://xhslink.com/S1YLQb','http://xhslink.com/9c3LQb','http://xhslink.com/LobMQb','http://xhslink.com/ithMQb',
            'http://xhslink.com/IPnMQb','http://xhslink.com/MDqMQb','http://xhslink.com/z1vMQb']
    for url in list:
        startUrl(url)
        time.sleep(5)



