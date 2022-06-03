# Zero-Player
제로 플레이어 게임

현재 구현된 시스템: 타일 기반 16x9 그리드 맵 표시, 마우스 클릭시 타일 변경, 키보드 위, 아래 화살표 눌러서 선 두께 변경

매인 파일: main.py 의 main 함수 (def main) 부분

게임 월드는 16 * 9 의 2 차원 int 배열이고, (0,0) 이 왼쪽 위, (15, 8) 이 오른쪽 아래

game.py 의 world 라는 배열의 내용이 수정되면, GPU는 해당하는 칸에 다른 텍스쳐를 띄움
world 라는 배열은 "지금당장 모니터에 띄울 타일의 번호" 임
game.py 의 tick 함수는 1초에 1번씩 호출되는 함수임. 그 함수에서 world 배열을 수정하는 것이 권장됨.

GPU 는 최대 32개의 텍스쳐를 저장할 수 있음, 다시 말해서, 타일의 종류가 32개를 넘어가면 안됨. 인덱스는 0번부터 시작하기 때문에, 0번째부터 31번째까지만 유요하고 32번째 텍스쳐는 유효하지 않음.
현재 등록된 텍스쳐는 0.png, 1.png, 2.png. 3.png, 4.png 이며, 0번째부터 4번째까지임. game.py 에서 texture_list 를 수정하는 것으로 더 추가할 수 있음.
world 배열의 요소중 32 이상의 값이 있으면 유효하지 않은 텍스쳐로 인식하고 프로그램이 중단됨.

마우스 클릭시 클릭한 칸에 해당하는 world 배열의 요소의 값에 1을 더함, 그리고 `world[x][y] = world[x][y] % 텍스쳐 갯수` 를 하여 유효하지 않은 텍스쳐를 표시하지 않도록 함.

# 입력 핸들링
inputhandler.py 는 키보드와 마우스 입력을 처리하는 파일, on_mouse 는 마우스 입력, on_key 는 키보드 입력을 처리함.