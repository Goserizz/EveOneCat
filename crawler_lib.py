import time


def scroll_to_bottom(browser):
    done = 0
    now_height = browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    while True:
        time.sleep(1)
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        prev_height = now_height
        now_height = browser.execute_script('return document.body.scrollHeight')
        if prev_height == now_height:
            done += 1
            if done == 30:  # 30 seconds no response, then break
                break
        else:
            done = 0
        print('\rWaited for {0}s...'.format(done), end='')
    return browser.execute_script('return document.body.scrollHeight')


def get_tweet(soup):
    '''

    :param soup:    BeautifulSoup object of a twitter home page
    :return:        a list contains all tweet info dictionaries.
                    info dict:{
                        "time": tweet time,
                        "body": body content,
                        "videos": [video_links, ],
                        "images": [image_links, ]
                    }
    '''

    ret = list()
    for article in soup.find_all('article'):
        _time = article.find('time')['datetime']
        body = ''
        videos = list()
        images = list()
        body_div = article.find('div', attrs={'lang': True})
        if body_div:
            tweet_div = body_div.parent
        else:
            tweet_div = article.contents[0].contents[1].contents[1]
        for child in tweet_div.descendants:
            if body_div and child in body_div.descendants:  # body content
                if child.name == 'span':
                    body += child.text
                elif child.name == 'img':
                    body += child['alt']
            else:
                if child.name == 'video':
                    videos.append(child['src'])
                elif child.name == 'img':
                    images.append(child['src'])
        ret.append({
            'time': _time,
            'body': body,
            'videos': videos,
            'images': images
        })

    return ret
