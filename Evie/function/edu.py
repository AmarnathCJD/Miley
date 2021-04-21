import sys
import os
import subprocess
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
finally:
    import requests
import urllib, time
from io import BytesIO
from zipfile import ZipFile
import tarfile
try:
    from clint.textui import progress
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'clint'])
finally:
    from clint.textui import progress

######## This script is only for educational purpose ########
######## use it on your own RISK ########
######## I'm not responsible for any loss or damage ########
######## caused to you using this script ########
######## Github Repo - https://git.io/JJisT/ ########

def get_platform_architecture_chrome():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    else:
        print('Could not determine chromedriver download URL for this platform.')
    return platform, architecture


def get_chrome_version():
    """
    :return: the version of chrome installed on client
    """
    platform, _ = get_platform_architecture_chrome()
    if platform == 'linux':
        try:
            with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
                version = proc.stdout.read().decode('utf-8').replace('Chromium', '').strip()
                version = version.replace('Google Chrome', '').strip()
        except:
            return None
    else:
        await event.reply("System is.not lnux")
    try:
        version = version.split(' ')[0]
    except:
        pass
    return version

def get_major_version(version):
    return version.split('.')[0]

def get_chrome_driver_v(version):
    return requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + str(version)).text

def get_chrome_driver_dwnld_url(version):
    platform, architecture = get_platform_architecture_chrome()
    return 'https://chromedriver.storage.googleapis.com/' + str(version) + '/chromedriver_' + platform + str(architecture) + '.zip'

def dwnld_zip_file(url, save_path, chunk_size=128):
    print('Downloading...')
    r = requests.get(url)
    total_length = int(r.headers['Content-Length'])
    if total_length is None or total_length == 0:
        return print('Download failed')
    with ZipFile(BytesIO(r.content)) as my_zip_file:
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            pass
        print('Download Successful')
        my_zip_file.extractall(save_path)

def dwnld_tar_file(url, save_path):
    print('Downloading...')
    response = requests.get(url)
    total_length = sum(len(chunk) for chunk in response.iter_content(8196))
    if total_length is None or total_length == 0:
        return await event.reply('Download Failed')
    with tarfile.open(fileobj=BytesIO(response.content), mode='r|gz') as my_tar_file:
        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            pass
        print('Download Successful')
        my_tar_file.extractall(save_path)

def setup_Chrome(version):
    mjVer = get_major_version(version)
    if mjVer != None:
        print('Installed version - ' + str(mjVer))
        chromeDv = get_chrome_driver_v(mjVer)
        print('Chrome Driver Version Needed -', chromeDv)
        dwnldLink = get_chrome_driver_dwnld_url(chromeDv)
        dwnld_zip_file(dwnldLink, './webdriver')
    else:
        print('Chrome is not downloaded')
