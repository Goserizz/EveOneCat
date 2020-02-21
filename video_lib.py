import requests
from contextlib import closing
import os


class ProgressBar(object):

    '''
    作者：微微寒
    链接：https://www.zhihu.com/question/41132103/answer/93438156
    来源：知乎
    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    '''

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def dl_gif(url, name, video_dir='./', gif_dir='./'):
    '''
    :param url:         video url
    :param name:        name of the video
    :param video_dir:   directory name of video to store
    :param gif_dir:     directory name of gif to store
    :return:            None
    '''
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        progress = ProgressBar(name, total=content_size, unit='KB', chunk_size=chunk_size,
                               run_status='Downloading', fin_status='Done')
        with open(os.path.join(video_dir, name+'.mp4'), 'wb') as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                progress.refresh(count=len(data))
    os.system('ffmpeg -y -i {0}.mp4  -filter_complex \"[0:v] fps=30,scale=w=480:h=-1,split [a][b];\
    [a] palettegen=stats_mode=single [p];[b][p] paletteuse=new=1" {1}.gif'.format(
        os.path.join(video_dir, name),
        os.path.join(gif_dir, name)))
