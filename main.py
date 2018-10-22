# coding: utf-8
import re, os

# Check libs
try:
  import requests
  from bs4 import BeautifulSoup
  from lxml import html
  from pyfiglet import Figlet  
except ModuleNotFoundError:
  print('[INFO] Installing libraries\n')
  os.system('pip install requests bs4 lxml pyfiglet')
  import requests
  from bs4 import BeautifulSoup
  from lxml import html
  from pyfiglet import Figlet
except:
  print('Oops! Unknown error. Try again...')


headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,ru;q=0.9,en-US;q=0.8,uk;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'readmanga.me',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
      } 

def requests_r(url):
  return requests.session().get(url, headers = headers).text

def main():
  url_manga = input('Enter link to manga: ')

  first_r = requests_r(url_manga)
  url_read = html.fromstring(first_r).xpath('//div[@class = "subject-actions col-sm-7"]/a/@href')[0] 

  # Getting list of links to chapters
  print('[INFO] Getting list of links to chapters')
  second_r = requests_r('http://readmanga.me' + url_read)
  selectors = html.fromstring(second_r).xpath('//select[@id = "chapterSelectorSelect"]/option/@value')

  # Check link on "?mtr=1"
  if(selectors):
    pass
  else:
    second_r = requests_r('http://readmanga.me' + url_read + '?mtr=1')
    selectors = html.fromstring(second_r).xpath('//select[@id = "chapterSelectorSelect"]/option/@value')

  selectors.reverse()
  i_img = 0

  for selector in selectors:

    # Getting list of links to pictures
    print('[INFO] Getting list of links to pictures')
    imgs_r = requests_r('http://readmanga.me' + selector)
    urls = []
    result = re.findall(r'rm_h\.init\((.+\]\])', imgs_r)[0].split("],")

    for item in result:
      res = re.findall(r'\[\'\',\'(.+)\',"(.+)"', item)
      urls.append(res[0][0] + res[0][1])

    # Saving pictures in folder
    img_folder = selector.split("?")[0].split("/")
    img_folder_manga = img_folder[len(img_folder)-3]
    img_folder_vol = img_folder[len(img_folder)-2]
    img_folder_ch = img_folder[len(img_folder)-1]
    img_link_folder = 'Downloads/' + img_folder_manga + '/' + img_folder_vol + '/' + img_folder_ch + '/'
    print('[INFO] Saving pictures in folder ' + img_folder_vol + '/' + img_folder_ch)

    try:
      os.makedirs(img_link_folder)
    except OSError:
      pass

    for url in urls:
      img_name = url.split("?")[0].split("/")
      img_name = img_name[len(img_name)-1]
      r = requests.get(url, allow_redirects=True)
      open(img_link_folder + img_name, 'wb').write(r.content)
      print('[Downloaded] ' + img_link_folder + img_name)
      i_img += 1;

  print('\nSaving completed successfully!')
  print('Downloaded: ' + str(i_img) + ' pictures.\n')
  res_next = input('Want are you download other manga?? [Y/n] ')
  if (res_next == 'y' or res_next == 'yes'):
    main()
  else:
    input('Press enter and exit')

f = Figlet(font='slant')
print(f.renderText('CLI Manga Downloader'))
print('CLI "Manga Downloader" v1.0 | https://github.com/LightC0de/mangaDownloader')
main()