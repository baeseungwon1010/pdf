import fitz
import subprocess
import sys
import json
import os
from pathlib import Path

def get_dir_info(path_obj):
    """디렉토리 내 파일 목록과 권한을 확인하는 헬퍼 함수"""
    try:
        if not path_obj.exists():
            return "Does not exist"
        items = os.listdir(str(path_obj))
        return {
            "path": str(path_obj.resolve()),
            "writable": os.access(str(path_obj), os.W_OK),
            "files": items[:20]  # 너무 많을 수 있으니 20개까지만
        }
    except Exception as e:
        return f"Error: {str(e)}"

# 1. 경로 설정
pdf = Path(sys.argv[1]).resolve()
script_dir = Path(__file__).parent.resolve()
cwd = Path.cwd().resolve()

# 결과 저장용 폴더 생성 (bot.py와 같은 위치의 extracted 폴더)
out_dir = script_dir / "extracted" / pdf.stem
out_dir.mkdir(parents=True, exist_ok=True)

# 2. PDF 내 임베드 파일 이름 확인
try:
    doc = fitz.open(str(pdf))
    names = doc.embfile_names()
    doc.close()
except Exception as e:
    print(json.dumps({"error": f"PDF Open Error: {str(e)}"}))
    sys.exit(1)

# 3. 추출 및 덮어쓰기 시도
res = []
for i, n in enumerate(names):
    # 각 시도의 결과물 위치 (실제로 생성되는지 확인용)
    expected_out = out_dir / f"file_{i}"
    
    p = subprocess.run(
        [sys.executable, "-m", "pymupdf", "embed-extract",
         str(pdf), "-name", n],
        capture_output=True,
        text=True
    )
    
    res.append({
        "name": n,
        "ok": p.returncode == 0,
        "stdout": p.stdout.strip(),
        "stderr": p.stderr.strip()
    })

# 4. 서버 내부 구조 디버깅 정보 수집
debug_info = {
    "env": {
        "cwd": str(cwd),
        "script_dir": str(script_dir),
        "python_version": sys.version.split()[0]
    },
    "hierarchy": {
        "current_cwd": get_dir_info(cwd),
        "parent_1": get_dir_info(cwd / ".."),
        "parent_2": get_dir_info(cwd / "../.."),
        "root": get_dir_info(Path("/"))
    }
}

# 5. 최종 결과 출력 (JSON)
print(json.dumps({
    "debug": debug_info,
    "pdf_info": {
        "path": str(pdf),
        "count": len(names),
        "names": names
    },
    "results": res
}, ensure_ascii=False, indent=2))
