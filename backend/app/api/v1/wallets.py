from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_session, require_owner, get_current_user
from app.services.wallet_service import WalletService
from app.models.wallet import Wallet
from app.db.connection import AsyncSessionLocal
from decimal import Decimal

router = APIRouter(prefix='/v1/wallets', tags=['wallets'])

@router.get('/me')
async def my_wallet(current_user = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    w = await WalletService.get_wallet_by_user(session, current_user.id)
    if not w:
        w = await WalletService.create_wallet_for_user(session, current_user.id)
    return {"id": str(w.id), "balance": str(w.balance), "total_recharged": str(w.total_recharged), "total_spent": str(w.total_spent)}

@router.post('/{user_id}/admin_recharge')
async def admin_recharge(user_id: str, amount: float, reference: str = None, _owner = Depends(require_owner), session: AsyncSession = Depends(get_session)):
    # Owner endpoint to credit wallet
    # find or create wallet
    from uuid import UUID
    try:
        uid = UUID(user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user id')
    w = await WalletService.get_wallet_by_user(session, uid)
    if not w:
        w = await WalletService.create_wallet_for_user(session, uid)
    try:
        await WalletService.apply_recharge(session, w.id, Decimal(amount), reference)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"message": "wallet credited"}
