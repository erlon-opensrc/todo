from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.models import User


def test_create_user(session: Session, mock_db_time):  # type: ignore
    with mock_db_time(model=User) as time:  # type: ignore
        new_user = User(
            username='Alice', email='alice@example.com', password='secret'
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'Alice'))

    new_user_dict = asdict(new_user)
    new_user_dict.update({'id': 1})
    new_user_dict.update({'created_at': time})  # time gerado por mock_db_time
    new_user_dict.update({'updated_at': time})

    assert user is not None
    assert asdict(user) == new_user_dict
