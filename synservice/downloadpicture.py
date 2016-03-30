__author__ = 'hzyiting'
import os


def main():
    imageFile=open('image.txt')
    url="https://hub.docker.com/public/images/official/"
    for imageName in imageFile.readlines():
        imageName = imageName.strip()
        imageUrl=url+imageName+".png"
        os.system("wget "+imageUrl)

if __name__ == '__main__':
    main()