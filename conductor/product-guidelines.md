# Product Guidelines - Kiriş Analiz CLI

Bu belge, uygulamanın tasarım, kullanıcı deneyimi ve teknik standartlarını belirler.

## Kullanıcı Deneyimi (UX) Prensipleri
*   **Öğretici ve Açıklayıcı:** Uygulama sadece sonuç üretmekle kalmaz, hesaplama adımlarını ve kullanılan formülleri açıklayarak kullanıcıya (mühendise) hesap sürecini takip etme şansı verir.
*   **Yardımsever Hata Yönetimi:** Hatalı veri girişlerinde kullanıcıyı suçlamak yerine, hatanın nedenini ve nasıl düzeltilebileceğini açık bir dille (yönlendirici ton) açıklar.

## Görsel Stil ve Çıktı Standartları
*   **Renkli Terminal Arayüzü:** Kritik noktalar (maksimum moment, mesnet reaksiyonları, aşırı yükleme uyarıları) renklerle vurgulanarak görsel hiyerarşi sağlanır.
*   **Zengin ASCII Grafikleri:** Kesme kuvveti ve moment diyagramları, terminal sınırları içinde anlamlı ve okunaklı bir şekilde çizilir.

## Yazılım Mimarisi
*   **Modüler Yapı:** Hesaplama çekirdeği (engine), görselleştirme modülü ve kullanıcı arayüzü birbirinden bağımsızdır. Bu sayede yeni yükleme veya analiz tipleri kolayca eklenebilir.

## Dokümantasyon
*   **Akademik Titizlikte Yardım:** Yardım komutları ve dokümantasyon, mühendislik yaklaşımlarını, kabulleri ve birim sistemlerini detaylı bir şekilde açıklar.
