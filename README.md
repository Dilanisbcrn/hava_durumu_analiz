# hava_durumu_analiz
Hava Durumuna Dayalı Spotify Şarkı Popülerliği Tahmin ve Öneri Sistemi
1. Giriş
Teknolojik gelişmelerle birlikte bireylerin günlük yaşamları dijital ortamlarda şekillenmeye başlamış ve özellikle müzik dinleme alışkanlıkları kişisel tercihlere göre büyük bir çeşitlilik kazanmıştır. Bu tercihler yalnızca bireysel beğenilerden değil, aynı zamanda çevresel faktörlerden de etkilenmektedir. Yapılan araştırmalar, insanların ruh hâlinin ve çevresel koşulların (hava durumu gibi) müzik tercihleri üzerinde belirleyici bir etkisi olduğunu ortaya koymuştur. Bu noktadan hareketle, bu projede kullanıcıların o anki hava durumu bilgisi temel alınarak, onlara uygun Spotify şarkı önerilerinde bulunabilecek bir sistem geliştirilmiştir. Bu sistem, yalnızca öneri yapmakla kalmayıp aynı zamanda önerilen şarkıların popülerlik düzeyini de tahmin edebilen bir makine öğrenmesi modeli içermektedir. Proje boyunca kullanılan veri bilimi yöntemleri sayesinde, veri temizleme, dengesiz sınıfları dengeleme, model seçimi ve optimizasyon süreçleri titizlikle yürütülmüştür. Nihai hedef, kullanıcıya o anki çevresel koşullara göre anlamlı ve yüksek kaliteli öneriler sunmaktır.
2. Projenin Amacı
Bu çalışmanın temel amacı, Spotify platformunda yer alan şarkıların müzikal özelliklerini ve popülerlik düzeylerini analiz ederek, belirli bir hava durumu ile örtüşen ve kullanıcı deneyimini iyileştirebilecek öneriler sunan bir sistem oluşturmaktır.
Proje sayesinde:
Kullanıcılara ruh hâline daha uygun müzikler önerilmesi,
Spotify şarkı popülerliğinin tahminlenerek listeleme yapılması,
Veri bilimi ve makine öğrenmesi yöntemlerinin pratik bir probleme uygulanması,
Geliştirilen sistemin ileride kullanıcı geçmişine, saat dilimine ya da konuma göre genişletilebilecek altyapıya sahip olması amaçlanmaktadır.
Bu yönüyle proje, yalnızca akademik bir uygulama değil, aynı zamanda sektörel kullanıma da uygun bir öneri sisteminin temelini oluşturmaktadır.

