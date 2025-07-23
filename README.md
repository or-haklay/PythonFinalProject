פרויקט API לבלוג - Django REST Framework
📖 תיאור הפרויקט
פרויקט זה הוא REST API עבור פלטפורמת בלוג, שנבנה באמצעות Django ו-Django REST Framework. ה-API מאפשר ניהול מלא של משתמשים, כתבות, תגובות ותגיות, עם מערכת הרשאות מבוססת תפקידים ואימות באמצעות JWT.

✨ תכונות מרכזיות
מערכת משתמשים מלאה: הרשמה, התחברות ואימות באמצעות טוקנים (JWT).

ניהול תוכן (CRUD): יצירה, קריאה, עדכון ומחיקה של:

כתבות (Articles)

תגובות (Comments)

תגיות (Tags)

פרופיל משתמש: לכל משתמש פרופיל הניתן לעריכה עם פרטים נוספים.

מערכת הרשאות:

אורחים יכולים לצפות בכתבות ותגובות.

משתמשים רשומים יכולים לכתוב תגובות ולערוך את התוכן של עצמם.

מנהלי מערכת (Admins) יכולים ליצור, לערוך ולמחוק כל תוכן.

חיפוש: יכולת חיפוש דינמית בכתבות לפי כותרת, תוכן ושמות תגיות.

מערכת לייקים: אפשרות למשתמשים לסמן "לייק" על כתבות.

🛠️ טכנולוגיות
Backend: Python, Django, Django REST Framework

Database: PostgreSQL

Authentication: djangorestframework-simplejwt

Environment Variables: python-decouple

CORS: django-cors-headers

Code Quality: flake8

🚀 הוראות התקנה והרצה
כדי להריץ את הפרויקט על סביבה מקומית, בצע את השלבים הבאים.

דרישות קדם
Python 3.8+

PostgreSQL

Git

1. שיבוט (Clone) של הפרויקט
Bash

git clone <your-repository-url>
cd <repository-folder>
2. הקמת סביבה וירטואלית
Bash

# צור סביבה וירטואלית
python -m venv .venv

# הפעל את הסביבה
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
3. התקנת תלויות
התקן את כל החבילות הדרושות באמצעות קובץ ה-requirements.txt.

Bash

pip install -r requirements.txt
4. הגדרת משתני סביבה
צור קובץ חדש בתיקייה הראשית בשם .env. העתק לתוכו את התוכן הבא ועדכן את הפרטים בהתאם להגדרות ה-PostgreSQL שלך.

Code snippet

# .env

SECRET_KEY=your-secret-django-key-goes-here
DEBUG=True

# PostgreSQL Database
DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
5. הרצת מיגרציות
הפקודה תבנה את כל הטבלאות בבסיס הנתונים ותאכלס אותו במידע התחלתי (2 משתמשים, 2 כתבות וכו').

Bash

python manage.py migrate
6. יצירת משתמש-על (Superuser)
צור משתמש-על כדי לגשת לממשק הניהול של ג'אנגו.

Bash

python manage.py createsuperuser
עקוב אחר ההוראות להזנת שם משתמש, אימייל וסיסמה.

7. הרצת השרת
Bash

python manage.py runserver
השרת יהיה זמין בכתובת: http://127.0.0.1:8000/

🔗 נקודות קצה (API Endpoints)
Endpoint	Method	Description
/api/auth/register/	POST	הרשמת משתמש חדש.
/api/token/	POST	קבלת Access ו-Refresh טוקנים באמצעות שם משתמש וסיסמה.
/api/token/refresh/	POST	רענון Access token באמצעות Refresh token.
/api/articles/	GET, POST	קבלת רשימת כתבות או יצירת כתבה חדשה (למנהלים).
/api/articles/<id>/	GET, PUT, DELETE	צפייה, עדכון או מחיקה של כתבה ספציפית.
/api/articles/?search=<term>	GET	חיפוש כתבות.
/api/comments/	GET, POST	קבלת רשימת תגובות כללית או יצירת תגובה חדשה.
/api/comments/<id>/	GET, PUT, DELETE	צפייה, עדכון או מחיקה של תגובה ספציפית.
