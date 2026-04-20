from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, func, BigInteger
from datetime import timezone

class Base(DeclarativeBase):
    pass

class MatchSummary(Base):
    __tablename__ = "match_summaries"
    id = mapped_column(Integer, primary_key=True)

    sender_id = mapped_column(String(36), nullable=False)
    sent_timestamp = mapped_column(String(50), nullable=False)
    batch_id = mapped_column(String(36), nullable=False)
    trace_id = mapped_column(BigInteger, nullable=False)

    match_id = mapped_column(String(36), nullable=False) #UUID String
    league = mapped_column(String(100), nullable=False)
    season = mapped_column(String(50), nullable=False)

    # Match date comes in "DD/MM/YYYY" format, so its stored as a string
    match_date = mapped_column(String(10), nullable=False)
    
    home_team_id = mapped_column(Integer, nullable=False)
    home_team_name = mapped_column(String(250), nullable=False)
    away_team_id = mapped_column(Integer, nullable=False)
    away_team_name = mapped_column(String(250), nullable=False)

    home_goals = mapped_column(Integer, nullable=False)
    away_goals = mapped_column(Integer, nullable=False)

    result = mapped_column(String(2), nullable=False)

    # COLUMN REQUIRED - Insert time (When it was saved to the db)
    date_created = mapped_column(DateTime, nullable=False, default=func.now())

    def to_dict(self):
        dc = self.date_created
        if dc is not None and dc.tzinfo is None:
            dc = dc.replace(tzinfo=timezone.utc)
        return {
        "id": self.id,
        "sender_id": self.sender_id,
        "sent_timestamp": self.sent_timestamp,
        "batch_id": self.batch_id,
        "trace_id": self.trace_id,
        "match_id": self.match_id,
        "league": self.league,
        "season": self.season,
        "match_date": self.match_date,
        "home_team_id": self.home_team_id,
        "home_team_name": self.home_team_name,
        "away_team_id": self.away_team_id,
        "away_team_name": self.away_team_name,
        "home_goals": self.home_goals,
        "away_goals": self.away_goals,
        "result": self.result,
        "date_created": dc.isoformat().replace("+00:00", "Z") if dc else None
        }


class BettingOdds(Base):
    __tablename__ = "betting_odds"
    id = mapped_column(Integer, primary_key=True)

    sender_id = mapped_column(String(36), nullable=False)
    sent_timestamp = mapped_column(String(50), nullable=False)
    batch_id = mapped_column(String(36), nullable=False)
    trace_id = mapped_column(BigInteger, nullable=False)

    match_id = mapped_column(String(36), nullable=False) #UUID String
    bookmaker = mapped_column(String(250), nullable=False)
    market = mapped_column(String(100), nullable=False)
    outcome = mapped_column(String(100), nullable=False)

    odds = mapped_column(Float, nullable=False)
    odds_type = mapped_column(String(20), nullable=False)

    # Event time when odds were collected
    collected_at = mapped_column(String(25), nullable=False)

    # COLUMN REQUIRED - Insert time (When it was saved to the db)
    date_created = mapped_column(DateTime, nullable=False, default=func.now())

    def to_dict(self):
        dc = self.date_created
        if dc is not None and dc.tzinfo is None:
            dc = dc.replace(tzinfo=timezone.utc)
        return {
        "id": self.id,
        "sender_id": self.sender_id,
        "sent_timestamp": self.sent_timestamp,
        "batch_id": self.batch_id,
        "trace_id": self.trace_id,
        "match_id": self.match_id,
        "bookmaker": self.bookmaker,
        "market": self.market,
        "outcome": self.outcome,
        "odds": self.odds,
        "odds_type": self.odds_type,
        "collected_at": self.collected_at,
        "date_created": dc.isoformat().replace("+00:00", "Z") if dc else None
        }