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

## GitHub'a yükleme

Önce GitHub'da yeni bir repository oluşturun:

1. GitHub'a giriş yapın ve sağ üstteki **+** simgesinden **New repository** seçin.
2. Repository adı olarak `media_visualizer` yazın.
3. Public veya Private seçin.
4. **Add a README file** seçeneğini işaretlemeyin; bu proje zaten README içeriyor.
5. **Create repository** düğmesine basın.

Ardından proje klasöründe terminal açın. Aşağıdaki komutları sırayla çalıştırın. `KULLANICI_ADINIZ` kısmını GitHub kullanıcı adınızla değiştirin.

```powershell
# 1) Klasörü Git projesi yapar.
git init

# 2) Tüm proje dosyalarını hazırlama alanına ekler.
git add .

# 3) İlk sürümü kaydeder.
git commit -m "Initial media visualizer"

# 4) Ana dalın adını main yapar.
git branch -M main

# 5) GitHub'daki repository'yi bu yerel klasöre bağlar.
git remote add origin https://github.com/KULLANICI_ADINIZ/media_visualizer.git

# 6) Dosyaları GitHub'a gönderir.
git push -u origin main
```

İlk `git push` sırasında GitHub oturum açma penceresi açılır. Tarayıcıda hesabınızla giriş yapıp yetki verin. Eğer kullanıcı adı/parola sorulursa parola yerine GitHub'ın oluşturduğu bir **Personal Access Token** kullanmalısınız.

Sonraki güncellemeler için yalnızca şu üç komut yeterlidir:

```powershell
git add .
git commit -m "Güncelleme açıklaması"
git push
```

