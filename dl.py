from video_lib import dl_gif
import json
import re
import os


os.environ['all_proxy'] = 'http://127.0.0.1:1087'
with open('motions_cat.json', mode='r') as f:
    cat_dict = json.load(f)
wuti = 0
for _time in cat_dict.keys():
    cat = cat_dict[_time]
    if len(cat['videos']) != 0:
        print('now processing {0}...'.format(cat['body']))
        name = re.findall('(「.*」)', cat['body'])[0].replace(' ', '').replace('*', '白金之星')
        if name == '「無題」':
            name = '「無題{0}」'.format(wuti)
            wuti += 1
        if name+'.gif' not in os.listdir('gifs'):
            dl_gif(cat_dict[_time]['videos'][0], name, 'videos', 'gifs')