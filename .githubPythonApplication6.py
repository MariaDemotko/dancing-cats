

import cv2
import numpy as np
import pygame
import threading
import time
import os
import platform

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def play_audio(path):
    pygame.mixer.init()
    try:
        # Если файла нет — просто пропустим аудио и не будем падать
        pygame.mixer.music.load(r"C:\Users\home\Desktop\ASII\коты_муз.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except Exception as e:
        print(f"Аудио не найдено или ошибка: {e}")


def convert_to_ascii(image, new_width=65):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    resized = cv2.resize(image, (new_width, new_height))

    ascii_chars = "@%#*+=-:. "
    max_idx = len(ascii_chars) - 1

    ascii_str = ''
    for row in resized:
        for pixel in row:
            idx = pixel // 28
            if idx > max_idx:
                idx = max_idx
            ascii_str += ascii_chars[idx]
        ascii_str += '\n'
    return ascii_str


def main():
    # 1. Инициализация pygame — обязательно в главном потоке
    pygame.init()
    # Параметры для более стабильного звука
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.mixer.init()

    video_path = r"C:\Users\home\Desktop\ASII\коты_вид.MP4"
    audio_path = r"C:\Users\home\Desktop\ASII\коты_муз.mp3"

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео. Проверь путь и имя файла.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 24
    frame_delay = 1 / fps

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = convert_to_ascii(frame)

        # 2. На первом кадре: запускаем музыку ПРЯМО ЗДЕСЬ, без вызова play_audio
        if frame_count == 0:
            if os.path.exists(audio_path):
                try:
                    pygame.mixer.music.load(audio_path)
                    pygame.mixer.music.play()
                except pygame.error as e:
                    print(f"Ошибка аудио: {e}")
            start_time = time.time()

        # 3. Синхронизация
        current_time = time.time()
        expected_time = start_time + frame_count * frame_delay

        if current_time < expected_time:
            time.sleep(expected_time - current_time)

        clear_screen()
        print(ascii_frame, end='')
        frame_count += 1

    cap.release()

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    pygame.quit()




if __name__ == "__main__":
    main()
