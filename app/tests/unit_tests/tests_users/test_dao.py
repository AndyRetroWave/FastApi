import pytest

from app.dao.base import BaseDAO
from app.users.dao import UsersDAO

BaseDAO


@pytest.mark.parametrize("id,email,is_present", [
    (1, "fedor@moloko.ru", True),
    (2, "....", False),
    ])
async def test_find_user_by_id(id, email, is_present):
    user = await UsersDAO.find_by_id(id)

    if is_present:
        assert user
        assert user.id == id
        assert user.email == email

    else: 
        assert not user
