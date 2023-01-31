import os 
os.getcwd()
import re
import pandas as pd
import numpy as np
from tqdm import tqdm
from konlpy.tag import Okt

# from pykospacing import Spacing
from collections import Counter, defaultdict
import os


from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

import warnings
warnings.filterwarnings('ignore')

#  내가 직접 지정한 불용어 리스트 작성
custom_stopwords = [
    "범죄도시", "범죄 도시", "범죄", "도시", "죽지",
    "늑대사냥", "늑대", "사냥",
    "공조", "인터네셔날","인터내셔날",
    "한산", "용", "용의", "출현", "용의출현", "장군님", "장군",
    "뜨거운피", "피", "뜨거운",
    "외계인", "외계", "인",
    "영화", "무비", "영화관", "한국영화",
    "진짜", "진자", "완전", "존나", "졸라", "느낌", "뭔가", "제일", "개", "보고", "사람", "보지",
    "어요", "오늘", "그냥", "생각", "면서", "더니", "인적", "거지", "보기", "나름", "살짝",
    "정말", "대박", "역대", "최고", "어제", "편이", "계속", "요소", "처럼", "이나", "역시", "부분", "던데",
    "스포", "개봉", "한번", "내내", "구나", "때문", "어서", "정도", "다가", "다시", "누가", "덕분", "항상",
    "봤는데", "왔는데", 
    "이라니", "어도"
    "스포일러가 포함된 감상평입니다."
]

#  ckonlpy에 추가할 단어 지정
custom_noun = [

    #  [ 범죄도시 ]
    "장이수", "강해상", "손석구", "마석도", "마동석", "마블리", "박지환", "윤계상",
    "2부", "2탄", "2편", "1부", "1탄", "1편",
    #  * 같은 단어 : 장이수=이수, 마석도=마동석=마블리
    #  * 불용어 처리하면 안되는 단어 :
    #  - 구씨 : 배우 손석구가 다른 작품에서 맡았던 케릭터 이름

    #  [ 늑대사냥 ]
    "서인국", "장동윤", "박호산", "정소민", "고창석", "성동일",
    "콘에어", "콘 에어", "잔인",
    #  * 같은 단어 : 콘에어=콘 에어
    #  * 불용어 처리하면 안되는 단어 :
    #  - 콘에어 : 니콜라스 케이지 출연 1997년 영화. 늑대사냥과 비슷한 소재를 다루고있음.

    #  [ 공조2 ]
    "현빈", "유해진", "윤아", "다니엘 헤니", "다니엘헤니", "다니엘", "헤니", "진선규",
    "장영남", "박훈", "임성재", "림청렬", "청렬", "강진태", "진태", "장명준", "박소연",
    "박상위", "박민영",
        "불시착", "사랑의 불시착",
    # 같은 단어 : 다니엘헤니=다니엘=헤니, 불시착=사랑의 불시착

    #  [ 외계인1부 ]
    "류준열", "김우빈", "김태리", "소지섭", "염정아", "조우진", "이하늬",
    "무륵", "김현중", "이안", "문도석", "흑설", "청운",
    "2부", "2탄", "2편", "1부", "1탄", "1편", "돈", "SF", "sf", "SF물", "sf물",
    #  * 불용어 처리하면 안되는 단어 :
    #  - 돈 : 한 글자 '돈 아깝다'같은 말이 종종 보임.
    #  - SF, sf : 장르명. 한글이 아니라고해서 없애면 안됨.

    #  [ 한산 ]
    "박해일", "안성기", "변요한", "손현주", "김성규", "김성균", "김향기", "택연", "옥택연",
    "이순신", "장군님", "장군", "어영담", "원균", "준산", "히데요시", "도요토미", "도요토미 히데요시",
    "한산도", "대첩", "한산도 대첩", "임진왜란", "유키나가", "학익진",
    #  * 같은 단어 : 이순신=이순신장군
    #  * 불용어 처리하면 안되는 단어 :
    #  - 하라 : '전군 출정하라', '선회하라', '발포하라'가 이 영화의 명대사인가봄.

    # 뜨거운피 배우명/등장인물명
    "정우", "김갑수", "최무성", "지승현", "김해곤", "윤지혜", "이홍내", "정호빈"
    #  * 불용어 처리하면 안되는 단어 :
    #  - 짱구 : 배우 정우가 다른 작품에서 맡았던 케릭터 이름
    
    #

]

