import streamlit as st
import os
import time
import tempfile
import numpy as np
from typing import Optional
import logging
import av
import queue

try:
    from streamlit_webrtc import (
        webrtc_streamer,
        WebRtcMode,
        RTCConfiguration,
        AudioProcessorBase,
        MediaStreamConstraints,
        WebRtcStreamerContext,
    )
    WEBRTC_AVAILABLE = True
except ImportError:
    WEBRTC_AVAILABLE = False
    logging.warning("streamlit-webrtc не установлен. Альтернативный компонент записи недоступен.")

class AudioRecorder:
    def __init__(self, use_fallback=False):
        self.use_fallback = use_fallback
        self.audio_data = None
        self.recording_state = {"recording": False, "finished": False}
    
    def use_webrtc_recorder(self):
        """Использует streamlit-webrtc для записи аудио"""
        if not WEBRTC_AVAILABLE:
            st.error("Не удалось импортировать streamlit-webrtc. Установите его с помощью: pip install streamlit-webrtc")
            return None
        
        st.info("Используется альтернативный метод записи аудио через WebRTC")
        
        class AudioProcessor(AudioProcessorBase):
            def __init__(self):
                self.audio_buffer = []
                self.sample_rate = 16000
                self.audio_queue = queue.Queue()
                self.recording = False
                
            def recv(self, frame):
                """Получение аудио-фрейма от WebRTC"""
                if self.recording:
                    sound = frame.to_ndarray()
                    sound = sound.reshape(-1)
                    self.audio_buffer.extend(sound.tolist())
                return frame
            
            def get_audio_data(self):
                """Возвращает накопленные аудио-данные как байты в формате WAV"""
                if not self.audio_buffer:
                    return None
                
                # Создание WAV-файла из накопленных данных
                import wave
                import io
                
                audio_bytes = io.BytesIO()
                with wave.open(audio_bytes, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Моно
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(self.sample_rate)
                    audio_array = np.array(self.audio_buffer, dtype=np.int16)
                    wav_file.writeframes(audio_array.tobytes())
                
                return audio_bytes.getvalue()
        
        # Конфигурация ICE-серверов для WebRTC
        rtc_configuration = RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )
        
        # Создаем вертикальные колонки для лучшего расположения элементов
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Настройка WebRTC стримера
            audio_processor = AudioProcessor()
            webrtc_ctx = webrtc_streamer(
                key="audio-recorder",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=rtc_configuration,
                media_stream_constraints={"video": False, "audio": True},
                audio_processor_factory=lambda: audio_processor,
                async_processing=True,
            )
        
        with col2:
            # Кнопки управления записью
            if webrtc_ctx.state.playing:
                if st.button("🔴 Начать запись", disabled=audio_processor.recording):
                    audio_processor.recording = True
                    audio_processor.audio_buffer = []  # Очистка буфера
                    st.session_state['webrtc_recording'] = True
                
                if st.button("⏹️ Остановить запись", disabled=not audio_processor.recording):
                    audio_processor.recording = False
                    st.session_state['webrtc_recording'] = False
                    
                    # Получаем записанное аудио
                    audio_data = audio_processor.get_audio_data()
                    if audio_data:
                        st.session_state['webrtc_audio_data'] = audio_data
                        st.success("Аудио успешно записано!")
                        st.audio(audio_data, format="audio/wav")
                        return audio_data
                    else:
                        st.error("Не удалось записать аудио. Попробуйте еще раз.")
                
                # Отображаем статус записи
                if 'webrtc_recording' in st.session_state and st.session_state['webrtc_recording']:
                    st.markdown("#### 🔴 Идет запись...")
        
        # Возвращаем ранее записанное аудио, если оно есть
        if 'webrtc_audio_data' in st.session_state:
            return st.session_state['webrtc_audio_data']
        
        return None
    
    def use_standard_recorder(self):
        """Использует стандартный st.audio_input"""
        audio_data = st.audio_input("Нажмите для записи аудио")
        return audio_data
    
    def record_audio(self) -> Optional[bytes]:
        """Записывает аудио и возвращает его как bytes"""
        # Сначала пробуем использовать стандартный компонент, если не указано иное
        if not self.use_fallback:
            audio_data = self.use_standard_recorder()
            if audio_data is not None:
                return audio_data
        
        # Если стандартный компонент не работает или указан fallback, используем WebRTC
        return self.use_webrtc_recorder()
    
    def render_audio_recorder(self, title="Запись аудио"):
        """Отображает интерфейс записи аудио и возвращает записанные данные"""
        st.subheader(title)
        
        # Добавляем переключатель для выбора метода записи
        record_method = st.radio(
            "Выберите метод записи аудио:",
            ["Стандартный (для локального использования)", "Альтернативный (для удаленных серверов)"],
            index=1 if self.use_fallback else 0,
        )
        
        self.use_fallback = record_method == "Альтернативный (для удаленных серверов)"
        
        # Отображаем соответствующий компонент записи
        audio_data = None
        if self.use_fallback:
            audio_data = self.use_webrtc_recorder()
        else:
            audio_data = self.use_standard_recorder()
        
        # Возвращаем записанные данные
        return audio_data

def create_audio_recorder(use_fallback=False):
    """Фабричная функция для создания экземпляра аудио-рекордера"""
    return AudioRecorder(use_fallback=use_fallback) 