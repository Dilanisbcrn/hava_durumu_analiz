# **Hava Durumuna Dayalı Spotify Şarkı Popülerliği Tahmin ve Öneri Sistemi**

---

## **1. Giriş**  
Teknolojik gelişmelerle birlikte bireylerin günlük yaşamları dijital ortamlarda şekillenmeye başlamış ve özellikle müzik dinleme alışkanlıkları kişisel tercihlere göre büyük bir çeşitlilik kazanmıştır. Bu tercihler yalnızca bireysel beğenilerden değil, aynı zamanda çevresel faktörlerden de etkilenmektedir. Yapılan araştırmalar, insanların ruh hâlinin ve çevresel koşulların (hava durumu gibi) müzik tercihleri üzerinde belirleyici bir etkisi olduğunu ortaya koymuştur.

Bu projede kullanıcıların o anki hava durumu bilgisi temel alınarak, onlara uygun Spotify şarkı önerilerinde bulunabilecek bir sistem geliştirilmiştir. Sistem, önerilen şarkıların popülerlik düzeyini de tahmin eden bir makine öğrenmesi modeli içermektedir. Proje boyunca veri temizleme, dengesiz sınıfları dengeleme, model seçimi ve optimizasyon süreçleri titizlikle yürütülmüştür. Nihai hedef, kullanıcıya o anki çevresel koşullara göre anlamlı ve yüksek kaliteli öneriler sunmaktır.

---

## **2. Projenin Amacı**  
Bu çalışmanın temel amacı, Spotify platformunda yer alan şarkıların müzikal özelliklerini ve popülerlik düzeylerini analiz ederek, belirli bir hava durumu ile örtüşen ve kullanıcı deneyimini iyileştirebilecek öneriler sunan bir sistem oluşturmaktır.

**Projenin hedefleri:**  
- Kullanıcılara ruh hâline daha uygun müzikler önerilmesi  
- Spotify şarkı popülerliğinin tahmin edilerek listeleme yapılması  
- Veri bilimi ve makine öğrenmesi yöntemlerinin pratik bir probleme uygulanması  
- İleride kullanıcı geçmişi, saat dilimi ve konuma göre genişletilebilecek altyapı sağlanması  

Bu yönüyle proje, hem akademik bir uygulama hem de sektörel kullanıma uygun bir öneri sistemi temelini oluşturmaktadır.

---

## **3. Literatür Taraması**  
Müzik öneri sistemleri genellikle kullanıcıların dinleme geçmişi, beğeni listeleri ve popülerlik metrikleri temel alınarak öneriler sunar. Spotify gibi platformların veri setleriyle ses özelliklerine dayalı popülerlik tahmini ve öneri sistemleri yaygındır. Ancak, hava durumu gibi çevresel verilerle entegre çalışan sistemler azdır.

Hava durumu faktörlerinin öneri algoritmalarına katılması, kullanıcının ruh hâline uygun, bağlama duyarlı dinleme deneyimi sunmak açısından yenilikçidir. Bu proje, hem şarkı popülerliği tahmini hem de hava durumu verisiyle entegre öneri sistemi geliştirmesiyle literatürdeki benzer çalışmalardan ayrılmaktadır.

---

## **4. Veri Seti ve Özellikler**

### **4.1 Kullanılan Veri Seti**  
Veri seti: `spotify_weather_data.csv`  
Temel öznitelikler:  
- Weather (hava durumu; örn. sunny, rainy, cloudy)  
- Artist, Track Name, Album  
- Popularity (0-100 arası Spotify popülerlik puanı)  

### **4.2 Türetilen Özellikler**  
- `popularity_category`: Popülerlik skoruna göre sınıflandırma ('low', 'medium', 'high')  
- `Artist_Popularity`: Her sanatçının ortalama popülerlik skoru  
- `Track_Name_Length`: Şarkı adının karakter uzunluğu  
- `Album_Name_Length`: Albüm adının karakter uzunluğu  

### **4.3 Veri Ön İşleme**  
- Eksik veriler `dropna()` ile çıkarıldı  
- Popularity, `pd.cut()` ile kategorilere ayrıldı  
- Artist bazlı ortalama popülerlik hesaplandı  
- Metin uzunlukları sayısal öznitelik olarak eklendi  

---

## **5. Modelleme ve Algoritmalar**

### **5.1 Özellik Ayrımı**  
- Bağımsız değişkenler (X):  
  - Kategorik: Weather, Artist  
  - Sayısal: Artist_Popularity, Track_Name_Length, Album_Name_Length  
- Bağımlı değişken (y): `popularity_category` (3 sınıf)  

Kategorik veriler `OneHotEncoder` ile dönüştürülüp, diğer sayısal özniteliklerle birlikte `ColumnTransformer` pipeline’ında toplandı.

### **5.2 Kullanılan Algoritmalar**  
- **Random Forest (SMOTE ile):**  
  Doğruluk: %80.80, F1-score: 0.79  
  Dengeli sınıflandırma ve güçlü genel performans  
- **Logistic Regression:**  
  Doğruluk: %80.43 (SMOTE uygulanmadan)  
- **Decision Tree:**  
  Doğruluk: %76.92, overfitting nedeniyle daha düşük performans  

---

## **6. Model Optimizasyonu**  
Random Forest hiperparametre ayarı (GridSearchCV) ile doğruluk %80.80’den %81.79’a çıkarıldı. Böylece model, daha güvenilir tahminler yapabilir hale geldi.

---

## **7. Gerçek Zamanlı Öneri Sistemi**  
Model eğitildikten sonra, kullanıcıdan alınan anlık hava durumu bilgisiyle en uygun ve popüler şarkıları listeleyen öneri sistemi geliştirildi. Kullanıcı, beğendiği şarkıları favori listesine ekleyebilir ve CSV dosyası olarak kaydedebilir.

---

## **8. Model Seçiminin Gerekçesi**  
- Yüksek sınıf ayrımı başarısı ve dengeli sonuçlar  
- SMOTE ile dengesiz veri üzerinde güçlü performans  
- Eğitim ve test verilerinde tutarlı sonuçlar  
- Hiperparametre ayarlarıyla gelişmeye açık yapı  

Bu nedenlerle Random Forest, sistem için en uygun model olarak tercih edilmiştir.

---

## **9. Sonuç**  
Bu proje, hava durumu verisi ile entegre çalışan ve Spotify şarkılarının popülerliğini tahmin ederek öneride bulunan yenilikçi bir sistem sunmaktadır. Veri bilimi ve makine öğrenmesinin gerçek hayat problemlerine uygulanmasını gösterirken, kullanıcılara kişiselleştirilmiş ve bağlamsal dinleme deneyimi sağlamaktadır.
