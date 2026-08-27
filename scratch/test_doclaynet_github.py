import urllib.request

def check_github():
    url = "https://raw.githubusercontent.com/DS4SD/DocLayNet/main/README.md"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8')
            print("GitHub DocLayNet README retrieved successfully!")
            print("Length:", len(content))
            return True
    except Exception as e:
        print("GitHub check failed:", e)
        return False

if __name__ == "__main__":
    check_github()
