**※ 모든 파일은 /home/pi 가 기본(Default)경로 입니다.**

/* 

**· 라즈베리파이 최신 버전 업데이트**

**sudo apt-get update**

**sudo apt-get upgrade** 

**· 라즈베리파이 호스팅 네임 변경**

https://snowdeer.github.io/raspberry/2017/07/24/change-host-name-of-raspberry/

**sudo nano /etc/hostname**

raspberry <-> Auto-Diffuser 으로 변경

**sudo nano /etc/hosts**

raspberry <-> Auto-Diffuser 으로 변경


**· 라즈베리파이 수동 종료(케이스 button) state : off 변경**

**sudo nano /usr/bin/argononed.py**

def shutdown_check():

	while True:
	
		pulsetime = 1
		
		GPIO.wait_for_edge(shutdown_pin, GPIO.RISING)
		
		time.sleep(0.01)
		
		while GPIO.input(shutdown_pin) == GPIO.HIGH:
		
			time.sleep(0.01)
			
			pulsetime += 1
			
		if pulsetime >=2 and pulsetime <=3:
		
			**os.system("sudo python3 /home/pi/poweroff.py")** <-- 이 부분 추가
			
			**time.sleep(1)** <-- 이 부분 추가
			
			os.system("reboot")
			
		elif pulsetime >=4 and pulsetime <=5:
		
			**os.system("sudo python3 /home/pi/poweroff.py")** <-- 이 부분 추가
			
			**time.sleep(1)** <-- 이 부분 추가
			
			os.system("shutdown now -h")

*/

· 진행상황 유튜브 재생목록 : https://youtube.com/playlist?list=PLQcbrPqBPDWBvnNA4iCAFQh5WGHrUEXCE

· <참고한 사이트> ─────────────────────────────────────────────────────────────────────────────────────────

· 1. bluetooth 라이브러리 설치 : https://snowdeer.github.io/raspberry/2017/07/24/bluetooth-library-install-on-raspberry/

**sudo apt-get install python-dev** // 파이썬 코드 실행 라이브러리

**sudo apt-get install build-essential libbluetooth-dev** //블루투스 라이브러리

**sudo apt-get install bluetooth blueman bluez** //블루투스 라이브러리

**sudo pip3 install pybluez** //블루투스 라이브러리

**sudo pip3 install python-firebase** //파이어베이스 라이브러리

**sudo pip3 install firebase-admin** //파이어베이스 라이브러리

**sudo pip3 install requests** //파이어베이스 라이브러리

**sudo pip install bs4** // 크롤링 라이브러리

**sudo pip install html5lib** // 크롤링 라이브러리

※ 1-1. 파일 설정 https://landwhale2.github.io/iot/171/

**Terminal : nano /home/pi/.bashrc** -> 맨 아래에 있는 "fi" 밑에 코드 작성 : **sudo chmod 777 /var/run/sdp**

**Terminal : sudo nano /etc/systemd/system/dbus-org.bluez.service**

'ExecStart ='줄 끝에 호환성 플래그 '-C'를 추가합니다. 그 뒤에 새 줄을 추가하여 SP 프로필을 추가

**ExecStart=/usr/lib/bluetooth/bluetoothd -C**

**ExecStartPost=/usr/bin/sdptool add SP**

─────────────────────────────────────────────────────────────────────────────────────────

· 2. rc.local 파일 수정 (자동 실행) : https://blog.naver.com/emperonics/221770579539

현재 디렉토리에 존재하는 파일 권한 부여하기 (sh파일에만)

**chmod 755 ./blueon.sh**

**chmod 755 ./blueoff.sh**

※ 2-1. 예외 (auto_pair.py) : https://kingmuraa.tistory.com/2

**Terminal : sudo nano /etc/profile**

· 맨 밑의 fi 아래에 자동 실행할 파일 경로 추가

**(sleep 15 && /usr/bin/python3 /home/pi/auto_pair.py) &** // sleep을 넣지 않고, 실행시 자동실행이 되지 않아 꼭 넣어야 함
─────────────────────────────────────────────────────────────────────────────────────────

· 3. Auto_pair.py 코드 : https://stackoverflow.com/questions/66401660/how-can-i-automate-pairing-rpi-and-android-with-bluetooth-batch-script/66403748#66403748

─────────────────────────────────────────────────────────────────────────────────────────
