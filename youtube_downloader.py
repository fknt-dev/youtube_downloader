from os import getcwd, remove, removedirs
from pytube import YouTube
from subprocess import run

pasta_destino = getcwd() + '\\Vídeos\\'
pasta_temporaria = getcwd() + '\\Temp\\'

def mixar_arquivos(titulo_do_video):
    video = pasta_temporaria + f'{titulo_do_video}-video.webm'
    audio = pasta_temporaria + f'{titulo_do_video}-audio.webm'
    saida = pasta_destino + f'{titulo_do_video}.mkv'

    run(f'mkvmerge -o "{saida}" "{video}" "{audio}" -q')
    remove(video); remove(audio); removedirs(pasta_temporaria)

def gerenciador_de_downloads():
    url_do_video = input('Digite o link do vídeo: ')
    yt = YouTube(url_do_video)
    titulo_do_video = yt.title

    caracteres_especiais = '\/:*?"<>|'
    for caractere in caracteres_especiais:
        if caractere in titulo_do_video:
            titulo_do_video = titulo_do_video.replace(caractere, '-')

    video = yt.streams.get_by_itag(248)
    audio = yt.streams.get_by_itag(251)

    print(f'Baixando: "{titulo_do_video}"')
    video.download(pasta_temporaria, f'{titulo_do_video}-video.webm')
    audio.download(pasta_temporaria, f'{titulo_do_video}-audio.webm')

    mixar_arquivos(titulo_do_video)

    localização = pasta_destino + titulo_do_video + '.mkv'
    tamanho_em_mb = round(video.filesize_mb + audio.filesize_mb, 2)
    print(f'Localização: "{localização}"')
    print(f'Tamanho do arquivo: {tamanho_em_mb} MB')

if __name__ == '__main__':
    gerenciador_de_downloads()
