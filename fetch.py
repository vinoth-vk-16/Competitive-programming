import os
import requests
import argparse
from typing import List, Dict
import html2text

GRAPHQL_URL = "https://leetcode.com/graphql"

# Hardcoded LeetCode session cookie - REPLACE THIS WITH YOUR ACTUAL COOKIE
LEETCODE_SESSION_COOKIE = ""

EXT_MAP = {
    "python": "py", "python3": "py", "cpp": "cpp", "java": "java", "c": "c",
    "csharp": "cs", "javascript": "js", "typescript": "ts", "kotlin": "kt",
    "swift": "swift", "golang": "go", "ruby": "rb", "scala": "scala",
    "rust": "rs", "mysql": "sql", "bash": "sh", "racket": "rkt", "erlang": "erl",
    "elixir": "ex", "dart": "dart", "php": "php", "perl": "pl", "haskell": "hs"
}

VALID_LANGUAGES = list(EXT_MAP.keys())

def graphql_request(query: str, variables: dict, session_token: str) -> dict:
    r = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={
            "Content-Type": "application/json",
            "Cookie": f"LEETCODE_SESSION={session_token};",
            "Referer": "https://leetcode.com/problemset/all/"
        }
    )
    if not r.ok:
        print("GraphQL error:", r.text)
        r.raise_for_status()
    return r.json()

def get_all_submissions(session_token: str, max_submissions: int = 50) -> List[Dict]:
    """Fetch submissions with a limit on total number"""
    subs = []
    offset = 0
    limit = 20

    while len(subs) < max_submissions:
        data = graphql_request(
            """
            query subs($offset: Int!, $limit: Int!) {
              submissionList(offset: $offset, limit: $limit) {
                submissions {
                  id titleSlug lang statusDisplay timestamp
                }
                hasNext
              }
            }
            """,
            {"offset": offset, "limit": limit},
            session_token
        )
        s = data["data"]["submissionList"]
        subs.extend(s["submissions"])
        
        # Stop if we've reached the limit or no more submissions
        if len(subs) >= max_submissions or not s["hasNext"]:
            break
        offset += limit
    
    # Return only the requested number of submissions
    return subs[:max_submissions]

def get_submission_code(submission_id: int, session_token: str) -> str:
    data = graphql_request(
        """
        query details($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
          }
        }
        """,
        {"submissionId": submission_id},
        session_token
    )
    return data["data"]["submissionDetails"]["code"]

def html_to_md(html: str) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.body_width = 0
    return h.handle(html)

def get_problem_data(slug, session_token):
    q = """
    query q($slug: String!) {
      question(titleSlug: $slug) {
        title content difficulty codeSnippets { lang code }
      }
    }"""
    return graphql_request(q, {"slug": slug}, session_token)["data"]["question"]

