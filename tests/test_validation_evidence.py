import asyncio
import sys
from http import HTTPStatus
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from profile_checker import main


class FakeResponse:
    status_code = HTTPStatus.OK

    @staticmethod
    def json():
        return {
            "valid": False,
            "reason": "taken",
            "msg": "Username has already been taken",
            "desc": "That username has been taken. Please choose another.",
        }


class FakeClient:
    async def get(self, *_args, **_kwargs):
        return FakeResponse()


def test_x_validation_evidence_is_returned(monkeypatch):
    monkeypatch.setattr(main, "client", FakeClient())

    exists, evidence = asyncio.run(
        main.confirm_profile_exists(
            "https://api.x.com/i/users/username_available.json?username=example",
            "example",
            "X",
        )
    )

    assert exists is True
    assert evidence.reason.value == "taken"
    assert evidence.msg == "Username has already been taken"
    assert evidence.desc == "That username has been taken. Please choose another."
