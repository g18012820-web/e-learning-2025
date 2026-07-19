from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction
from sqlalchemy import select, update, insert, text
from decimal import Decimal

class WalletService:
    @staticmethod
    async def get_wallet_by_user(session: AsyncSession, user_id):
        stmt = select(Wallet).where(Wallet.user_id == user_id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def create_wallet_for_user(session: AsyncSession, user_id):
        w = Wallet(user_id=user_id)
        session.add(w)
        await session.flush()
        return w

    @staticmethod
    async def apply_recharge(session: AsyncSession, wallet_id, amount: Decimal, reference: str = None):
        # Use SELECT FOR UPDATE in raw SQL to lock wallet row
        await session.execute(text("LOCK TABLE wallets IN SHARE ROW EXCLUSIVE MODE"))
        stmt = select(Wallet).where(Wallet.id == wallet_id)
        res = await session.execute(stmt)
        w = res.scalar_one_or_none()
        if not w:
            raise ValueError('Wallet not found')
        # update amounts
        new_balance = (w.balance or 0) + Decimal(amount)
        upd = update(Wallet).where(Wallet.id == wallet_id).values(balance=new_balance, total_recharged=(w.total_recharged or 0) + Decimal(amount))
        await session.execute(upd)
        txn = WalletTransaction(wallet_id=wallet_id, transaction_type='recharge', amount=Decimal(amount), description='Admin recharge', reference=reference, status='completed')
        session.add(txn)
        await session.commit()
        return True
