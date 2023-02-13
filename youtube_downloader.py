import logging
from os import getcwd
from pytube import YouTube, request, exceptions as e
from pytube.cli import on_progress
from shutil import rmtree
from subprocess import run

request.default_range_size = 1048576
pasta_destino = getcwd() + '\\Vídeos baixados\\'
pasta_temporaria = getcwd() + '\\Arquivos temporários\\'

def mesclando_arquivos(titulo_do_video):
    video = pasta_temporaria + f'{titulo_do_video}-video.webm'
    audio = pasta_temporaria + f'{titulo_do_video}-audio.webm'
    saida = pasta_destino + f'{titulo_do_video}.mkv'

    run(f'mkvmerge -o "{saida}" "{video}" "{audio}" -q')
    rmtree(pasta_temporaria)

def remover_caracteres_especiais(titulo_do_video):
    caracteres_especiais = '\/:*?"<>|'

    for caractere in caracteres_especiais:
        if caractere in titulo_do_video:
            titulo_do_video = titulo_do_video.replace(caractere, '-')

    return titulo_do_video

def gerenciador_de_downloads(url_do_video):
    try:
        objeto = YouTube(url_do_video, on_progress_callback=on_progress)
        exception = False
    except e.VideoPrivate as private:
        exception = private
    except e.VideoRegionBlocked as region_blocked:
        exception = region_blocked
    except e.VideoUnavailable as unavailable:
        exception = unavailable
    except e.RegexMatchError as regex_error:
        exception = regex_error
    if exception is not False:
        logging.warning(f'Nome da exceção: {exception}')
        logging.warning(f'Descrição da exceção: {type(exception).__name__}')
        return

    titulo_do_video = remover_caracteres_especiais(objeto.title)
    print(f'Título do vídeo: "{titulo_do_video}"')

    video = objeto.streams.filter(adaptive=True, file_extension='webm', type='video').first()
    audio = objeto.streams.filter(adaptive=True, file_extension='webm', type='audio').last()

    print('Baixando o vídeo em separado...')
    video.download(pasta_temporaria, f'{titulo_do_video}-video.webm'); print()
    print('Baixando a faixa de áudio...')
    audio.download(pasta_temporaria, f'{titulo_do_video}-audio.webm'); print()
    print('Mesclando os arquivos...')
    mesclando_arquivos(titulo_do_video)

    localização = pasta_destino + titulo_do_video + '.mkv'
    tamanho_em_mb = str(round(video.filesize_mb + audio.filesize_mb, 2)).replace('.', ',')

    print(f'O vídeo foi salvo em: "{localização}"')
    print(f'Tamanho do arquivo: {tamanho_em_mb} MB')

if __name__ == '__main__':
    url_do_video = input('Digite o link do vídeo: ')
    gerenciador_de_downloads(url_do_video)
