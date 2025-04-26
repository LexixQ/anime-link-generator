# Anime Link Generator

MyAnimeList üzerinde anime araması yaparak forumlarda veya diğer platformlarda kolayca paylaşmak için BBCode veya Markdown formatında linkler oluşturan basit bir masaüstü aracı.

![image](https://github.com/user-attachments/assets/c696e7a8-dfd0-4da9-acf3-1e9c38d80290)


## Özellikler

*   MyAnimeList üzerinde anime arama (Jikan API v4 aracılığıyla)
*   Arama sonuçlarını listede gösterme
*   Seçilen anime için kapak resmi (thumbnail) gösterme
*   BBCode veya Markdown formatında link oluşturma
*   Oluşturulan koda isteğe bağlı olarak şu bilgileri ekleme: Puan, Türler, Tip, Yıl, Resim Etiketi (`[img]`)
*   Oluşturulan kodu panoya kopyalama (manuel veya otomatik)
*   Açık/Koyu/Sistem teması desteği
*   Ayarların (limit, tema, otomatik kopya vb.) kaydedilmesi (`settings.json`)

## Gereksinimler

*   **Windows İşletim Sistemi**
*   **Python:** Sürüm 3.10 veya üzeri önerilir. (Python 3.10, 3.11, 3.12 ile test edilmiştir).
    *   **ÖNEMLİ:** Python yüklenirken **"Add Python X.Y to PATH"** seçeneğinin işaretlenmiş olması **gereklidir**.
    *   Eğer Python kurulu değilse, [Python İndirme Sayfası](https://www.python.org/downloads/)'ndan indirebilirsiniz.
*   **İnternet Bağlantısı:** İlk kurulum (`update.bat`) ve anime arama sırasında gereklidir.

## Kurulum ve Çalıştırma (Windows - Kolay Yöntem)

1.  **Projeyi İndirin:**
    *   Bu sayfanın sağ üstündeki yeşil `<> Code` butonuna tıklayın.
    *   "Download ZIP" seçeneğini seçin.
    *   İndirdiğiniz ZIP dosyasını **Türkçe karakter veya boşluk içermeyen** bir klasöre çıkartın (Örneğin: `C:\AnimeLinkGenerator`).

2.  **İlk Kurulumu Yapın:**
    *   Klasörün içine girin.
    *   `update.bat` dosyasına **çift tıklayarak** çalıştırın.
    *   Bu işlem, programın çalışması için gerekli olan sanal ortamı ve kütüphaneleri otomatik olarak kuracaktır. İnternet hızınıza bağlı olarak birkaç dakika sürebilir.
    *   Ekranda "Guncelleme ve kurulum tamamlandi!" mesajını gördüğünüzde bir tuşa basarak pencereyi kapatabilirsiniz.
    *   **Bu adımı sadece bir kere yapmanız yeterlidir** (veya programı güncellemek istediğinizde yapmalısınız).

3.  **Programı Çalıştırın:**
    *   Kurulum tamamlandıktan sonra, programı her çalıştırmak istediğinizde `run.bat` dosyasına **çift tıklayın**.
    *   Program arayüzü açılacaktır.

## Diğer Platformlar / Manuel Kurulum

Eğer Windows kullanmıyorsanız veya kurulumu manuel yapmak isterseniz:

1.  Depoyu klonlayın veya ZIP olarak indirin.
2.  Terminali açıp proje klasörüne gidin (`cd anime-link-generator`).
3.  Sanal ortam oluşturun: `python -m venv venv`
4.  Sanal ortamı aktifleştirin (Mac/Linux: `source venv/bin/activate`, Windows: `.\venv\Scripts\activate`).
5.  Bağımlılıkları yükleyin: `pip install -r requirements.txt`
6.  Programı çalıştırın: `python anime_bbcode_generator.py`

## Kullanım

1.  "Anime Adı" kutusuna aramak istediğiniz animeyi yazın.
2.  İsterseniz "Limit" kutusunu değiştirerek kaç sonuç listeleneceğini ayarlayın (varsayılan 10).
3.  "Ara" butonuna tıklayın veya Enter'a basın.
4.  Sol taraftaki "Arama Sonuçları" listesinden istediğiniz animeye tıklayın.
5.  Seçtiğiniz animenin resmi ve oluşturulan kod sağ tarafta görünecektir.
6.  Oluşturulan kodun formatını (BBCode/Markdown) ve koda eklenecek bilgileri (Puan, Tür, Tip, Yıl, Resim) alt kısımdaki seçeneklerle ayarlayın. Kod anlık olarak güncellenecektir.
7.  "Panoya Kopyala" butonu ile kodu kopyalayabilir veya ayarlardan "Otomatik Kopyala" seçeneğini aktif ettiyseniz, arama sonucuna tıkladığınızda kod otomatik olarak kopyalanacaktır.
8.  Seçili animenin MyAnimeList sayfasını tarayıcıda açmak için "MAL Sayfasını Aç" butonunu kullanabilirsiniz.

## Ayarlar

Program tema, limit, otomatik kopyalama tercihi gibi ayarlarınızı otomatik olarak programın çalıştığı klasörde oluşturulan `settings.json` dosyasına kaydeder. Programı tekrar başlattığınızda bu ayarlar yüklenir.

## Kaldırma

Programı kaldırmak için sadece indirdiğiniz ve çıkarttığınız `anime-link-generator` klasörünü silmeniz yeterlidir. Bilgisayarınıza başka bir kalıcı dosya yüklemez.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.
