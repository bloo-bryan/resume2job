import pytest
from httpx import ASGITransport, AsyncClient

from resume2job.api.app import app

SAMPLE_RESUME = (
    "Senior Python developer with 5 years of machine learning experience."
    " Skills: Python, PyTorch, NLP, Docker, SQL."
)
SAMPLE_JD = (
    "Looking for a Senior ML Engineer with Python, PyTorch, and NLP experience."
    " 3+ years required. Bachelor's degree minimum."
)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestHealthEndpoint:
    async def test_health_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("healthy", "unhealthy")
        assert "models_loaded" in data


class TestParseEndpoint:
    async def test_parse_resume_text(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/parse",
            data={
                "doc_type": "resume",
                "text": "John Doe\nSenior Python developer\nSkills: Python, PyTorch",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "raw_text" in data
        assert "entities" in data
        assert data["doc_type"] == "resume"

    async def test_parse_jd_text(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/parse",
            data={
                "doc_type": "job_description",
                "text": "Looking for Senior ML Engineer with Python, PyTorch. 3+ years.",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["doc_type"] == "job_description"
        assert "entities" in data

    async def test_parse_missing_both_text_and_file(self, client: AsyncClient) -> None:
        response = await client.post("/api/parse", data={"doc_type": "resume"})
        assert response.status_code == 400

    async def test_parse_invalid_doc_type(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/parse",
            data={"doc_type": "invalid", "text": "some text"},
        )
        assert response.status_code == 400


class TestMatchEndpoint:
    async def test_match_hybrid(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/match",
            json={"resume_text": SAMPLE_RESUME, "jd_text": SAMPLE_JD},
        )
        assert response.status_code == 200
        data = response.json()
        assert 0 <= data["overall_score"] <= 1
        assert "breakdown" in data
        assert "summary" in data

    async def test_match_tfidf_algorithm(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/match",
            json={
                "resume_text": "Python developer",
                "jd_text": "Looking for Python developer",
                "algorithm": "tfidf",
            },
        )
        assert response.status_code == 200

    async def test_match_invalid_algorithm(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/match",
            json={
                "resume_text": "text",
                "jd_text": "text",
                "algorithm": "invalid",
            },
        )
        assert response.status_code == 400


class TestCompareEndpoint:
    async def test_compare_returns_all_algorithms(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/match/compare",
            json={
                "resume_text": SAMPLE_RESUME,
                "jd_text": SAMPLE_JD,
            },
        )
        assert response.status_code == 200
        data = response.json()
        for algo in ("tfidf", "embedding", "hybrid"):
            assert algo in data
            assert "overall_score" in data[algo]
            assert "breakdown" in data[algo]
