from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///monsters.db", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT name FROM MONSTERS WHERE ac = 15"))
    print(result.all())