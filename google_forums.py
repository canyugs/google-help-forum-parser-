# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
import datetime
import re
import json
import os
import sys

# topic reference
"""
<div __idx="1" class="BOXPGHD-F-c" style="outline:none;">
  <div class="BOXPGHD-S-Q BOXPGHD-S-T">
    <div class="BOXPGHD-S-R"><span><div class="BOXPGHD-S-F"><span><div class="BOXPGHD-S-o"></div></span><span><span class="BOXPGHD-b-rb BOXPGHD-S-I">已選取</span></span><span><span class="BOXPGHD-b-rb BOXPGHD-S-U">未讀訊息</span></span><span><div class="BOXPGHD-S-c BOXPGHD-D-b"><a href="#!profile/drive/APn2wQe1XvQ2GMYJ_jtxpvqrOAWzwu8SoyoH8_DOysb-8z7jrfCNw2DbbW77JPnBhyDf6owwVvq9"><img src="https://www.google.com/s2/photos/public/AIbEiAIAAABDCJaKwvHMjOG-XiILdmNhcmRfcGhvdG8qKDAwNDMwNmYwMjM2ZjE0NDMwNWVmYTk3ODg1MzM1YTM5OTlkNzc4M2MwATOBRvfDVfklEiyg-kw_CpenJA3b?sz=34" alt="Сергей Девяткин的個人資料相片"></a></div></span><span><div class="BOXPGHD-T-c"><div class="BOXPGHD-T-a" tabindex="0" role="checkbox" aria-checked="false"><div class="BOXPGHD-T-b"></div></div></div></span></div>
    </span><span><div class="BOXPGHD-S-l"><span><div class="BOXPGHD-U-c" role="button" aria-pressed="false"><div class="BOXPGHD-U-b"></div></div></span>
    <h3 class="BOXPGHD-S-O"><a href="#!topic/drive/0Pd_McE9kKg;context-place=forum/drive">When I add to "my drive" some folders and its content (third party ones with shared access from other users ) what will it happen ?</a></h3>
    <div class="BOXPGHD-S-N"></div>
    <div class="BOXPGHD-S-L">When I add to "my drive" some folders and its content (third party ones with shared access from other users ) what will it happen if admin remove me ...</div>
    <div class="BOXPGHD-V-m" gwtuirendered="gwt-uid-327">
      <div class="BOXPGHD-V-k"> <a class="BOXPGHD-V-c" href="#!profile/drive/APn2wQe1XvQ2GMYJ_jtxpvqrOAWzwu8SoyoH8_DOysb-8z7jrfCNw2DbbW77JPnBhyDf6owwVvq9"> 作者：Сергей Девяткин </a>
        <div class="BOXPGHD-V-j">下午8:46</div>
      </div>
      <div class="BOXPGHD-V-l">
        <div>1 則留言</div>
        <div>瀏覽次數：1</div>
      </div>
    </div>
  </div>
  </span>
</div>
</div>
</div>
"""

class topic:

    def __init__(self, topic_element):
        self.topic = topic_element

    def get_id(self):
        return int(self.topic.get_attribute('__idx'))

    def get_title(self):
        return self.topic.find_elements_by_tag_name('a')[1].text

    def get_content_link(self):
        return self.topic.find_elements_by_tag_name('a')[1].get_attribute('href')

    def get_time(self):
        return self.topic.find_element_by_class_name('BOXPGHD-V-j').text

    def get_response(self):
        string = self.topic.find_element_by_xpath('//div[@class="BOXPGHD-V-l"]/div[1]').text
        #  '6 則留言'
        return int(string.split(' ')[0])

    def get_view(self):
        string = self.topic.find_element_by_xpath('//div[@class="BOXPGHD-V-l"]/div[2]').text
        # '瀏覽次數：69'
        return int(string.split('：')[1])

    def get_expert_response(self):
        string = self.topic.find_element_by_xpath('//div[@class="BOXPGHD-V-l"]/div[3]').text
        return int(string.split(' ')[0])

    def as_dict(self):
        return {
            'title': self.get_title(),
            'time': self.get_time(),
            'content_link': self.get_content_link(),
            'response': self.get_response(),
            'views': self.get_view()
        }

class topic_content:
    pass

def get_all_topics(driver):
    log('Update array with all topic')
    return driver.find_elements_by_xpath('//div[@__idx]')


def get_all_topics_number(driver):
    num = len(get_all_topics(driver))
    print('Topic numbers: {}'.format(num))
    return num


def scroll_to_end(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def log(msg):
    print('LOG: {}'.format(msg))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        total_scroll_times = int(sys.argv[1])
    else:
        print('Usage:')
        print('     python {} <Scroll Times>'.format(sys.argv[0]))
        sys.exit()

    log('Initializing')
    json_encoder = json.JSONEncoder()
    file_op = open('posts.result', 'a', encoding = 'UTF-8')

    driver = webdriver.PhantomJS()

    log('Go to target site')
    driver.get('https://productforums.google.com/forum/#!forum/drive')
    
    log('Wait 10s for page loading')
    sleep(10)

    elements = get_all_topics(driver)
    initial_max = get_all_topics_number(driver)
    max = initial_max
    log('Grather post information: 1 ~ 30')

    init_tmp = {}
    for element in elements:
        post = topic(element)
        init_tmp[post.get_id()] = post.as_dict()
    json_string = json_encoder.encode(init_tmp)
    file_op.writelines(json_string)
    
    scroll_to_end(driver)
    sleep(10)


    for i in range(1, total_scroll_times):
        elements = get_all_topics(driver)
        log('Grather post information: {} ~ {}'.format(max, len(elements)))
        tmp = {}
        for element in elements[max + 1:]:
            post = topic(element)
            tmp[post.get_id()] = post.as_dict()

        json_string = json_encoder.encode(tmp)
        file_op.writelines(json_string)
        
        max = get_all_topics_number(driver)
        scroll_to_end(driver)
        sleep(max / 500) if max / 500 > 1 else sleep(3)

    driver.close()
