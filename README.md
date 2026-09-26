# Media Visualizer

Python ve Tkinter ile geliştirilmiş basit bir masaüstü görsel görselleştirici uygulamasıdır. PNG, JPG ve JPEG dosyalarını açabilir; siyah-beyaz, sepya, negatif filtreleri ile parlaklık ayarı uygulayabilir ve sonucu yeni dosya olarak kaydedebilirsiniz.

Bu proje özellikle anlaşılır kalması için tek Python dosyasında tutulmuştur.

## Hızlı kurulum ve çalıştırma

1. Bilgisayarınızda Python 3.10 veya daha yeni bir sürüm olduğundan emin olun. [Python indirme sayfasından](https://www.python.org/downloads/) indirin. Kurulum ekranında **Add Python to PATH** seçeneğini işaretleyin.
2. Proje klasörünü indirin veya GitHub'dan klonlayın.
3. Klasörde terminal açın ve şu komutları çalıştırın:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

PowerShell etkinleştirme izni vermezse, yalnızca o terminal oturumu için şu komutu çalıştırın:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Ardından `.venv\Scripts\Activate.ps1` komutunu tekrar kullanın.

## Kolay kullanım: EXE oluşturma

Python yüklüyse, bağımlılıkları kurduktan sonra `build_exe.bat` dosyasına çift tıklayın. İşlem bittiğinde şu dosya oluşur:

```text
dist\MediaVisualizer.exe
```

Bu `.exe` dosyası tek başına çalışır; hedef bilgisayarda Python kurulmasına gerek yoktur. İlk oluşturma birkaç dakika sürebilir. EXE'yi paylaşırken sadece `dist` klasöründeki dosyayı göndermeniz yeterlidir.

Alternatif olarak terminalden:

```powershell
pyinstaller --noconfirm --onefile --windowed --name MediaVisualizer main.py
```

> Not: Windows SmartScreen, kendi oluşturduğunuz imzasız EXE'lerde uyarı gösterebilir. Bu normaldir; kaynak kodu siz oluşturduğunuz için güvenliğinden emin olduğunuz dosyalarda çalıştırın.

## Sound Visualizer (Windows system audio)

The Sound Visualizer captures the default Windows speaker output, so it can display audio from apps such as Spotify while they play. It uses Windows WASAPI loopback through the `soundcard` package and shows a CAVA-inspired spectrum.

Install its separate dependencies and run it:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r sound_requirements.txt
python sound_visualizer.py
```

Build its standalone Windows executable with:

```powershell
python -m PyInstaller --noconfirm --onefile --windowed --name SoundVisualizer sound_visualizer.py
```