def save_problem(slug: str, problem_data: dict, submissions: List[dict], base_dir: str, session_token: str, languages: List[str]):
    title = problem_data["title"]
    problem_dir = os.path.join(base_dir, slug)
    os.makedirs(os.path.join(problem_dir, "submissions"), exist_ok=True)

    with open(os.path.join(problem_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{html_to_md(problem_data.get('content',''))}\n")
       

    for snippet in problem_data.get("codeSnippets", []):
        if snippet["lang"].lower() in languages:
            p = os.path.join(problem_dir, f"solutiontemplate.{EXT_MAP.get(snippet['lang'].lower(), snippet['lang'].lower())}")
            with open(p, "w", encoding="utf-8") as f:
                f.write(snippet["code"])
            break

    for sub in submissions:
        lang = sub["lang"].lower()
        if lang not in languages:
            continue
        ext = EXT_MAP.get(lang, lang)
        lang_dir = os.path.join(problem_dir, "submissions", lang)
        os.makedirs(lang_dir, exist_ok=True)

        code = get_submission_code(int(sub["id"]), session_token)
        timestamp = sub["timestamp"]
        status = sub["statusDisplay"].replace(" ", "_")
        filename = f"{timestamp}_{status}.{ext}"
        path = os.path.join(lang_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

def write_root_readme(output: str, summary: List[Dict], languages: List[str]):
    summary_path = os.path.join(output, "README.md")
    total = len(summary)
    count = {"Easy": 0, "Medium": 0, "Hard": 0}
    for item in summary:
        count[item["difficulty"]] += 1

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("""leetcode
========
""")
        f.write(f"#### Total solved: {total} (Easy: {count['Easy']} Medium: {count['Medium']} Hard: {count['Hard']})\n")
        f.write("My solutions of [leetcode](https://leetcode.com/problemset/all/)\n\n")
        f.write(f"Languages: {', '.join(languages)}\n\n")
        f.write("| No | Title | Source Code | Difficulty |\n")
        f.write("|----|-------|-------------|------------|\n")
        for i, item in enumerate(sorted(summary, key=lambda x: x["title"])):
            slug = item["slug"]
            title = item["title"]
            diff = item["difficulty"]
            url = f"./{slug}"
            f.write(f"| {i+1} | {title} | [Link]({url}) | {diff} |\n")
        

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="leetcode")
    p.add_argument("--sync", action="store_true")
    p.add_argument("--limit", type=int, default=50,
                   help="Maximum number of submissions to fetch (default: 50)")
    p.add_argument("--only-accepted", action=argparse.BooleanOptionalAction, default=True,
                   help="Only include accepted submissions (default: True)")
    p.add_argument("--languages", nargs="+", default=["python3"], choices=VALID_LANGUAGES,
                   help="Languages to include (default: python3). Use lowercase names like 'cpp', 'python3'.")
    p.add_argument("--all-languages", action="store_true",
                   help="Include all available LeetCode languages")
    args = p.parse_args()

    languages = VALID_LANGUAGES if args.all_languages else args.languages

    # Use hardcoded cookie instead of browser extraction
    token = LEETCODE_SESSION_COOKIE
    
    if token == "your_leetcode_session_cookie_here":
        print("❌ ERROR: Please update LEETCODE_SESSION_COOKIE with your actual cookie value!")
        print("\nTo get your cookie:")
        print("1. Open LeetCode in Chrome and log in")
        print("2. Press F12 → Application → Cookies → https://leetcode.com")
        print("3. Copy the value of 'LEETCODE_SESSION'")
        print("4. Replace 'your_leetcode_session_cookie_here' in the code")
        return
    
    print(f"Fetching last {args.limit} submissions...")
    all_subs = get_all_submissions(token, max_submissions=args.limit)
    print(f"✓ Retrieved {len(all_subs)} submissions")
    
    by_slug = {}

    for s in all_subs:
        if args.only_accepted and s["statusDisplay"] != "Accepted":
            continue
        by_slug.setdefault(s["titleSlug"], []).append(s)

    slugs = list(by_slug.keys())
    if args.sync and os.path.exists(args.output):
        existing = set(os.listdir(args.output))
        slugs = [s for s in slugs if s not in existing]
    print(f"Processing {len(slugs)} problems…")

    total_submissions_written = 0
    total_problems = len(slugs)
    summary = []

    for slug in slugs:
        try:
            pd = get_problem_data(slug, token)
            subs = by_slug[slug]
            save_problem(slug, pd, subs, args.output, token, languages)
            total_submissions_written += len([s for s in subs if s["lang"].lower() in languages])
            summary.append({"slug": slug, "title": pd["title"], "difficulty": pd["difficulty"]})
        except Exception as e:
            print(f"❌ {slug}: {e}")

    write_root_readme(args.output, summary, languages)

    print(f"\n✅ Finished. {total_problems} problems saved.")
    print(f"📝 Total submissions downloaded: {total_submissions_written}")

if __name__ == "__main__":
    main()
