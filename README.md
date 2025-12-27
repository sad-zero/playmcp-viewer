# 🎮 PlayMCP Viewer

> 카카오 PlayMCP에 등록된 MCP 서버들을 탐험하고 발견하는 여행의 시작! 🚀  
> 수많은 서버들 속에서 당신만의 보물을 찾아보세요 ✨

카카오 PlayMCP에 등록된 MCP 서버들을 쉽고 재미있게 탐색할 수 있는 뷰어입니다. 다양한 검색 기준으로 서버를 찾고, 바로 접근할 수 있는 링크를 제공합니다.

---

## ✨ 주요 기능
> [tool](src/playmcp_viewer/inbound/tool.py) 을 참고하세요!

### find_mcp_servers
- [x] 🔍 **스마트 검색 & 필터링**: 다양한 기준으로 MCP 서버를 찾아보세요. 원하는 서버를 금방 찾을 수 있어요!
- [x]🔗 **원클릭 접근**: 등록된 MCP 서버로 바로 이동합니다. 클릭 한 번이면 끝!
- [x] 📊 **깔끔한 정리**: 서버들을 보기 좋게 정리해서 보여줍니다. 눈이 편안해집니다 👀
- [x] 🎯 **실시간 정보**: 최신 서버 정보를 실시간으로 확인할 수 있습니다. 놓치지 마세요!

---

## 🛠️ 기술 스택

이 프로젝트는 아래의 최신 기술과 라이브러리로 구성되어 있습니다:

- **FastMCP** ⚡: MCP 서버 애플리케이션을 위한 현대적 프레임워크 (`fastmcp`)
- **Pydantic** 🛡️: 강력한 데이터 검증과 데이터 모델링 (`pydantic`)
- **Pydantic Settings** 🔧: 환경설정 및 비밀 값 관리를 위한 통합 설정 툴 (`pydantic-settings`)
- **Dependency Injector** 🚰: 의존성 주입 지원 (`dependency-injector`)
- **httpx** 🌐: 빠르고 현대적인 비동기 HTTP 클라이언트
- **python-dotenv** 🗂️: `.env` 파일에서 환경 변수 손쉽게 로드
- **PyYAML** 📝: YAML 파일 파싱 및 직렬화
- **python-json-logger** 📋: JSON 형태의 구조화된 로깅
- **Python 3.12** 🐍: 최신 Python 버전 지원

개발 및 테스트 도구(예: `pytest`, `pytest-cov` 등)는 별도의 dev dependency 그룹에 포함되어 있습니다.

전체 의존성 목록은 `pyproject.toml`에서 확인 가능합니다.

---

## 📋 필요 사항

시작하기 전에 준비해야 할 것들:

- **Python 3.12** 🐍: 최신 버전이 필요해요
- **[uv](https://github.com/astral-sh/uv)** 📦: 빠르고 현대적인 패키지 매니저

> 💡 **팁**: uv가 없다면? 걱정 마세요! 설치 방법은 [여기](https://github.com/astral-sh/uv)를 참고하세요.

---

## 🚀 시작하기

### 로컬 개발 환경

로컬에서 개발하고 싶다면? 간단합니다!

1. **의존성 설치하기**:
   ```bash
   uv sync
   ```
   > ⏳ 잠시만요... 패키지들을 가져오고 있어요!

2. **서버 실행하기**:
- 환경 파일 준비하기  
실행 환경에 맞는 `{ENVIRONMENT}.env` 파일이 필요합니다. (기본값: `.env`)  
예시:
   ```env
   KAKAO_PLAYMCP_ENDPOINT=https://playmcp.kakao.com
   TOOL_CALL_LIMIT_PER_SECOND=1
   ```

- 서버 시작하기  
   ```bash
   uv run fastmcp run
   ```
   > 🎉 서버가 성공적으로 실행되었습니다!

---

### 🐳 Docker로 실행하기

- 이미지 빌드  
  ```bash
  docker image build -t {image}:{tag} --build-arg ENVIRONMENT={local|dev|prod} .
  ```
  `{ENVIRONMENT}`는 사용할 환경(`local`, `dev`, `prod` 등)에 맞게 지정하세요.


---

## 🧪 테스트

코드가 제대로 작동하는지 확인해볼까요?

```bash
# 모든 테스트 실행
uv run pytest

# 커버리지 포함 테스트
uv run pytest --cov
```

> 💪 테스트는 건강한 코드의 비결이에요!

---

## 📝 라이선스

이 프로젝트는 [MIT License](LICENSE)로 배포됩니다.  
자유롭게 사용하고 수정할 수 있어요! 🎉

---

## 🤝 기여하기

버그를 발견했거나 아이디어가 있으신가요?  
이슈를 등록하거나 풀 리퀘스트를 보내주세요! 환영합니다! 🎊

---

<div align="center">

**Made with ❤️ and ☕ by the PlayMCP Viewer Team**

⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요! ⭐

</div>
