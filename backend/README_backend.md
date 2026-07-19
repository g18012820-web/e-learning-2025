"""
Backend README (Arabic)

يوضح هذا المستند كيفية تشغيل الـ Backend المحلي وربطه بقاعدة البيانات التي تم تصميمها.
"""

# E-Learning Backend (FastAPI)

هذا المشروع هو طبقة الـ Backend المصممة للعمل مع مخطّط قاعدة البيانات PostgreSQL 16+ الموجود في مجلد migrations/.

المتطلبات:
- Python 3.11+
- Docker & docker-compose (موصى به لتشغيل قاعدة البيانات محليًا)

تشغيل محلي سريع (باستخدام Docker):
1. انسخ ملف .env.example إلى .env وغيّر القيم المناسبة.
2. شغّل: docker-compose up --build
3. بعد تشغيل Postgres، نفّذ ملفات الهجرة SQL على قاعدة البيانات (أو استخدم Flyway).
4. شغّل backend: سيكون متاحًا على http://localhost:8000/docs

ملاحظات:
- استبدل JWT_SECRET في بيئة التشغيل بقيمة سرية قوية.
- تأكد من تشغيل الهجرات (مجلد migrations/) قبل تنفيذ أي عمليات.

