from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

from app import dependencies, models, schemas
from app.models.user import User

router = APIRouter()

# Endpoint để lấy danh sách sách đang mượn
@router.get("/current", response_model=list[schemas.BorrowResponse])
def get_current_borrows(
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.require_user)
):
    borrows = db.query(models.Borrow).options(joinedload(models.Borrow.book)).filter(
        models.Borrow.user_id == current_user.id,
        models.Borrow.status == 'borrowing'
    ).all()
    return borrows

# Endpoint để lấy lịch sử mượn sách
@router.get("/history", response_model=list[schemas.BorrowResponse])
def get_borrow_history(
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.require_user)
):
    borrows = db.query(models.Borrow).options(joinedload(models.Borrow.book)).filter(
        models.Borrow.user_id == current_user.id,
        models.Borrow.status != 'borrowing'
    ).order_by(models.Borrow.borrow_date.desc()).all()
    return borrows

# Endpoint để người dùng mượn một cuốn sách
@router.post("/borrow/{book_id}", response_model=schemas.BorrowResponse)
def borrow_book(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.require_user)
):
    # 1. Kiểm tra sách có tồn tại và còn sách không
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is out of stock")

    # 2. Kiểm tra người dùng đã mượn cuốn này chưa
    existing_borrow = db.query(models.Borrow).filter(
        models.Borrow.user_id == current_user.id,
        models.Borrow.book_id == book_id,
        models.Borrow.status == 'borrowing'
    ).first()
    if existing_borrow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already borrowed this book")

    # 3. Tạo lượt mượn mới
    new_borrow = models.Borrow(
        user_id=current_user.id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14) # Hạn trả sách là 14 ngày
    )
    
    # 4. Giảm số lượng sách
    book.quantity -= 1

    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    
    return new_borrow