class idk():
    def __init__(self):
        None
    def extract_word(text):
        hangul_eng_num = re.compile('[^가-힣a-zA-Z0-9]') 
        result = hangul_eng_num.sub(' ', str(text)) 
        return result



    from hanspell import spell_checker

    def sth(SEARCH, spellcheck=False):

        # 불용어
        with open('./utils/한국어불용어_new.txt', 'r', encoding = 'utf-8') as f:
            stop_words = f.read()
        f.close()
        
        documents_noun =[]
        documents_morph = []
        
        stop_words = stop_words.split(',')
        stop_words.extend(custom_stopwords)

        # 사용자 지정 단어 사전 추가
        from ckonlpy.tag import Twitter
        custom_okt = Twitter()
        for noun in custom_noun:
            custom_okt.add_dictionary(noun, 'Noun')

        # df = pd.read_csv(f'./naver_review/review_{SEARCH}_naver_20-10-2022.csv')
        df = pd.read_csv(f'./data/{SEARCH}_네이버평점 크롤링.csv')
        # 결측치 : 10정도 소수 : 삭제
        df = df.dropna().reset_index(drop=True)
        
        # 한글만 + 영어, 숫자
        df['review'] = df['comment'].apply(lambda x: extract_word(x))
        
        # 스펠 교정
        if spellcheck ==True :
            from hanspell import spell_checker
            for idx,review in tqdm(enumerate(df['review'])):
                review = spell_checker.check(review).checked
                df.iloc[idx,1] = review
            
        #  불용어 제거, 한글자 단어 제거 / noun
        for review in df['review']:
            document = ""
            words = custom_okt.nouns(review)
            for word in words : 
                if(len(word) >= 2 ) or (word in custom_noun):
                    if word not in stop_words:
                        document += word + " "
            document = document.rstrip()              # rstrip([chars]) : 인자로 전달된 문자를 String의 오른쪽에서 제거
            documents_noun.append(document)
            
        #morphs로
        from konlpy.tag import Okt
        okt = Okt()
        for review in df['review']:
            document = ""
            words = okt.morphs(review, stem = True)
            for word in words:
                if (len(word) >= 2 ):
                    if word not in stop_words:
                        document += word + " "
            document = document.rstrip()
            documents_morph.append(document)
        
        
        df['result_noun'] = documents_noun
        df['result_morph'] = documents_morph

        print(df.head())
        
        row_review = df.loc[(df['score'] <=5) ]
        mid_review = df.loc[(df['score'] >5) | (df['score'] <8) ]
        high_review = df.loc[(df['score'] >= 8)]

        
        #noun 으로 토큰화된것
        row_keyword_noun = tfidf(row_review['result_noun'])
        mid_keyword_noun = tfidf(mid_review['result_noun'])
        high_keyword_noun = tfidf(high_review['result_noun'])
        
        #morph 으로 토큰화된것
        row_keyword_morph = tfidf(row_review['result_morph'])
        mid_keyword_morph = tfidf(mid_review['result_morph'])
        high_keyword_morph = tfidf(high_review['result_morph'])
        
        
        print('noun', '\n', tfidf(documents_noun))
        print('morphs', '\n', tfidf(documents_morph))
        
        
        print('row', row_keyword_morph)
        print('mid', mid_keyword_morph)
        print('high', high_keyword_morph)

        return None


    from ckonlpy.tag import Twitter
    custom_okt = Twitter()

    for n in custom_noun:
        custom_okt.add_dictionary(n,'Noun')

    #  TF-IDF 방식으로 키워드를 추출하는 모듈
    def tfidf(documents) :

        print("TF-IDF 기반 키워드 추출 시작")

        import pandas as pd
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer 

        #  문서군의 TF-IDF 행렬 생성
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_mat = tfidf_vectorizer.fit_transform(documents)
        #np.asarray
        tfidf_mat = pd.DataFrame(np.asarray(tfidf_mat), columns = tfidf_vectorizer.get_feature_names_out())

        #  각 문서별로 TF-IDF 값이 가장 높은 단어만 선별
        max_mat = pd.DataFrame(columns=["word", "tfidf"])
        max_mat["tfidf"] = tfidf_mat.max(axis="columns")
        max_mat["word"] = tfidf_mat.idxmax(axis="columns")

        #  각 단어들에 대한 TF-IDF값들 통계
        #  word : 단어
        #  freq_count : 해당 단어의 TF-IDF값이 가장 높게 나온 문서 개수
        #  tfidf_mean, tfidf_std : 해당 단어의 TF-IDF값들 평균, 표준편차
        statistic_mat = pd.DataFrame(
            columns=["word", "freq_count", "tfidf_mean", "tfidf_std"])

        th = 0.6  # TF-IDF값이 0.6 이상인 단어만 저장
        statistic_mat["word"] = list(
            max_mat[max_mat["tfidf"]>th].groupby("word")["word"].count().index)

        statistic_mat["freq_count"] = list(
            max_mat[max_mat["tfidf"]>th].groupby("word")["word"].count())

        statistic_mat["tfidf_mean"] = list(
            max_mat[max_mat["tfidf"]>th].groupby("word")["tfidf"].mean())

        statistic_mat["tfidf_std"] = list(
            max_mat[max_mat["tfidf"]>th].groupby("word")["tfidf"].std())

        statistic_mat.sort_values(by="freq_count", ascending=False, inplace=True)
        statistic_mat = statistic_mat.head(20)  # 빈도수 상위 100개만 저장
        statistic_mat.reset_index(drop=True, inplace=True)
        statistic_mat = statistic_mat.round(2)
        # ? round : round(statistic_mat, 2)

    #     if filename != "" :
    #         statistic_mat.to_csv("{}.csv".format(filename),index=False ,sep=",", encoding="utf-8")
    #         print("TF-IDF 기반 키워드 csv 파일 저장 완료")

        #print("TF-IDF 기반 키워드 추출 완료\n")
        return statistic_mat

