from sqlalchemy.orm import Session
from datetime import datetime, timezone
from faker import Faker

from app import models
from app.utils.hashing import hash_password

def seed_data(db: Session):
    fake = Faker()

    # Seed roles
    if not db.query(models.Role).first():
        roles = [
            models.Role(name="admin"),
            models.Role(name="user")
        ]
        db.add_all(roles)
        db.commit()

    # Seed categories
    if not db.query(models.Category).first():
        categories = [
            models.Category(name="Linh tinh học", description="Các sách còn phân vân chưa biết phân loại vào đâu", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Khoa học viễn tưởng", description="Sách về các chủ đề khoa học viễn tưởng", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Khoa học tự nhiên", description="Sách về các lĩnh vực khoa học", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Xã hội học", description="Sách về các vấn đề xã hội và con người", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Toán học", description="Sách về toán học và lý thuyết số", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Văn học", description="Các tác phẩm văn học nổi tiếng", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Công nghệ", description="Sách về công nghệ và kỹ thuật", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Lịch sử", description="Sách về các sự kiện lịch sử quan trọng", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Triết học", description="Các tác phẩm triết học kinh điển", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Tâm lý học", description="Sách về tâm lý và hành vi con người", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Giáo dục", description="Sách giáo khoa và tài liệu học thuật", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Nghệ thuật", description="Sách về nghệ thuật và thiết kế", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
            models.Category(name="Du lịch", description="Sách hướng dẫn du lịch và khám phá thế giới", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)),
        ]
        db.add_all(categories)
        db.commit()

    # Seed users
    if not db.query(models.User).first():
        users = [
            models.User(
                username="admin1", 
                email="admin1@gmail.com", 
                hashed_password=hash_password("admin1"), 
                phone="0913584413", 
                dob="2000-01-01",
                is_active=1,
                role_id=1,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.User(
                username="admin2", 
                email="admin2@gmail.com", 
                hashed_password=hash_password("admin2"), 
                phone="0913584414", 
                dob="2000-01-02",
                is_active=1,
                role_id=1,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.User(
                username="Bảo đen", 
                email="baoden@gmail.com", 
                hashed_password=hash_password("123456789"), 
                phone="0123456789", 
                dob="2004-09-25",
                is_active=1,
                role_id=2,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.User(
                username="Nguyễn Văn A", 
                email="nguyenvana@gmail.com", 
                hashed_password=hash_password("123456789"), 
                phone="0124561454", 
                dob="2020-07-25",
                is_active=0,
                role_id=2,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.User(
                username="Phạm Hồng Nhung",
                email="nhung.pham@gmail.com",
                hashed_password=hash_password("123456789"),
                phone="0933445566",
                dob="2002-11-20",
                is_active=1,
                role_id=2,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            models.User(
                username="Park Boeun",
                email="pb@gmail.com",
                hashed_password=hash_password("123456789"),
                phone="0987654321",
                dob="1998-05-15",
                is_active=1,
                role_id=2,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            models.User(
                username="Zlatan Ibrahimović",
                email="zlatan@gmail.com",
                hashed_password=hash_password("123456789"),
                phone="0912341648",
                dob="1981-10-03",
                is_active=1,
                role_id=2,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            models.User(
                username="Nguyễn Thị Mai",
                email="nguyenthi@gmail.com",
                hashed_password=hash_password("123456789"),
                phone="0915891648",
                dob="1951-12-23",
                is_active=1,
                role_id=2,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            models.User(
                username="Lê Văn Tứ",
                email="levantu@gmail.com",
                hashed_password=hash_password("123456789"),
                phone="0914582678",
                dob="1960-11-21",
                is_active=1,
                role_id=2,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
        ]
        db.add_all(users)
        db.commit()

    # Seed authors
    if not db.query(models.Author).first():
        authors = [
            models.Author(name="Nguyễn Nhật Ánh"),
            models.Author(name="Haruki Murakami"),
            models.Author(name="J.K. Rowling"),
            models.Author(name="George Orwell"),
            models.Author(name="Albert Camus"),
            models.Author(name="Isaac Asimov"),
            models.Author(name="Stephen King"),
            models.Author(name="Jane Austen"),
            models.Author(name="Mark Twain"),
            models.Author(name="Charles Dickens"),
            models.Author(name="Vũ Quốc Bảo"),
        ]
        db.add_all(authors)
        db.commit()

    # Seed books
    if not db.query(models.Book).first():
        books = [
            models.Book(
                title="Khi lỗi thuộc về những vì sao",
                main_author_id=1,
                description="Một câu chuyện tình yêu đầy cảm động giữa hai người trẻ tuổi mắc bệnh ung thư.",
                quantity=10,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                category_id=1
            ),
            models.Book(
                title="Kafka bên bờ biển",
                main_author_id=2,
                description="Một tác phẩm kỳ ảo và sâu sắc về cuộc sống và số phận.",
                quantity=5,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                category_id=2
            ),
            models.Book(
                title="Harry Potter và Hòn đá Phù thủy",
                main_author_id=3,
                description="Cuộc phiêu lưu của cậu bé phù thủy Harry Potter tại trường Hogwarts.",
                quantity=15,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                category_id=3
            ),
            models.Book(
                title="Bảo đen và những người bạn",
                main_author_id=11,
                description="Một tác phẩm kinh điển về những câu chuyện xoay quanh Bảo đen.",
                quantity=102,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                category_id=1
            ),
        ]
        db.add_all(books)
        db.commit()