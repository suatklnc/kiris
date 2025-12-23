# Kiriş Analiz CLI (Beam Analysis Tool)

Saha mühendisleri için geliştirilmiş, Python tabanlı pratik bir kiriş analiz aracıdır. Basit mesnetli kirişler üzerindeki tekil ve düzgün yayılı yüklerin etkilerini analiz eder, reaksiyon kuvvetlerini hesaplar ve terminal üzerinde Kesme Kuvveti (SFD) ve Eğilme Momenti (BMD) diyagramlarını çizer.

## Özellikler

- **İnteraktif Sihirbaz:** Adım adım veri girişi.
- **Yük Tipleri:** Tekil Yük (Point Load) ve Düzgün Yayılı Yük (UDL).
- **Detaylı Raporlama:** Mesnet reaksiyonları ve kritik maksimum değerler.
- **Görselleştirme:** Terminal içinde renkli ASCII diyagramları.

## Kurulum

Bu proje [Poetry](https://python-poetry.org/) kullanılarak geliştirilmiştir.

1. Depoyu klonlayın:
   ```bash
   git clone <repo-url>
   cd conductortest
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   poetry install
   ```

## Kullanım

Uygulamayı hızlıca başlatmak için proje dizininde şu komutu çalıştırabilirsiniz:

```bash
./run
```

Alternatif olarak, Poetry ile manuel çalıştırmak isterseniz:

```bash
poetry run python beam_analysis/cli.py
```

Veya sanal ortam içinden:

```bash
.venv/bin/python beam_analysis/cli.py
```

### Örnek Senaryo

1. Uygulamayı başlatın.
2. Kiriş uzunluğu olarak `10` girin.
3. Yük Tipi olarak `Tekil Yük` seçin.
   - Kuvvet: `-10` (Aşağı yönlü 10kN)
   - Konum: `5` (Kirişin tam ortası)
4. `Analizi Başlat` seçeneğini seçin.
5. Sonuçları ve diyagramları inceleyin.

## Geliştirme

Testleri çalıştırmak için:

```bash
poetry run pytest
```
