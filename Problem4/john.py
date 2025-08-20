import subprocess, tempfile, os, shlex

JOHN = "/opt/homebrew/Cellar/john-jumbo/1.9.0_1/bin/john"   # john 절대경로
MASK = "[a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9]"

def crack_zip(hash_str, mask=MASK):
    # 1) 임시 해시 파일
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(hash_str + "\n")
        hash_file = f.name

    # 2) 임시 pot 파일
    pot_file = tempfile.mktemp()

    # 3) john 실행  (옵션 --potfile-path → --pot 로 교체)
    cmd = [
        JOHN, "--format=pkzip",
        f"--mask={mask}",
        hash_file,
        "--verbosity=1",
        f"--pot={pot_file}"
    ]
    print(" ".join(shlex.quote(c) for c in cmd))
    subprocess.run(cmd, check=True)

    # 4) pot 파일에서 패스워드 추출
    with open(pot_file) as pf:
        pwd = pf.readline().strip().split(":", 1)[1]

    # 5) 임시파일 정리
    os.remove(hash_file)
    os.remove(pot_file)
    return pwd

hash_str = "$pkzip2$1*1*2*0*19*b*cbc0a921*0*2a*8*19*cbc0*8a4a*d61516376fd82fddcd82a86b90a3a416205d20d7a1c02c18f6*$/pkzip2$"
password = crack_zip(hash_str)
print("Found password →", password)
