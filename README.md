# SmartNetworkService
2023-2학기 스마트 네트워크 서비스 기말 프로젝트

개발자 : 류건, 정성원

### Dependency

* PyQt5~=5.15.10
* PyQt5-Qt5==5.15.2
* PyQt5-sip==12.13.0

### File Descriptions

* PyQtServer: 채팅을 위한 서버 프로그램
* PyQtClient: 실제 채팅용 클라이언트 프로그램
######
* PyQtChatWithMemo: 클라이언트에 서버 기능도 이식한 단일 실행 프로그램

### 실행 방법 및 기능

- 유튜브 링크 : **https://youtu.be/Hv912kI_Weg/**

* 서버가 실행된 후 클라이언트 실행 시, 클라이언트에서 소켓 통신을 통해 서버에 연결, 다른 클라이언트와 채팅이 가능해진다.
* 각 클라이언트에는 채팅 중 사용할 수 있는 메모장 기능이 있으며, 작성한 내용은 프로그램 종료 전까지 저장된다.
