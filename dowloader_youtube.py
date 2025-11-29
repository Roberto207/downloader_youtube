#!/usr/bin/env python3

"""
YouTube Video Downloader
Baixa vídeos do YouTube com alta qualidade de vídeo e áudio.
"""

import yt_dlp
import os
import sys
from pathlib import Path


class YouTubeDownloader:
    def __init__(self, output_dir="downloads"):
        """
        Inicializa o downloader do YouTube.
        
        Args:
            output_dir (str): Diretório onde os vídeos serão salvos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def download_video(self, url, quality="best", audio_only=False, video_only=False):
        """
        Baixa um vídeo do YouTube.
        
        Args:
            url (str): URL do vídeo do YouTube
            quality (str): Qualidade do vídeo ('best', 'worst', ou formato específico)
            audio_only (bool): Se True, baixa apenas o áudio
            video_only (bool): Se True, baixa apenas o vídeo (sem áudio)
        
        Returns:
            bool: True se o download foi bem-sucedido, False caso contrário
        """
        
        # Configurações base do yt-dlp
        ydl_opts = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'writeinfojson': True,  # Salva metadados
            #'writesubtitles': True,  # Baixa legendas se disponíveis
            #'writeautomaticsub': True,  # Baixa legendas automáticas
        }
        
        # Configurações de formato baseadas nas opções
        if audio_only:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        elif video_only:
            ydl_opts['format'] = 'bestvideo/best'
        else:
            # Melhor qualidade de vídeo + áudio
            if quality == "best":
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best'
            else:
                ydl_opts['format'] = quality
            
            # Merge vídeo e áudio em MP4
            ydl_opts['merge_output_format'] = 'mp4'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extrai informações do vídeo
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Vídeo sem título')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Desconhecido')
                
                print(f"\n📹 Título: {title}")
                print(f"👤 Canal: {uploader}")
                print(f"⏱️  Duração: {duration // 60}:{duration % 60:02d}")
                print(f"📁 Salvando em: {self.output_dir}")
                print("\n🔄 Iniciando download...")
                
                # Faz o download
                ydl.download([url])
                print(f"\n✅ Download concluído com sucesso!")
                return True
                
        except Exception as e:
            print(f"\n❌ Erro durante o download: {e}")
            return False
    
    def download_playlist(self, url, quality="best"):
        """
        Baixa uma playlist inteira do YouTube.
        
        Args:
            url (str): URL da playlist do YouTube
            quality (str): Qualidade dos vídeos
        
        Returns:
            bool: True se todos os downloads foram bem-sucedidos
        """
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best',
            'outtmpl': str(self.output_dir / '%(playlist_title)s/%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'writeinfojson': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("🔄 Baixando playlist...")
                ydl.download([url])
                print("✅ Playlist baixada com sucesso!")
                return True
        except Exception as e:
            print(f"❌ Erro ao baixar playlist: {e}")
            return False
    
    def get_video_info(self, url):
        """
        Obtém informações sobre um vídeo sem baixá-lo.
        
        Args:
            url (str): URL do vídeo do YouTube
        
        Returns:
            dict: Informações do vídeo
        """
        ydl_opts = {'quiet': True}
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title'),
                    'uploader': info.get('uploader'),
                    'duration': info.get('duration'),
                    'view_count': info.get('view_count'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description', '')[:200] + '...'
                }
        except Exception as e:
            print(f"Erro ao obter informações: {e}")
            return None


def main():
    """Função principal com interface de linha de comando."""
    print("🎬 YouTube Video Downloader")
    print("=" * 40)
    
    downloader = YouTubeDownloader()
    
    while True:
        print("\nOpções:")
        print("1. Baixar vídeo")
        print("2. Baixar apenas áudio")
        print("3. Baixar playlist")
        print("4. Obter informações do vídeo")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == "1":
            url = input("URL do vídeo: ").strip() #aqui onde colocamos a url q queremos
            if url:
                downloader.download_video(url)
        
        elif choice == "2":
            url = input("URL do vídeo: ").strip()
            if url:
                downloader.download_video(url, audio_only=True)
        
        elif choice == "3":
            url = input("URL da playlist: ").strip()
            if url:
                downloader.download_playlist(url)
        
        elif choice == "4":
            url = input("URL do vídeo: ").strip()
            if url:
                info = downloader.get_video_info(url)
                if info:
                    print(f"\n📹 Título: {info['title']}")
                    print(f"👤 Canal: {info['uploader']}")
                    print(f"⏱️  Duração: {info['duration'] // 60 if info['duration'] else 0}:{info['duration'] % 60 if info['duration'] else 0:02d}")
                    print(f"👀 Visualizações: {info['view_count']:,}" if info['view_count'] else "👀 Visualizações: N/A")
                    print(f"📅 Data de upload: {info['upload_date']}")
                    print(f"📝 Descrição: {info['description']}")
        
        elif choice == "5":
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main()



