import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier  # Burada eklendi
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import warnings

warnings.filterwarnings('ignore')

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna()

    data['popularity_category'] = pd.cut(
        data['Popularity'],
        bins=[-0.1, 20, 60, 100],
        labels=['low', 'medium', 'high']
    )

    data['Artist_Popularity'] = data.groupby('Artist')['Popularity'].transform('mean')
    data['Track_Name_Length'] = data['Track Name'].str.len()
    data['Album_Name_Length'] = data['Album'].str.len()

    return data

def prepare_features(data):
    features = ['Weather', 'Artist', 'Artist_Popularity', 'Track_Name_Length', 'Album_Name_Length']
    X = data[features]
    y = data['popularity_category']
    return X, y

def build_pipeline(model, use_smote=False):
    categorical_features = ['Weather', 'Artist']
    numerical_features = ['Artist_Popularity', 'Track_Name_Length', 'Album_Name_Length']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', 'passthrough', numerical_features)
        ])

    if use_smote:
        pipeline = ImbPipeline([
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', model)
        ])
    else:
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])

    return pipeline

def optimize_hyperparameters(pipeline, X_train, y_train):
    param_dist = {
        'classifier__n_estimators': [100, 200, 300, 400],
        'classifier__max_depth': [5, 10, 15, 20, None],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4]
    }

    random_search = RandomizedSearchCV(
        pipeline, param_distributions=param_dist,
        n_iter=20, cv=3, verbose=1, n_jobs=-1, random_state=42
    )
    random_search.fit(X_train, y_train)
    print("En iyi parametreler:", random_search.best_params_)
    return random_search.best_estimator_

def recommend_songs(data, model, weather_input, top_n=5):
    data_copy = data.copy()
    data_copy['Weather'] = weather_input

    features = ['Weather', 'Artist', 'Artist_Popularity', 'Track_Name_Length', 'Album_Name_Length']
    X_input = data_copy[features]

    probs = model.predict_proba(X_input)
    classes = list(model.named_steps['classifier'].classes_)
    high_index = classes.index('high')
    high_probs = probs[:, high_index]

    data_copy = data_copy.reset_index(drop=True)
    data_copy['high_prob'] = high_probs

    top_songs = data_copy.sort_values(by='high_prob', ascending=False).head(top_n)

    print(f"\nGirilen hava durumu: '{weather_input}' için en popüler {top_n} şarkı:")
    for idx, row in enumerate(top_songs.itertuples(), 1):
        print(f"{idx}. {row._asdict().get('Track Name')} by {row.Artist} (Popularity: {row.Popularity}, High olasılık: {row.high_prob:.3f})")

    # 🎯 Favorilere ekleme
    favorites = []
    try:
        choices = input("\n💾 Favorilere eklemek istediğiniz şarkı numaralarını virgülle ayırarak girin (örn: 1,3,5): ")
        indexes = [int(i.strip()) for i in choices.split(',')]
        for i in indexes:
            if 1 <= i <= len(top_songs):
                favorites.append(top_songs.iloc[i - 1])
    except:
        print("Geçersiz giriş. Hiçbir şarkı favorilere eklenmedi.")

    if favorites:
        fav_df = pd.DataFrame(favorites)
        fav_df.to_csv('favori_sarkilar.csv', mode='a', header=False, index=False)
        print("\n⭐ Seçilen favori şarkılar 'favori_sarkilar.csv' dosyasına eklendi.")
    else:
        print("Hiçbir şarkı kaydedilmedi.")



def main():
    print("Spotify Şarkı Popülerlik Tahmini Başlatılıyor...\n")

    data = load_and_preprocess_data('spotify_weather_data.csv')
    print("Sınıf Dağılımı:")
    print(data['popularity_category'].value_counts())

    X, y = prepare_features(data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)

    model_candidates = {
        'Random Forest': (RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1), True),
        'Logistic Regression': (LogisticRegression(max_iter=1000, random_state=42), False),
        'Decision Tree': (DecisionTreeClassifier(random_state=42, class_weight='balanced'), False)
    }

    results = {}

    print("\nFarklı modeller test ediliyor...\n")
    for name, (base_model, use_smote) in model_candidates.items():
        print(f"{name} modeli için pipeline kuruluyor... (SMOTE: {use_smote})")
        pipeline = build_pipeline(base_model, use_smote)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        print(f"{name} Doğruluk (Accuracy): {acc:.4f}")
        print(f"{name} Detaylı Rapor:")
        print(classification_report(y_test, y_pred))

        results[name] = acc

    best_model_name = max(results, key=results.get)
    print(f"\nEn iyi model: {best_model_name} (Doğruluk: {results[best_model_name]:.4f})")

    if best_model_name == 'Random Forest':
        print("\nRandom Forest için hiperparametre optimizasyonu başlıyor...")
        rf_pipeline = build_pipeline(RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1), use_smote=True)
        best_model = optimize_hyperparameters(rf_pipeline, X_train, y_train)
    else:
        base_model, use_smote = model_candidates[best_model_name]
        best_model = build_pipeline(base_model, use_smote)
        best_model.fit(X_train, y_train)

    y_pred = best_model.predict(X_test)
    print("\nİyileştirilmiş model değerlendirme:")
    print(f"Doğruluk (Accuracy): {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))

    print("\nTahmin Sistemi Hazır!")
    """
    print("\n--- Hava Durumuna Göre Önerilen Şarkılar ---")
    unique_weathers = data['Weather'].unique()
    for weather in unique_weathers:
        print(f"\nHava Durumu: {weather}")
        recommend_songs(data, best_model, weather_input=weather, top_n=5) """


    while True:
        weather_input = input("\nHava durumu girin (Çıkmak için 'q'): ").strip()
        if weather_input.lower() == 'q':
            print("Çıkılıyor...")
            break
        recommend_songs(data, best_model, weather_input)

        

if __name__ == "__main__":
    main()

    
