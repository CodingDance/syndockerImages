__author__ = 'hzyiting'
import os


def main():
    imageFile=open('picture.txt')
    url="https://hub.docker.com/public/images/official/"
    dirname="pictures"
    if os.path.exists(dirname)==False:
        os.mkdir(dirname)
    os.chdir(dirname)
    for imageName in imageFile.readlines():
        imageName = imageName.strip()
        imageUrl=url+imageName+".png"
        os.system("wget "+imageUrl)

if __name__ == '__main__':
    main()