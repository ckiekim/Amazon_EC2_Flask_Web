## Web for DataAnalysis & AI Application
- http://168.138.102.210:5000

### Application
- 지역 분석, 카토그램, 크롤링, 워드클라우드
- 추천 시스템: 책, 영화
- 머신러닝: 분류, 회귀, PCA, 군집화
- 딥러닝: 이미지 분류, 이미지 검출
- 자연어 처리: 영화평 감성분석, 번역
- 게시판

### Software Version
- Anaconda3-2021.05 with python 3.8.8
- Flask 1.1.2
- Surprise 1.1.1
- Folium 0.12.1.post1
- MySQL 8.0.21
- Bootstrap 4.6
- jQuery 3.6, jQuery-ui 1.12.1

### Hardware System
- Oracle Cloud VM instance, Centos 8

### API 접속 Key 
- Weather API key (https://openweathermap.org/api)
- Kakao 인공지능 REST API key (https://developers.kakao.com/)
- 공공 인공지능 오픈 API key (https://aiopen.etri.re.kr/)

## 설치 방법
#### Anaconda 설치 ('21.09.08, Python 3.8.8)
<pre>
$ curl -O https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
$ sudo bash Anaconda3-2021.05-Linux-x86_64.sh
</pre>

#### Flask, Surprise, Folium, wordcloud 설치
<pre>
$ sudo pip install Flask
$ sudo pip install scikit-surprise
$ sudo pip install folium
$ sudo pip install wordcloud
</pre>

#### 한글 폰트 설치
<pre>
$ wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
$ unzip NanumFont_TTF_ALL.zip -d NanumFont
$ sudo mv NanumFont /usr/share/fonts
$ sudo fc-cache -fv
</pre>

#### Chrome driver and Selenium 설치
#### 1) Install Chrome
<pre>
$ vi /etc/yum.repos.d/google-chrome.repo
</pre>
<pre>
#Make sure you have below info in the file(remove hash).
#[google-chrome]
#name=google-chrome
#baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
#enabled=1
#gpgcheck=1
#gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
</pre>

#### 2) Install ChromeDriver
<pre>
$ wget -N https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip -P ~/
$ unzip ~/chromedriver_linux64.zip -d ~/
$ rm ~/chromedriver_linux64.zip
$ sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
$ sudo chown root:root /usr/local/bin/chromedriver
$ sudo chmod 0755 /usr/local/bin/chromedriver
</pre>

#### 3) Selenium 설치
<pre>
$ sudo pip install selenium
</pre>

#### Konlpy 설치
<pre>
$ sudo yum install java-11-openjdk-headless
$ sudo vi /etc/profile.d/java.sh
</pre>
<pre>
JAVA_HOME="/usr/lib/jvm/java-11-openjdk-11.0.12.0.7-0.el8_4.x86_64"
</pre>
<pre>
$ sudo pip install konlpy
</pre>

#### Tensorflow 설치
<pre>
$ sudo pip install tensorflow
</pre>
