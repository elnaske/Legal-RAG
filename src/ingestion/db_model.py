from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Text,
    Date,
    DateTime,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


# Clusters are the parent object
class Cluster(Base):
    __tablename__ = "cluster"

    # unique id
    id = Column(BigInteger, primary_key=True)
    case_name = Column(Text)
    docket_number = Column(Text)
    date_filed = Column(Date)
    citation = Column(Text)
    absolute_url = Column(Text)
    precedential_status = Column(Text)
    raw_source = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relational part
    opinions = relationship("Opinion", back_populates="cluster")
    chunks = relationship("Chunk", back_populates="cluster")


# Opinions are the child object
class Opinions(Base):
    __tablename__ = "opinion"

    # unique id
    id = Column(BigInteger, primary_key=True)
    cluster_id = Column(
        BigInteger, ForeignKey("cluster.id", ondelete="CASCADE"), nullable=False
    )
    author = Column(Text)
    raw_source = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relational part
    cluster = relationship("Cluster", back_populates="opinions")
    chunks = relationship("Chunk", back_populates="opinions")


# these are the embeddings for Chroma
class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Text, primary_key=True)
    cluster_id = Column(
        BigInteger, ForeignKey("cluster.id", ondelete="CASCADE"), nullable=False
    )
    opinion_id = Column(
        BigInteger, ForeignKey("opinions.id", ondelete="CASCADE"), nullable=False
    )
    chunk_index = Column(Integer, nullable=False)
    chroma_collection = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relational part
    cluster = relationship("Cluster", back_populates="chunks")
    opinion = relationship("Opinion", back_populates="chunks")
