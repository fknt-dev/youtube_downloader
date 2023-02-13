import os
import subprocess
from pytube import YouTube
from os import getcwd

def mixar_arquivos(nome_do_video):
    pasta_local = getcwd() + '\\Videos\\'
    pasta_temporaria = getcwd() + '\\Temp\\'

    video = pasta_temporaria + nome_do_video + '-video.webm'
    audio = pasta_temporaria + nome_do_video + '-audio.webm'
    saida = pasta_local + nome_do_video + '.mkv'

    subprocess.run(f'mkvmerge -o "{saida}" "{video}" "{audio}" -q')
    os.remove(f'{video}'); os.remove(f'{audio}'); os.removedirs(pasta_temporaria)

def main():
    url_do_video = input('Digite o link do vídeo: ')
    yt = YouTube(url_do_video)

    pasta_destino = getcwd() + '\\Videos\\'
    pasta_temporaria = getcwd() + '\\Temp\\'

    video = yt.streams.get_by_itag(248)
    audio = yt.streams.get_by_itag(251)

    titulo_do_video = yt.title
    print(f'Baixando: "{titulo_do_video}"')

    video.download(pasta_temporaria, titulo_do_video+'-video.webm')
    audio.download(pasta_temporaria, titulo_do_video+'-audio.webm')

    localização = pasta_destino + titulo_do_video + '.mkv'
    print(f'Localização: "{localização}"')
    tamanho_em_mb = round(video.filesize_mb + audio.filesize_mb, 2)
    print(f'Tamanho do arquivo: {tamanho_em_mb} MB')

    mixar_arquivos(titulo_do_video)

if __name__ == '__main__':
    main()
