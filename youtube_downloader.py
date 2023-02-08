import os
import subprocess
from pytube import YouTube
from os import getcwd

def mixar_arquivos(nome_do_arquivo):
    pasta_local = getcwd() + '\\Videos\\'

    video = pasta_local + nome_do_arquivo + '.vp9'
    audio = pasta_local + nome_do_arquivo + '.opus'
    saida = pasta_local + nome_do_arquivo + '.mkv'

    subprocess.run(f'mkvmerge -o "{saida}" "{video}" "{audio}" -q')
    os.remove(f'{video}'); os.remove(f'{audio}')

def main():
    url_do_video = input('Digite o link: ')
    yt = YouTube(url_do_video)

    pasta_local = getcwd() + '\\Videos\\'
    print(pasta_local)

    nome_do_arquivo = yt.title
    print(f'Baixando: "{nome_do_arquivo}"')

    video = yt.streams.get_by_itag(248)
    audio = yt.streams.get_by_itag(251)

    tamanho_em_megabytes = round(video.filesize_mb, 2)

    print(f'Tamanho: {tamanho_em_megabytes}mb')

    video.download(output_path=pasta_local, filename=nome_do_arquivo+'.vp9')
    audio.download(output_path=pasta_local, filename=nome_do_arquivo+'.opus')

    mixar_arquivos(nome_do_arquivo)

if __name__ == '__main__':
    main()
