# dansofestival
단소고 페스티벌 농구 슛 모션 분석 프로그램 - https://kwonkai.tistory.com/141  
https://developers.google.com/mediapipe/solutions/vision/pose_landmarker  
https://blog.naver.com/oliven2/220999105393 슛폼 정석  
https://blog.naver.com/oliven2/221066556948 슛폼 정석  
슛 날리는 방법 https://ko.wikihow.com/%EB%86%8D%EA%B5%AC-%EC%8A%9B-%EB%82%A0%EB%A6%AC%EB%8A%94-%EB%B0%A9%EB%B2%95  

<hr>

# Basketball Shoot Posture Help Program

### 프로그램 제작 이유
학교시간에 접해본 미디어파이프를 통해 미디어파이프에 있는 기능 중 자세 추정,동작 인식 등에 관심이 생겨 우리 주변에 접목해볼 사례를 생각하던 도중 학교에서 흔히 보는 농구하는 모습을 보고 슛을 쏠때 벌어지는 팔의 각도 움직이는 손가락 등 움직이는 자세를 통해 영상처리와 기술스택를 통해 분석하고 더 나아가 영상처리가 주요하게 접목되어 있는 자율 주행 자동차,CCTV 등 영상처리에 대해 한 층 더 알아보고자 조사하게 됨.

### 프로그램 로직 설명
포즈 랜드마크 모델에 들어가있는 점을 통해 어깨,팔,손바닥를 이용하여 6개의 점으로 팔꿈치 안의 각도와 손목,손바닥의 각도를 통해서 힘과 방향을 측정해서 기준이 되는 모션에 일치하는 만큼 점수가 추가된다.

### 핵심 알고리즘
이 프로그램에서 손과 팔을 영상 처리하여 어쩌구 저쩌구

### 프로그램의 장점
정확한 슛자세를 교정할수 있다

### 사용 방법
학번과 이름을 적는다 -> 왼손인지 오른손인지 정한다 -> 농구 골대쪽으로 몸을 겨냥하고 손이 카메라에 나오도록 한다 -> 슛을 쏜다
