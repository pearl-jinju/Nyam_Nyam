#함수로 작성할것
def recommand(latitude,longitude,radius_around,user_preference):
    import pandas as pd
    import pickle
    from sklearn.feature_extraction.text import CountVectorizer
    # from tensorflow.keras.preprocessing.text import Tokenizer    

    # 데이터 불러오기
    base_path = "data/"
    # 위도 경도 추출 및 기본 데이터 제공용도
    # Load data
    with open(base_path + 'data.pkl', 'rb') as fr:
        data = pickle.load(fr)

    data_df = pd.DataFrame(data)
    data_df = data_df.fillna('없음')

    # 위치 정보
    # 현재 위치 가져오기
    location = [str(latitude), str(longitude)]
    # 현재 위치 기준으로 몇미터 까지
    distance = radius_around

    # 1차 거리 기준 필터링
    from haversine import haversine
    data_df = data_df[data_df['latitude'] < 38.5] # 위도 38.5 이상은 외국

    # 위도, 경도 리스트 생성
    data_df['place'] = data_df['latitude'].astype(str) + "@" + data_df['longitude'].astype(str)
    data_df['place'] = data_df['place'].str.split("@")

    def func(x):
        """caculate distance"""
        store_wui, store_gyeong = float(x[0]), float(x[1])
        now_wui, now_gyeong = float(location[0]), float(location[1])
        store_place = (store_wui, store_gyeong)
        now_place = (now_wui, now_gyeong)
        return haversine(store_place, now_place, unit='m')

    # 입력받은 현재위치를 기준으로 식당 위치 추출
    data_df['distance'] = data_df['place'].apply(lambda x: func(x))
    data_df = data_df.sort_values("distance")
    nearest_store = data_df[data_df['distance'] < distance]

    # 평점 기준 추출
    nearest_rating_store = nearest_store[nearest_store['rating'] > 0].reset_index(drop=True)

    # CBF시작
    # Load vocabulary
    # with open(base_path + 'tokenizer-tf-90109.pkl', 'rb') as fr:
    #         tokenizer = pickle.load(fr)

    # 유저벡터 반영
    user_token = pd.DataFrame(data = {'top10_keywords': [user_preference]})
    restaurant_token = pd.DataFrame(nearest_rating_store['top10_keywords'])
    user_like_matrix = pd.concat([restaurant_token, user_token])

    # 검색결과 미달
    if len(user_like_matrix) <= 19:
        result_matrix = "주변에 추천할만한 맛집이 없어요 ㅠㅠ"
        return result_matrix

    # CountVectorizer로 벡터화 후 유사도 분석
    # tensorflow tokenizer
    # sequences = tokenizer.texts_to_matrix(user_like_matrix['top10_keywords'])

    # sklearn Countvectorizer
    count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
    keywords_string = user_like_matrix['top10_keywords'].apply(lambda x: " ".join(x))
    vectorized_matrix = count_vect.fit_transform(keywords_string)

    # 코사인 유사도 계산
    from sklearn.metrics.pairwise import cosine_similarity
    user_sim = cosine_similarity(vectorized_matrix, vectorized_matrix)

    #  20개만 가져오기(?)
    user_sim_sim_sorted_ind = user_sim.argsort()[:, ::-1]  # ::-1 : 역순으로 정렬

    if len(user_sim_sim_sorted_ind) <= 19:
        result_matrix = "주변에 추천할만한 맛집이 없어요 ㅠㅠ"
        return result_matrix

    similar_indexes = user_sim_sim_sorted_ind[-1, :20]
    similar_indexes = similar_indexes[1:21]

    # html에서 키워드 리스트를 str로 인식하도록 설계되었기 때문에 키워드 컬럼 타입을 str로 변경한다.
    check_df = nearest_rating_store[['restaurant_id', 'name', 'road_address', 'phone_number', 'rating',  'img_url', 'place', 'distance', 'top10_keywords']]
    result_matrix = check_df.iloc[similar_indexes].values.tolist()

    return result_matrix
