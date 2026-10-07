from src.specialists.developer.v2.developer_engine import DeveloperEngineV2

TASK = """
Create Phase 1 of AURA YouTube Studio Research Engine.

Requirements:

1. Create a modular src/youtube package.
2. Create a YouTube research engine for children's educational content.
3. Accept a research topic/query.
4. Prepare a structured research report.
5. Support YouTube search integration through an API-ready interface.
6. Do not scrape or bypass YouTube protections.
7. Collect, when officially available:
   - video title
   - channel name
   - published date
   - duration
   - view count
   - video URL
8. Identify recurring educational topics and research signals.
9. Score topics using transparent criteria such as:
   - relevance
   - educational value
   - freshness
   - competition
   - originality opportunity
10. Never copy another creator's script, video, thumbnail, characters,
    music or other copyrighted content.
11. Suggest original content angles only.
12. Store research results locally in a structured database.
13. Generate a machine-readable research report.
14. Include configuration support for API credentials through environment
    variables. Never hard-code API keys.
15. Include functional tests.
16. Keep the module independent from the existing AURA GUI initially.
17. Do not implement automatic public YouTube uploading in Phase 1.
18. Return a clear READY_FOR_CONTENT status when research succeeds.

Create complete working code and tests.
"""

engine = DeveloperEngineV2(workspace="workspace")

result = engine.develop(
    task=TASK,
    project_name="aura_youtube_research_engine"
)

print("=" * 60)
print("AURA YOUTUBE RESEARCH ENGINE - PHASE 1")
print("=" * 60)
print("PROJECT:", result["project_path"])
print("STATUS:", result["result"]["status"])
print("ITERATIONS:", result["result"]["iterations"])
print("=" * 60)
print("=" * 60)
print("DETAILED DEVELOPMENT HISTORY")
print("=" * 60)

for item in result["result"]["history"]:
    print("\nITERATION:", item["iteration"])
    print("OVERALL PASSED:", item["validation"]["overall_passed"])

    print("\nCOMPILE RESULTS:")
    for r in item["validation"].get("compile_results", []):
        print(r)

    print("\nTEST RESULTS:")
    for r in item["validation"].get("test_results", []):
        print(r)

    print("\nDEBUG:")
    print(item["debug"])