3. Literatür Taraması
Müzik öneri sistemleri üzerine yapılan çalışmalar incelendiğinde, genellikle kullanıcıların dinleme geçmişi, beğeni listeleri ve popülerlik metrikleri temel alınarak öneriler sunulduğu görülmektedir. Bununla birlikte, Spotify gibi platformların sağladığı veri setleri kullanılarak, şarkıların ses özelliklerine (örneğin danceability, energy, tempo vb.) dayalı popülerlik tahmini ve öneri sistemleri yaygın olarak geliştirilmiştir. Ancak mevcut literatürde, hava durumu gibi çevresel verilerle entegre çalışan müzik öneri sistemlerinin sayısı oldukça sınırlıdır. Hava durumu gibi faktörlerin öneri algoritmalarına entegre edilmesi, kullanıcının ruh hâline uygun ve bağlama duyarlı bir dinleme deneyimi sunmak açısından yenilikçi bir yaklaşım olarak öne çıkmaktadır. Bu proje, hem şarkı popülerliği tahmini hem de hava durumu verisiyle eşleştirilmiş öneri sistemi geliştirmesi yönüyle literatürdeki benzer çalışmalardan ayrılmaktadır.
4.Veri Seti ve Özellikler
Kullanılan veri seti spotify_weather_data.csv dosyasından yüklenmiş ve aşağıdaki temel öznitelikler üzerine kurulmuştur:
Weather: Hava durumu (örneğin: sunny, rainy, cloudy)
Artist, Track Name, Album: Şarkıya dair temel bilgiler
Popularity: Spotify’da şarkının aldığı popülerlik puanı (0-100 arası)
Bu bilgilerden türetilen yeni öznitelikler:
popularity_category: Popularity skoruna göre kategorik sınıf ('low', 'medium', 'high')
Artist_Popularity: Her sanatçının ortalama popülerlik skoru
Track_Name_Length: Şarkı adının karakter uzunluğu
Album_Name_Length: Albüm adının karakter uzunluğu
4.1 Veri Ön İşleme
Veri seti temizlendikten sonra aşağıdaki işlemler uygulanmıştır:
Eksik veriler dropna() ile çıkarılmıştır.
Popularity değeri, pd.cut() yöntemiyle sınıflandırılarak popularity_category adlı yeni hedef sütun oluşturulmuştur.
Artist bazlı ortalama popülerlik (feature engineering) hesaplanmıştır.
Metin uzunluğu bilgileri (Track_Name_Length, Album_Name_Length) sayısal öznitelik olarak eklenmiştir.
4.2 Özellik Ayrımı ve Modelleme
Veri seti x ve y olarak bölünmüş, uygun öznitelikler belirlenmiştir:
Bağımsız değişkenler (x):
Kategorik: Weather, Artist
Sayısal: Artist_Popularity, Track_Name_Length, Album_Name_Length
Bağımlı değişken (y):
popularity_category (3 sınıflı)
Kategorik veriler, OneHotEncoder ile dönüştürülmüş, diğer sayısal öznitelikler olduğu gibi bırakılmıştır. Bu işlemler ColumnTransformer yardımıyla bir pipeline içinde toplanmıştır.
5. Modelleme ve Algoritmalar
Proje kapsamında üç farklı makine öğrenmesi algoritması denenmiş ve karşılaştırılmıştır:
5.1 Random Forest (SMOTE ile)
Random Forest, birden fazla karar ağacı oluşturarak tahminlerde bulunan güçlü bir topluluk (ensemble) öğrenme yöntemidir. SMOTE ile birlikte kullanıldığında özellikle az sayıda örneğe sahip sınıflarda bile yüksek başarı sağlayabilmektedir.
Doğruluk (Accuracy): %80.80
F1-score (macro avg): 0.79
Öne çıkan sınıf: Medium (F1-score: 0.83)
5.2 Logistic Regression
Basit, yorumlanabilir ve hızlı çalışan bir model olan lojistik regresyon, sınıflandırma problemlerinde sıkça tercih edilir. Bu projede referans model olarak değerlendirilmiştir. SMOTE uygulanmadan test edilmiştir.
Doğruluk: %80.43
F1-score dengeli fakat Random Forest’a göre daha düşüktür.
5.3 Decision Tree
Karar ağaçları veriyi dallara ayırarak tahmin yapar. Ancak aşırı öğrenmeye (overfitting) yatkın olması nedeniyle düşük performans sergilemiştir.
Doğruluk: %76.92
Özellikle "Low" sınıfında zayıf sonuçlar vermiştir.
6. Model Optimizasyonu
Random Forest algoritması, elde edilen ilk başarılı sonuçların ardından hiperparametre ayarlaması (GridSearchCV) ile daha da geliştirilmiştir. Bu sayede modelin doğruluk oranı %80.80’den %81.79’a yükseltilmiştir. F1-score da artış göstermiştir. Böylece model, kullanıcıya daha güvenilir tahminlerde bulunabilir hale gelmiştir.
7. Gerçek Zamanlı Öneri Sistemi
Modelin başarıyla eğitilmesinin ardından gerçek zamanlı öneri yapabilen bir sistem kurulmuştur. Kullanıcı sistemde o anki hava durumunu (örneğin: “Clouds”, “Rain”, “Clear”) girdikten sonra, sistem o hava durumuna göre en uygun ve popüler şarkıları listeler.
Örnek öneri çıktısı:
None by Billie Eilish (Popülerlik: 75, High olasılık: 0.982)
None by Måneskin (Popülerlik: 81, High olasılık: 0.978)
Öneri sistemi, kullanıcıların önerilen şarkıları beğenme ya da favorilere ekleme seçeneği sunar. Kullanıcı beğendiği şarkıları seçip favori listesi (CSV dosyası) olarak kaydedebilir. Bu özellik sayesinde kullanıcılar kendi kişiselleştirilmiş listelerini oluşturabilmektedir.
8. Model Seçiminin Gerekçesi
Random Forest algoritmasının tercih edilmesinin ana nedenleri şunlardır:
Sınıf ayrımı konusunda yüksek başarı: Hem Low hem High sınıflarında dengeli sonuçlar sunmuştur.
SMOTE ile yüksek uyum: Dengesiz veri setine rağmen güçlü genelleme kabiliyeti göstermiştir.
Yüksek doğruluk ve tutarlılık: Eğitim ve test verilerinde benzer sonuçlar vermiştir.
Parametre ayarlarıyla gelişebilir yapı: Hiperparametre optimizasyonu ile başarı oranı artırılmıştır.
Tüm bu nedenlerle Random Forest, öneri sistemi için en uygun model olarak seçilmiştir.
9. Sonuç 
Bu proje kapsamında hava durumu bilgisi ile entegre çalışan ve Spotify şarkılarının popülerliğini tahmin ederek öneride bulunan bir sistem başarıyla geliştirilmiştir. Random Forest algoritması en yüksek başarıyı göstermiş ve öneri sistemiyle entegre edilmiştir.
Bu çalışma, veri bilimi ve makine öğrenmesinin gerçek hayat problemlerine nasıl uygulanabileceğini göstermiş, kullanıcı odaklı, bağlamsal ve dinamik bir öneri sisteminin temelini atmıştır. Proje sonunda elde edilen sistem, kişiselleştirilmiş deneyim sunarken aynı zamanda müzik dinleme davranışlarını çevresel verilerle bütünleştiren yenilikçi bir yaklaşım ortaya koymuştur.
